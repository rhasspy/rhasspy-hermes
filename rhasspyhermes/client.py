"""MQTT Hermes client base class"""
import asyncio
import io
import json
import logging
import subprocess
import threading
import typing
import wave
from concurrent.futures import CancelledError

from .audioserver import AudioFrame, AudioSessionFrame, AudioSummary
from .base import Message

# -----------------------------------------------------------------------------

TopicArgs = typing.Mapping[str, typing.Any]
GeneratorType = typing.AsyncIterable[
    typing.Optional[typing.Union[Message, typing.Tuple[Message, TopicArgs]]]
]

# -----------------------------------------------------------------------------


class HermesClient:
    """Base class for Hermes MQTT clients"""

    def __init__(
        self,
        client_name: str,
        mqtt_client,
        siteIds: typing.Optional[typing.List[str]] = None,
        sample_rate: int = 16000,
        sample_width: int = 2,
        channels: int = 1,
        loop=None,
    ):
        # Internal logger
        self.client_name = client_name
        self.logger = logging.getLogger(client_name)

        # Paho MQTT client
        self.mqtt_client = mqtt_client
        self.mqtt_client.on_connect = self.mqtt_on_connect
        self.mqtt_client.on_disconnect = self.mqtt_on_disconnect
        self.mqtt_client.on_message = self.mqtt_on_message

        # Set when on_connect succeeds
        self.mqtt_connected_event: asyncio.Event = asyncio.Event()
        self.mqtt_stopped_event: asyncio.Event = asyncio.Event()

        self.is_connected: bool = False
        self.subscribe_lock = threading.Lock()
        self.pending_mqtt_topics: typing.Set[str] = set()

        # Incoming message queue (async)
        self.in_queue: asyncio.Queue = asyncio.Queue()

        # Message types that are subscribed to
        self.subscribed_types: typing.Set[typing.Type[Message]] = set()

        # Set of valid siteIds (empty for all)
        self.siteIds: typing.Set[str] = set(siteIds) if siteIds else set()
        self.siteId = "default" if not siteIds else siteIds[0]

        # Event loop
        self.loop = loop or asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self.handle_messages_async(), self.loop)

        # Required audio format
        self.sample_rate = sample_rate
        self.sample_width = sample_width
        self.channels = channels

    # -------------------------------------------------------------------------
    # User Methods
    # -------------------------------------------------------------------------

    def subscribe(self, *message_types: typing.Type[Message], **topic_args):
        """Subscribe to one or more Hermes messages."""
        topics: typing.List[str] = []

        if self.siteIds:
            # Specific siteIds
            for siteId in self.siteIds:
                for message_type in message_types:
                    topics.append(message_type.topic(siteId=siteId))
                    self.subscribed_types.add(message_type)
        else:
            # All siteIds
            for message_type in message_types:
                topics.append(message_type.topic())
                self.subscribed_types.add(message_type)

        # Subscribe to all MQTT topics
        self.subscribe_topics(*topics)

    def subscribe_topics(self, *topics):
        """Subscribe to one or more MQTT topics."""
        with self.subscribe_lock:
            self.pending_mqtt_topics.update(topics)

            if self.is_connected:
                # Subscribe to all pending topics
                for topic in self.pending_mqtt_topics:
                    self.mqtt_client.subscribe(topic)
                    self.logger.debug("Subscribed to %s", topic)

                self.pending_mqtt_topics.clear()

    async def on_message(
        self,
        message: Message,
        siteId: typing.Optional[str] = None,
        sessionId: typing.Optional[str] = None,
        topic: typing.Optional[str] = None,
    ) -> GeneratorType:
        """Override to handle Hermes messages."""
        yield None

    async def on_raw_message(self, topic: str, payload: bytes):
        """Override to handle MQTT messages."""
        pass

    def stop(self):
        """Stop message handler gracefully."""
        if self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.in_queue.put(None), self.loop)
            asyncio.run_coroutine_threadsafe(self.mqtt_stopped_event.wait(), self.loop)

    # -------------------------------------------------------------------------
    # MQTT Event Handlers
    # -------------------------------------------------------------------------

    def mqtt_on_connect(self, client, userdata, flags, rc):
        """Connected to MQTT broker."""
        try:
            self.is_connected = True
            self.logger.debug("Connected to MQTT broker")
            self.subscribe()
            self.loop.call_soon_threadsafe(self.mqtt_connected_event.set)
        except Exception:
            self.logger.exception("on_connect")

    def mqtt_on_disconnect(self, client, userdata, flags, rc):
        """Automatically reconnect when disconnected."""
        try:
            # Automatically reconnect
            self.loop.call_soon_threadsafe(self.mqtt_connected_event.clear)
            self.is_connected = False
            self.logger.warning("Disconnected. Trying to reconnect...")
            self.mqtt_client.reconnect()
        except Exception:
            self.logger.exception("on_disconnect")

    def mqtt_on_message(self, client, userdata, msg):
        """Received message from MQTT broker."""
        try:
            # Handle message in event loop
            asyncio.run_coroutine_threadsafe(self.in_queue.put(msg), self.loop)
        except Exception:
            self.logger.exception("on_message")

    async def handle_messages_async(self):
        """Handles MQTT messages in event loop."""
        while self.loop.is_running():
            try:
                mqtt_message = await self.in_queue.get()
                if mqtt_message is None:
                    break

                # Fire and forget
                asyncio.ensure_future(
                    self.on_raw_message(mqtt_message.topic, mqtt_message.payload),
                    loop=self.loop,
                )

                # Check against all known message types
                for message_type in self.subscribed_types:
                    if message_type.is_topic(mqtt_message.topic):
                        # Verify siteId and parse
                        if message_type.is_binary_payload():
                            # Binary
                            if message_type.is_site_in_topic():
                                siteId = message_type.get_siteId(mqtt_message.topic)
                                if not self.valid_siteId(siteId):
                                    continue

                            # Assume payload is only argument to constructor
                            message = message_type(mqtt_message.payload)
                            if not isinstance(message, (AudioFrame, AudioSessionFrame)):
                                self.logger.debug(
                                    "<- %s(%s byte(s))",
                                    message_type.__name__,
                                    len(mqtt_message.payload),
                                )
                        else:
                            # JSON
                            json_payload = json.loads(mqtt_message.payload)
                            if message_type.is_site_in_topic():
                                siteId = message_type.get_siteId(mqtt_message.topic)
                            else:
                                siteId = json_payload.get("siteId", "default")

                            if not self.valid_siteId(siteId):
                                continue

                            # Load from JSON
                            message = message_type.from_dict(json_payload)

                            if not isinstance(message, AudioSummary):
                                self.logger.debug("<- %s", message)

                        sessionId = None
                        if message_type.is_session_in_topic():
                            sessionId = message_type.get_sessionId(mqtt_message.topic)

                        # Publish all responses
                        asyncio.ensure_future(
                            self.publish_all(
                                self.on_message(
                                    message,
                                    siteId=siteId,
                                    sessionId=sessionId,
                                    topic=mqtt_message.topic,
                                )
                            ),
                            loop=self.loop,
                        )

                        # Assume only one message type will match
                        break
            except KeyboardInterrupt:
                break
            except CancelledError:
                break
            except Exception:
                self.logger.exception("handle_messages_async")
                break
            finally:
                self.mqtt_stopped_event.set()

    # -------------------------------------------------------------------------
    # Publishing Messages
    # -------------------------------------------------------------------------

    def publish(self, message: Message, **topic_args):
        """Publish a Hermes message to MQTT."""
        try:
            topic = message.topic(**topic_args)
            payload = message.payload()

            if message.is_binary_payload():
                # Don't log audio frames
                if not isinstance(message, (AudioFrame, AudioSessionFrame)):
                    self.logger.debug(
                        "-> %s(%s byte(s))", message.__class__.__name__, len(payload)
                    )
            else:
                # Log most JSON messages
                if not isinstance(message, AudioSummary):
                    self.logger.debug("-> %s", message)
                    self.logger.debug(
                        "Publishing %s bytes(s) to %s", len(payload), topic
                    )

            self.mqtt_client.publish(topic, payload)
        except Exception:
            self.logger.exception("publish")

    async def publish_all(self, async_generator: GeneratorType):
        """Enumerate all messages in an async generator publish them"""
        async for maybe_message in async_generator:
            if maybe_message is None:
                continue

            if isinstance(maybe_message, Message):
                self.publish(maybe_message)
            else:
                message, kwargs = maybe_message
                self.publish(message, **kwargs)

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def valid_siteId(self, siteId: str):
        """True if siteId is valid for this client."""
        if self.siteIds:
            return siteId in self.siteIds

        return True

    def convert_wav(
        self,
        wav_bytes: bytes,
        sample_rate: typing.Optional[int] = None,
        sample_width: typing.Optional[int] = None,
        channels: typing.Optional[int] = None,
    ) -> bytes:
        """Converts WAV data to required format with sox. Return raw audio."""
        if sample_rate is None:
            sample_rate = self.sample_rate

        if sample_width is None:
            sample_width = self.sample_width

        if channels is None:
            channels = self.channels

        return subprocess.run(
            [
                "sox",
                "-t",
                "wav",
                "-",
                "-r",
                str(sample_rate),
                "-e",
                "signed-integer",
                "-b",
                str(sample_width * 8),
                "-c",
                str(channels),
                "-t",
                "raw",
                "-",
            ],
            check=True,
            stdout=subprocess.PIPE,
            input=wav_bytes,
        ).stdout

    def maybe_convert_wav(
        self,
        wav_bytes: bytes,
        sample_rate: typing.Optional[int] = None,
        sample_width: typing.Optional[int] = None,
        channels: typing.Optional[int] = None,
    ) -> bytes:
        """Converts WAV data to required format if necessary. Returns raw audio."""
        if sample_rate is None:
            sample_rate = self.sample_rate

        if sample_width is None:
            sample_width = self.sample_width

        if channels is None:
            channels = self.channels

        with io.BytesIO(wav_bytes) as wav_io:
            with wave.open(wav_io, "rb") as wav_file:
                if (
                    (wav_file.getframerate() != sample_rate)
                    or (wav_file.getsampwidth() != sample_width)
                    or (wav_file.getnchannels() != channels)
                ):
                    # Return converted wav
                    return self.convert_wav(
                        wav_bytes,
                        sample_rate=sample_rate,
                        sample_width=sample_width,
                        channels=channels,
                    )

                # Return original audio
                return wav_file.readframes(wav_file.getnframes())

    def to_wav_bytes(
        self,
        audio_data: bytes,
        sample_rate: typing.Optional[int] = None,
        sample_width: typing.Optional[int] = None,
        channels: typing.Optional[int] = None,
    ) -> bytes:
        """Wrap raw audio data in WAV."""
        if sample_rate is None:
            sample_rate = self.sample_rate

        if sample_width is None:
            sample_width = self.sample_width

        if channels is None:
            channels = self.channels

        with io.BytesIO() as wav_buffer:
            wav_file: wave.Wave_write = wave.open(wav_buffer, mode="wb")
            with wav_file:
                wav_file.setframerate(sample_rate)
                wav_file.setsampwidth(sample_width)
                wav_file.setnchannels(channels)
                wav_file.writeframes(audio_data)

            return wav_buffer.getvalue()
