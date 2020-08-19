"""Messages for audio recording and playback."""
import audioop
import io
import re
import time
import typing
import wave
from dataclasses import dataclass
from enum import Enum

from .base import Message


@dataclass
class AudioFrame(Message):
    """Recorded frame of audio.

    Attributes
    ----------
    wav_bytes: bytes
        Recorded audio frame in WAV format
    """

    TOPIC_PATTERN = re.compile(r"^hermes/audioServer/([^/]+)/audioFrame$")

    wav_bytes: bytes

    def payload(self) -> typing.Union[str, bytes]:
        """Get binary/string for this message."""
        return self.wav_bytes

    @classmethod
    def is_binary_payload(cls) -> bool:
        """True if payload is not JSON."""
        return True

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        site_id = kwargs.get("site_id", "+")
        return f"hermes/audioServer/{site_id}/audioFrame"

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from a topic"""
        match = re.match(AudioFrame.TOPIC_PATTERN, topic)
        assert match, "Not an audioFrame topic"
        return match.group(1)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AudioFrame.TOPIC_PATTERN, topic) is not None

    @classmethod
    def iter_wav_chunked(
        cls, wav_io: typing.BinaryIO, frames_per_chunk: int, live_delay: bool = False
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
                        out_wav.writeframes(chunk)

                    wav_bytes = out_io.getvalue()
                    yield wav_bytes

                    if live_delay:
                        time.sleep(AudioFrame.get_wav_duration(wav_bytes))

                frames_left -= frames_per_chunk

    @classmethod
    def get_wav_duration(cls, wav_bytes: bytes) -> float:
        """Return the real-time duration of a WAV file"""
        with io.BytesIO(wav_bytes) as wav_buffer:
            wav_file: wave.Wave_read = wave.open(wav_buffer, "rb")
            with wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                return frames / float(rate)


@dataclass
class AudioPlayBytes(Message):
    """Play WAV sound on specific site.

    Attributes
    ----------
    wav_bytes: bytes
        Audio to play in WAV format
    """

    TOPIC_PATTERN = re.compile(r"^hermes/audioServer/([^/]+)/playBytes/([^/]+)$")

    wav_bytes: bytes

    def payload(self) -> typing.Union[str, bytes]:
        """Get binary/string for this message."""
        return self.wav_bytes

    @classmethod
    def is_binary_payload(cls) -> bool:
        """True if payload is not JSON."""
        return True

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        site_id = kwargs.get("site_id", "+")
        request_id = kwargs.get("request_id", "#")
        return f"hermes/audioServer/{site_id}/playBytes/{request_id}"

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from a topic"""
        match = re.match(AudioPlayBytes.TOPIC_PATTERN, topic)
        assert match, "Not a playBytes topic"
        return match.group(1)

    @classmethod
    def get_request_id(cls, topic: str) -> str:
        """Get request id from a topic"""
        match = re.match(AudioPlayBytes.TOPIC_PATTERN, topic)
        assert match, "Not a playBytes topic"
        return match.group(2)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AudioPlayBytes.TOPIC_PATTERN, topic) is not None


@dataclass
class AudioPlayFinished(Message):
    """Sent when audio service has finished playing a sound.

    Attributes
    ----------
    id: str : Optional[str] = None
        Request identifier for the request passed from playBytes topic

    session_id: Optional[str] = None
        The id of the session, if there is an active session
    """

    TOPIC_PATTERN = re.compile(r"^hermes/audioServer/([^/]+)/playFinished$")

    id: typing.Optional[str] = None
    session_id: typing.Optional[str] = None

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        site_id = kwargs.get("site_id", "+")
        return f"hermes/audioServer/{site_id}/playFinished"

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site_id from a topic"""
        match = re.match(AudioPlayFinished.TOPIC_PATTERN, topic)
        assert match, "Not a playFinished topic"
        return match.group(1)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AudioPlayFinished.TOPIC_PATTERN, topic) is not None


# -----------------------------------------------------------------------------
# Rhasspy Only
# -----------------------------------------------------------------------------


class AudioDeviceMode(str, Enum):
    """Mode of an audio device.

    Values
    ------
    INPUT
        Recording device

    OUTPUT
        Playback device
    """

    INPUT = "input"
    OUTPUT = "output"


@dataclass
class AudioDevice:
    """Description of an audio device.

    Attributes
    ----------
    mode: AudioDeviceMode
        Recording or playback device

    id: str
        Unique id of audio device

    name: Optional[str] = None
        Optional human-readable name of audio device

    description: Optional[str] = None
        Optional human-readable description of audio device

    working: Optional[bool] = None
        Status of audio device if tested
    """

    mode: AudioDeviceMode
    id: str
    name: typing.Optional[str] = None
    description: typing.Optional[str] = None
    working: typing.Optional[bool] = None


@dataclass
class AudioGetDevices(Message):
    """Get details for available audio devices.

    Attributes
    ----------
    modes: List[AudioDeviceMode]
        Device types to get information about

    id: Optional[str] = None
        Unique id to be returned in response

    site_id: str = "default"
        Id of the site where devices are located

    test: bool = False
        True if devices should be tested
    """

    modes: typing.List[AudioDeviceMode]
    site_id: str = "default"
    id: typing.Optional[str] = None
    test: bool = False

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        return "rhasspy/audioServer/getDevices"


@dataclass
class AudioDevices(Message):
    """Response to getDevices.

    Attributes
    ----------
    devices: List[AudioDevice]
        Description of requested device types

    id: Optional[str] = None
        Unique id from request

    site_id: str = "default"
        Id of site where devices are located
    """

    devices: typing.List[AudioDevice]
    site_id: str = "default"
    id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        return "rhasspy/audioServer/devices"


@dataclass
class AudioSessionFrame(Message):
    """Recorded audio frame for a specific session.

    Attributes
    ----------
    wav_bytes: bytes
        Audio frame in WAV format
    """

    TOPIC_PATTERN = re.compile(
        r"^hermes/audioServer/([^/]+)/([^/]+)/audioSessionFrame$"
    )

    wav_bytes: bytes

    def payload(self) -> typing.Union[str, bytes]:
        """Get binary/string for this message."""
        return self.wav_bytes

    @classmethod
    def is_binary_payload(cls) -> bool:
        """True if payload is not JSON."""
        return True

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic."""
        return True

    @classmethod
    def is_session_in_topic(cls) -> bool:
        """True if session id is in topic."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        site_id = kwargs.get("site_id", "+")
        session_id = kwargs.get("session_id", "+")
        return f"hermes/audioServer/{site_id}/{session_id}/audioSessionFrame"

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from a topic"""
        match = re.match(AudioSessionFrame.TOPIC_PATTERN, topic)
        assert match, "Not an audioSessionFrame topic"
        return match.group(1)

    @classmethod
    def get_session_id(cls, topic: str) -> typing.Optional[str]:
        """Get session id from a topic"""
        match = re.match(AudioSessionFrame.TOPIC_PATTERN, topic)
        assert match, "Not an audioSessionFrame topic"
        return match.group(2)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AudioSessionFrame.TOPIC_PATTERN, topic) is not None


@dataclass
class AudioSummary(Message):
    """Summary of recent audio frame(s) for diagnostic purposes.

    debiased_energy: float
        Audio energy computed using get_debiased_energy

    is_speech: typing.Optional[bool] = None
        True/false if VAD detected speech
    """

    TOPIC_PATTERN = re.compile(r"^hermes/audioServer/([^/]+)/audioSummary$")

    debiased_energy: float
    is_speech: typing.Optional[bool] = None

    @classmethod
    def get_debiased_energy(cls, audio_data: bytes) -> float:
        """Compute RMS of debiased audio."""
        # Thanks to the speech_recognition library!
        # https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__init__.py
        energy = -audioop.rms(audio_data, 2)
        energy_bytes = bytes([energy & 0xFF, (energy >> 8) & 0xFF])
        debiased_energy = audioop.rms(
            audioop.add(audio_data, energy_bytes * (len(audio_data) // 2), 2), 2
        )

        # Probably actually audio if > 30
        return debiased_energy

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        site_id = kwargs.get("site_id", "+")
        return f"hermes/audioServer/{site_id}/audioSummary"

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from a topic"""
        match = re.match(AudioSummary.TOPIC_PATTERN, topic)
        assert match, "Not an audioSummary topic"
        return match.group(1)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AudioSummary.TOPIC_PATTERN, topic) is not None


@dataclass
class SummaryToggleOn(Message):
    """Activate sending of audio summaries.

    Attributes
    ----------
    site_id: str = "default"
        Id of site where audio is being recorded
    """

    site_id: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/audioServer/toggleSummaryOn"


@dataclass
class SummaryToggleOff(Message):
    """Deactivate sending of audio summaries.

    Attributes
    ----------
    site_id: str = "default"
        Id of site where audio is being recorded
    """

    site_id: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/audioServer/toggleSummaryOff"


@dataclass
class AudioToggleOn(Message):
    """Activate audio output system.

    Attributes
    ----------
    site_id: str = "default"
        Id of site where audio should be turned off
    """

    site_id: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/audioServer/toggleOn"


@dataclass
class AudioToggleOff(Message):
    """Deactivate audio output system.

    Attributes
    ----------
    site_id: str = "default"
        Id of site where audio should be turned on
    """

    site_id: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/audioServer/toggleOff"


@dataclass
class AudioRecordError(Message):
    """Error from audio input component.

    Attributes
    ----------
    error: str
        A description of the error that occurred

    site_id: str = "default"
        The id of the site where the error occurred

    context: Optional[str] = None
        Additional information on the context in which the error occurred

    session_id: Optional[str] = None
        The id of the session, if there is an active session
    """

    error: str
    site_id: str = "default"
    context: typing.Optional[str] = None
    session_id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/error/audioServer/record"


@dataclass
class AudioPlayError(Message):
    """Error from audio output component.

    Attributes
    ----------
    error: str
        A description of the error that occurred

    site_id: str = "default"
        The id of the site where the error occurred

    context: Optional[str] = None
        Additional information on the context in which the error occurred

    session_id: Optional[str] = None
        The id of the session, if there is an active session
    """

    error: str
    site_id: str = "default"
    context: typing.Optional[str] = None
    session_id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/error/audioServer/play"
