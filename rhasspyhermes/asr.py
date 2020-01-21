"""Messages for hermes/asr"""
import attr

from .base import Message


@attr.s(auto_attribs=True)
class AsrToggleOn(Message):
    """Activate the ASR component."""

    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/toggleOn"


@attr.s(auto_attribs=True)
class AsrToggleOff(Message):
    """Deactivate the ASR component."""

    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/toggleOff"


@attr.s(auto_attribs=True)
class AsrStartListening(Message):
    """Tell the ASR component to start listening."""

    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/startListening"


@attr.s(auto_attribs=True)
class AsrStopListening(Message):
    """Tell the ASR component to stop listening."""

    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/stopListening"


@attr.s(auto_attribs=True)
class AsrTextCaptured(Message):
    """Full ASR transcription results."""

    text: str
    likelihood: float
    seconds: float

    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/textCaptured"
