"""Messages for hermes/hotword"""
import attr

from .base import Message


@attr.s
class HotwordToggleOn(Message):
    """Activate the wake word component."""

    siteId: str = attr.ib(default="default")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/hotword/toggleOn"


@attr.s
class HotwordToggleOff(Message):
    """Deactivate the wake word component."""

    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/hotword/toggleOff"


@attr.s
class HotwordDetected(Message):
    """Wake word component has detected a specific wake word."""

    modelId: str = attr.ib()
    modelVersion: str = attr.ib()
    modelType: str = attr.ib()
    currentSensitivity: float = attr.ib()
    siteId: str = attr.ib(default="default")

    @classmethod
    def topic(cls, **kwargs) -> str:
        wakeword_id = kwargs["wakeword_id"]
        return f"hermes/hotword/{wakeword_id}/detected"
