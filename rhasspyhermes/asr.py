import typing

import attr

from .base import Message


@attr.s
class AsrToggleOn(Message):
    """Activate the ASR component."""

    TOPIC = "hermes/asr/toggleOn"

    siteId: str = attr.ib(default="default")

    def topic(self, *args, **kwargs) -> str:
        return AsrToggleOn.TOPIC


@attr.s
class AsrToggleOff(Message):
    """Deactivate the ASR component."""

    TOPIC = "hermes/asr/toggleOff"

    siteId: str = attr.ib(default="default")

    def topic(self, *args, **kwargs) -> str:
        return AsrToggleOff.TOPIC


@attr.s
class AsrStartListening(Message):
    """Tell the ASR component to start listening."""

    TOPIC = "hermes/asr/startListening"

    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    def topic(self, *args, **kwargs) -> str:
        return AsrStartListening.TOPIC


@attr.s
class AsrStopListening(Message):
    """Tell the ASR component to stop listening."""

    TOPIC = "hermes/asr/stopListening"

    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    def topic(self, *args, **kwargs) -> str:
        return AsrStopListening.TOPIC


@attr.s
class AsrTextCaptured(Message):
    """Full ASR transcription results."""

    TOPIC = "hermes/asr/textCaptured"

    text: str = attr.ib()
    likelihood: float = attr.ib()
    seconds: float = attr.ib()

    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    def topic(self, *args, **kwargs) -> str:
        return AsrTextCaptured.TOPIC
