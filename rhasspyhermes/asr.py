"""Messages for hermes/asr"""
import attr

from .base import Message


@attr.s
class AsrToggleOn(Message):
    """Activate the ASR component."""

    siteId: str = attr.ib(default="default")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/toggleOn"


@attr.s
class AsrToggleOff(Message):
    """Deactivate the ASR component."""

    siteId: str = attr.ib(default="default")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/toggleOff"


@attr.s
class AsrStartListening(Message):
    """Tell the ASR component to start listening."""

    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/startListening"


@attr.s
class AsrStopListening(Message):
    """Tell the ASR component to stop listening."""

    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/stopListening"


@attr.s
class AsrTextCaptured(Message):
    """Full ASR transcription results."""

    text: str = attr.ib()
    likelihood: float = attr.ib()
    seconds: float = attr.ib()

    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/textCaptured"
