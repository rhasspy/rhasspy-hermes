"""Messages for hermes/audioServer"""
import io
import re
import typing
import wave
from enum import Enum
from uuid import uuid4

import attr

from .base import Message


@attr.s(auto_attribs=True, slots=True)
class AudioFrame(Message):
    """Captured sound frame."""

    TOPIC_PATTERN = re.compile(r"^hermes/audioServer/([^/]+)/audioFrame$")

    wav_data: bytes

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        siteId = kwargs.get("siteId", "default")
        return f"hermes/audioServer/{siteId}/audioFrame"

    @classmethod
    def get_siteId(cls, topic: str) -> str:
        """Get siteId from a topic"""
        match = re.match(AudioFrame.TOPIC_PATTERN, topic)
        assert match, "Not an audioFrame topic"
        return match.group(1)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AudioFrame.TOPIC_PATTERN, topic) is not None

    @classmethod
    def iter_wav_chunked(
        cls, wav_io: typing.BinaryIO, frames_per_chunk: int
    ) -> typing.Iterable[bytes]:
        """Split single WAV into multiple WAV chunks"""
        with wave.open(wav_io) as in_wav:
            frames_left = in_wav.getnframes()

            while frames_left > 0:
                chunk = in_wav.readframes(frames_per_chunk)
                if not chunk:
                    break

                # Wrap chunk in WAV
                with io.BytesIO() as out_io:
                    out_wav: wave.Wave_write = wave.open(out_io, "wb")
                    with out_wav:
                        out_wav.setframerate(in_wav.getframerate())
                        out_wav.setsampwidth(in_wav.getsampwidth())
                        out_wav.setnchannels(in_wav.getnchannels())
                        out_wav.writeframesraw(chunk)

                    yield out_io.getvalue()

                frames_left -= frames_per_chunk


@attr.s(auto_attribs=True, slots=True)
class AudioPlayBytes(Message):
    """Play WAV sound on specific site."""

    TOPIC_PATTERN = re.compile(r"^hermes/audioServer/([^/]+)/playBytes/([^/]+)$")

    wav_data: bytes

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        siteId = kwargs.get("siteId", "default")
        requestId = kwargs.get("requestId") or str(uuid4())
        return f"hermes/audioServer/{siteId}/playBytes/{requestId}"

    @classmethod
    def get_siteId(cls, topic: str) -> str:
        """Get siteId from a topic"""
        match = re.match(AudioPlayBytes.TOPIC_PATTERN, topic)
        assert match, "Not a playBytes topic"
        return match.group(1)

    @classmethod
    def get_requestId(cls, topic: str) -> str:
        """Get requestId from a topic"""
        match = re.match(AudioPlayBytes.TOPIC_PATTERN, topic)
        assert match, "Not a playBytes topic"
        return match.group(2)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AudioPlayBytes.TOPIC_PATTERN, topic) is not None


@attr.s(auto_attribs=True, slots=True)
class AudioPlayFinished(Message):
    """Sent when audio service has finished playing a sound."""

    TOPIC_PATTERN = re.compile(r"^hermes/audioServer/([^/]+)/playFinished$")

    id: str = ""
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        siteId = kwargs.get("siteId", "default")
        return f"hermes/audioServer/{siteId}/playFinished"

    @classmethod
    def get_siteId(cls, topic: str) -> str:
        """Get siteId from a topic"""
        match = re.match(AudioPlayFinished.TOPIC_PATTERN, topic)
        assert match, "Not a playFinished topic"
        return match.group(1)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AudioPlayFinished.TOPIC_PATTERN, topic) is not None


# -----------------------------------------------------------------------------


class AudioDeviceMode(str, Enum):
    """Input/output mode of an audio device"""

    INPUT = "input"
    OUTPUT = "output"


@attr.s(auto_attribs=True, slots=True)
class AudioDevice:
    """Description of an audio device."""

    mode: AudioDeviceMode
    id: str
    name: str
    description: str
    working: typing.Optional[bool] = attr.ib(default=None)


@attr.s(auto_attribs=True, slots=True)
class AudioGetDevices(Message):
    """Get details for audio input devices."""

    modes: typing.List[AudioDeviceMode]
    id: str = ""
    siteId: str = "default"
    test: bool = False

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        return "rhasspy/audioServer/getDevices"


@attr.s(auto_attribs=True, slots=True)
class AudioDevices(Message):
    """Response to getDevices."""

    id: str = ""
    siteId: str = "default"
    devices: typing.List[AudioDevice] = attr.Factory(list)

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        return "rhasspy/audioServer/devices"

    @classmethod
    def from_dict(cls, message_dict: typing.Dict[str, typing.Any]):
        """Construct message from dictionary."""
        device_dicts = message_dict.pop("devices", [])
        devices = [AudioDevice(**d) for d in device_dicts]

        return AudioDevices(**message_dict, devices=devices)  # type: ignore
