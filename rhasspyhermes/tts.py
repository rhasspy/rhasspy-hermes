"""Messages for hermes/tts"""
import attr

from .base import Message


@attr.s(auto_attribs=True, slots=True)
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


@attr.s(auto_attribs=True, slots=True)
class TtsSayFinished(Message):
    """Sent when text to speech component has finished speaking some text."""

    id: str = ""
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/tts/sayFinished"
