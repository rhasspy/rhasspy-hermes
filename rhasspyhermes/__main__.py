"""Command-line interface to rhasspyhermes"""
import argparse
import io
import json
import logging
import os
import sys
import threading
from pathlib import Path
from uuid import uuid4

import attr
import paho.mqtt.client as mqtt

from .base import Message

_LOGGER = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


def main():
    """Main method"""
    # Parse command-line arguments
    args = get_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    _LOGGER.debug(args)

    # Connect to MQTT broker
    connected_event = threading.Event()
    client = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        try:
            # Signal main thread
            connected_event.set()
        except Exception:
            _LOGGER.exception("on_connect")

    def on_disconnect(client, userdata, flags, rc):
        try:
            # Automatically reconnect
            _LOGGER.info("Disconnected. Trying to reconnect...")
            client.reconnect()
        except Exception:
            _LOGGER.exception("on_disconnect")

    # Connect
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    def log_subscribe(topic):
        _LOGGER.debug("Subscribed to %s", topic)
        mqtt.Client.subscribe(client, topic)

    client.subscribe = log_subscribe

    _LOGGER.debug("Connecting to %s:%s", args.host, args.port)
    client.connect(args.host, args.port)

    client.loop_start()

    try:
        siteId = "default"
        if args.siteId:
            # Use first siteId
            siteId = args.siteId[0]
            args.siteId = set(args.siteId)

        # Call sub-commmand
        args.func(args, client, siteId)
    except KeyboardInterrupt:
        pass
    finally:
        _LOGGER.debug("Shutting down")
        client.loop_stop()


def get_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="rhasspy_hermes", description="rhasspy_hermes"
    )
    parser.add_argument(
        "--host", default="localhost", help="MQTT host (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=1883, help="MQTT port (default: 1883)"
    )
    parser.add_argument(
        "--siteId",
        action="append",
        help="Hermes siteId(s) to listen for (default: all)",
    )
    parser.add_argument(
        "--print-topics",
        action="store_true",
        help="Print MQTT topics with JSON messages",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Print DEBUG messages to the console"
    )

    # Create subparsers for each sub-command
    sub_parsers = parser.add_subparsers()
    sub_parsers.required = True
    sub_parsers.dest = "command"

    # --------------
    # transcribe-wav
    # --------------
    transcribe_parser = sub_parsers.add_parser(
        "transcribe-wav", help="Transcribe WAV file(s)"
    )
    transcribe_parser.set_defaults(func=transcribe)
    transcribe_parser.add_argument(
        "wav_file", nargs="*", default=[], help="Path(s) to WAV file(s)"
    )
    transcribe_parser.add_argument(
        "--stdin-files",
        "-f",
        action="store_true",
        help="Read WAV file paths from stdin instead of WAV data",
    )

    # ----------------
    # recognize-intent
    # ----------------
    recognize_parser = sub_parsers.add_parser(
        "recognize-intent", help="Recognize intent(s) from text"
    )
    recognize_parser.set_defaults(func=recognize)
    recognize_parser.add_argument(
        "sentence", nargs="*", default=[], help="Sentences to recognize"
    )

    # --------------
    # speak-sentence
    # --------------
    speak_parser = sub_parsers.add_parser("speak-sentence", help="Speak sentence(s)")
    speak_parser.add_argument("sentence", nargs="*", help="Sentence(s) to speak")
    speak_parser.add_argument(
        "--language", default="", help="Language for text to speech"
    )
    speak_parser.set_defaults(func=speak)

    # ---------
    # wait-wake
    # ---------
    wake_parser = sub_parsers.add_parser(
        "wait-wake", help="Wait until wake word is detected"
    )
    wake_parser.add_argument(
        "--toggle",
        action="store_true",
        help="Toggle hotword service on/off around detection",
    )
    wake_parser.add_argument(
        "--wakewordId",
        action="append",
        default=["default"],
        help="Wake word id(s) to wait for",
    )
    wake_parser.set_defaults(func=wake)

    return parser.parse_args()


# -----------------------------------------------------------------------------


def publish(client, message: Message, **topic_args):
    """Publish a Hermes message to MQTT."""
    try:
        _LOGGER.debug("-> %s", message)
        topic = message.topic(**topic_args)
        payload = json.dumps(attr.asdict(message))
        _LOGGER.debug("Publishing %s char(s) to %s", len(payload), topic)
        client.publish(topic, payload)
    except Exception:
        _LOGGER.exception("on_message")


def check_siteId(args, json_payload):
    """Return True if siteId matches one of configured siteIds"""
    if args.siteId:
        siteId = json_payload.get("siteId", "default")
        return siteId in args.siteId

    return True


def print_json(args, topic: str, message: Message):
    """Print Hermes message as single line of JSON to stdout"""
    if args.print_topics:
        print(topic, end=" ")

    json.dump(attr.asdict(message), sys.stdout)
    print("")
    sys.stdout.flush()


# -----------------------------------------------------------------------------


def transcribe(args, client, siteId):
    """Transcribe one or more WAV files using hermes/asr"""
    from .asr import AsrStartListening, AsrStopListening, AsrTextCaptured
    from .audioserver import AudioFrame

    client.subscribe(AsrTextCaptured.topic())
    frame_topic = AudioFrame.topic(siteId=siteId)

    if args.wav_file:
        # Read WAV paths from command-line arguments
        def get_wavs():
            for wav_path in args.wav_file:
                wav_path = Path(wav_path)
                with open(wav_path, "rb") as wav_file:
                    yield str(wav_path), wav_file

    elif args.stdin_files:
        # Read WAV paths from stdin (one per line)
        def get_wavs():
            for wav_path in sys.stdin:
                wav_path = Path(wav_path.strip())
                with open(wav_path, "rb") as wav_file:
                    yield str(wav_path), wav_file

    else:
        # Read WAV data from stdin
        def get_wavs():
            if os.isatty(sys.stdin.fileno()):
                print("Reading WAV data from stdin...", file=sys.stderr)

            wav_bytes = sys.stdin.buffer.read()
            with io.BytesIO(wav_bytes) as wav_file:
                yield "<stdin>", wav_file

    for wav_name, wav_file in get_wavs():
        _LOGGER.debug("Transcribing %s", wav_name)

        done_event = threading.Event()
        result_topic = ""
        text_captured = None
        sessionId = str(uuid4())

        def on_message(client, userdata, msg):
            nonlocal result_topic, text_captured
            try:
                if msg.topic == AsrTextCaptured.topic():
                    # Verify siteId/sessionId
                    json_payload = json.loads(msg.payload)
                    if check_siteId(args, json_payload) and (
                        json_payload.get("sessionId", "") == sessionId
                    ):
                        # Matched
                        result_topic = msg.topic
                        text_captured = AsrTextCaptured(**json_payload)
                        done_event.set()
            except Exception:
                _LOGGER.exception("transcribe.on_message")

        client.on_message = on_message

        with wav_file:
            # startListening
            publish(client, AsrStartListening(siteId=siteId, sessionId=sessionId))

            # Send WAV chunks (audioFrame)
            for wav_chunk in AudioFrame.iter_wav_chunked(
                wav_file, frames_per_chunk=2048
            ):
                client.publish(frame_topic, wav_chunk)

            # stopListening
            publish(client, AsrStopListening(siteId=siteId, sessionId=sessionId))

        _LOGGER.debug(
            "Waiting for textCaptured (%s, sessionId=%s)", wav_name, sessionId
        )

        # Wait for textCaptured
        done_event.wait()

        # Print result
        assert text_captured is not None
        print_json(args, result_topic, text_captured)


# -----------------------------------------------------------------------------


def recognize(args, client, siteId):
    """Recognize intent(s) from one or more sentences using hermes/nlu"""
    from .nlu import NluQuery, NluIntent, NluIntentNotRecognized, NluError

    client.subscribe(NluIntent.topic(intentName="#"))
    client.subscribe(NluIntentNotRecognized.topic())
    client.subscribe(NluError.topic())

    if args.sentence:
        # Read sentences from arguments
        sentences = args.sentence
    else:
        # Read sentences from stdin
        if os.isatty(sys.stdin.fileno()):
            print("Reading sentences from stdin...", file=sys.stderr)

        sentences = args.stdin

    # Process sentences
    for sentence in sentences:
        sentence = sentence.strip()
        _LOGGER.debug("Processing '%s'", sentence)

        done_event = threading.Event()
        result_topic = ""
        result_message = None
        queryId = str(uuid4())
        sessionId = str(uuid4())

        def on_message(client, userdata, msg):
            nonlocal result_topic, result_message
            try:
                if NluIntent.is_topic(msg.topic):
                    # Verify siteId/id/sessionId
                    json_payload = json.loads(msg.payload)
                    if (
                        check_siteId(args, json_payload)
                        and (json_payload.get("sessionId", "") == sessionId)
                        and (json_payload.get("id", "") == queryId)
                    ):
                        # Matched
                        result_topic = msg.topic
                        result_message = NluIntent(**json_payload)
                        done_event.set()
                elif msg.topic == NluIntentNotRecognized.topic():
                    # Verify siteId/id/sessionId
                    json_payload = json.loads(msg.payload)
                    if (
                        check_siteId(args, json_payload)
                        and (json_payload.get("id", "") == queryId)
                        and (json_payload.get("sessionId", "") == sessionId)
                    ):
                        # Not recognized
                        result_topic = msg.topic
                        result_message = NluIntentNotRecognized(**json_payload)
                        done_event.set()
                elif msg.topic == NluError.topic():
                    # Verify siteId/sessionId
                    json_payload = json.loads(msg.payload)
                    if check_siteId(args, json_payload) and (
                        json_payload.get("sessionId", "") == sessionId
                    ):
                        # Error
                        result_topic = msg.topic
                        result_message = NluError(**json_payload)
                        _LOGGER.error(result_message.error)
                        done_event.set()
            except Exception:
                _LOGGER.exception("recognize.on_message")

        client.on_message = on_message

        # Send query
        publish(
            client,
            NluQuery(input=sentence, siteId=siteId, id=queryId, sessionId=sessionId),
        )

        # Wait for response
        _LOGGER.debug("Waiting for intent/notRecognized/error (id=%s)", queryId)
        done_event.wait()

        # Print result
        assert result_message is not None
        print_json(args, result_topic, result_message)


# -----------------------------------------------------------------------------


def speak(args, client, siteId):
    """Speak one or more sentences using hermes/tts"""
    from .tts import TtsSay, TtsSayFinished

    client.subscribe(TtsSayFinished.topic())

    if args.sentence:
        # Read sentences from arguments
        sentences = args.sentence
    else:
        # Read sentences from stdin
        if os.isatty(sys.stdin.fileno()):
            print("Reading sentences from stdin...", file=sys.stderr)

        sentences = args.stdin

    # Speak sentences
    for sentence in sentences:
        sentence = sentence.strip()
        _LOGGER.debug("Speaking '%s'", sentence)

        done_event = threading.Event()
        result_topic = ""
        result_message = None
        sayId = str(uuid4())
        sessionId = str(uuid4())

        def on_message(client, userdata, msg):
            nonlocal result_topic, result_message
            try:
                if msg.topic == TtsSayFinished.topic():
                    # Verify siteId/id/sessionId
                    json_payload = json.loads(msg.payload)
                    if (
                        check_siteId(args, json_payload)
                        and (json_payload.get("sessionId", "") == sessionId)
                        and (json_payload.get("id", "") == sayId)
                    ):
                        # Matched
                        result_topic = msg.topic
                        result_message = TtsSayFinished(**json_payload)
                        done_event.set()
            except Exception:
                _LOGGER.exception("speak.on_message")

        client.on_message = on_message

        # Send say
        publish(
            client,
            TtsSay(
                text=sentence,
                lang=args.language,
                siteId=siteId,
                id=sayId,
                sessionId=sessionId,
            ),
        )

        # Wait for finished
        _LOGGER.debug("Waiting for finished (id=%s)", sayId)
        done_event.wait()

        # Print result
        assert result_message is not None
        print_json(args, result_topic, result_message)


# -----------------------------------------------------------------------------


def wake(args, client, siteId):
    """Wait until wake word is detected"""
    from .wake import HotwordToggleOn, HotwordDetected, HotwordToggleOff

    assert args.wakewordId, "No wake word ids"
    for wakewordId in args.wakewordId:
        client.subscribe(HotwordDetected.topic(wakewordId=wakewordId))

    done_event = threading.Event()
    result_topic = ""
    result_message = None

    def on_message(client, userdata, msg):
        nonlocal result_topic, result_message
        try:
            if HotwordDetected.is_topic(msg.topic):
                # Verify wakewordId
                wakewordId = HotwordDetected.get_wakewordId(msg.topic)
                if wakewordId in args.wakewordId:
                    # Matched
                    json_payload = json.loads(msg.payload)
                    result_topic = msg.topic
                    result_message = HotwordDetected(**json_payload)
                    done_event.set()
        except Exception:
            _LOGGER.exception("speak.on_message")

    client.on_message = on_message

    if args.toggle:
        # toggleOn
        publish(client, HotwordToggleOn(siteId=siteId))

    # Wait for detection
    _LOGGER.debug("Waiting for detected (wakewordId=%s)", args.wakewordId)
    done_event.wait()

    if args.toggle:
        # toggleOff
        publish(client, HotwordToggleOff(siteId=siteId))

    # Print result
    assert result_message is not None
    print_json(args, result_topic, result_message)


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
