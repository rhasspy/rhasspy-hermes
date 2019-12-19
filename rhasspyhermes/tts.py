"""Messages for hermes/tts"""
import attr

from .base import Message


@attr.s
class TtsSay(Message):
    """Send text to be spoken by the text to speech component."""

    text: str = attr.ib()
    lang: str = attr.ib(default="")
    id: str = attr.ib(default="")
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/tts/say"


@attr.s
class TtsSayFinished(Message):
    """Sent when text to speech component has finished speaking some text."""

    id: str = attr.ib(default="")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/tts/sayFinished"
