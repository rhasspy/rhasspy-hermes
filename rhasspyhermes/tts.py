"""Messages for text to speech."""
import typing
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

from .base import Message


@dataclass
class TtsSay(Message):
    """Send text to be spoken by the text to speech component."""

    text: str
    site_id: str = "default"
    lang: typing.Optional[str] = None
    id: typing.Optional[str] = None
    session_id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/tts/say"


@dataclass
class TtsSayFinished(Message):
    """Sent when text to speech component has finished speaking some text."""

    site_id: str = "default"
    id: typing.Optional[str] = None
    session_id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/tts/sayFinished"


# -----------------------------------------------------------------------------
# Rhasspy Only
# -----------------------------------------------------------------------------


@dataclass
class GetVoices(Message):
    """Get available voices for text to speech system."""

    id: typing.Optional[str] = None
    site_id: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "rhasspy/tts/getVoices"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Voice:
    """Information about a single TTS voice."""

    voice_id: str
    description: str = ""


@dataclass
class Voices(Message):
    """Response to getVoices."""

    voices: typing.Dict[str, Voice]
    id: typing.Optional[str] = None
    site_id: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "rhasspy/tts/voices"


@dataclass
class TtsError(Message):
    """Error from TTS component.


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
        return "hermes/error/tts"
