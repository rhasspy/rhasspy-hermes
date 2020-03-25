"""Messages for hermes/tts"""
import typing
from dataclasses import dataclass, field

from .base import Message


@dataclass
class TtsSay(Message):
    """Send text to be spoken by the text to speech component."""

    text: str
    lang: str = ""
    id: str = ""
    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/tts/say"


@dataclass
class TtsSayFinished(Message):
    """Sent when text to speech component has finished speaking some text."""

    id: str = ""
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/tts/sayFinished"


# -----------------------------------------------------------------------------
# Rhasspy Only
# -----------------------------------------------------------------------------


@dataclass
class GetVoices(Message):
    """Get available voices for text to speech system."""

    id: str = ""
    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "rhasspy/tts/getVoices"


@dataclass
class Voice:
    """Information about a single TTS voice."""

    voiceId: str
    description: str = ""


@dataclass
class Voices(Message):
    """Response to getVoices."""

    voices: typing.Dict[str, Voice] = field(defaultfactory=dict)
    id: str = ""
    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "rhasspy/tts/voices"
