"""Messages for text to speech."""
import typing
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

from .base import Message


@dataclass
class TtsSay(Message):
    """Send text to be spoken by the text to speech component.

    Attributes
    ----------
    text: str
        The text to be spoken

    site_id: str = "default"
        The id of the site where the text should be spoken

    lang: Optional[str] = None
        The language code to use when saying the text

    id: Optional[str] = None
        A request identifier. If provided, it will be passed back in the
        response.

    session_id: Optional[str] = None
        The id of the session, if there is an active session
    """

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
    """Response when text to speech component has finished speaking.

    Attributes
    ----------
    site_id: str = "default"
        The id of the site where the text was spoken

    id: Optional[str] = None
        Identifier from the request

    session_id: Optional[str] = None
        The id of the session, if there is an active session
    """

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
    """Get available voices for text to speech system.

    Attributes
    ----------
    id: typing.Optional[str] = None
        Unique identifier passed to response

    site_id: str = "default"
        Id of site to request voices from
    """

    id: typing.Optional[str] = None
    site_id: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "rhasspy/tts/getVoices"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Voice:
    """Information about a single TTS voice.

    Attributes
    ----------
    voice_id: str
        Unique identifier for voice

    description: Optional[str] = None
        Human-readable description of voice
    """

    voice_id: str
    description: typing.Optional[str] = None


@dataclass
class Voices(Message):
    """Response to getVoices.

    Attributes
    ----------
    voices: List[ Voice]
        List of available voices

    id: Optional[str] = None
        Unique identifier from request

    site_id: str = "default"
        Id of site where voices were requested
    """

    voices: typing.List[Voice]
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
