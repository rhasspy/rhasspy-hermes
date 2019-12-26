"""Messages for hermes/hotword"""
import re

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

    TOPIC_PATTERN = re.compile(r"^hermes/hotword/([^/]+)/detected$")

    modelId: str = attr.ib()
    modelVersion: str = attr.ib()
    modelType: str = attr.ib()
    currentSensitivity: float = attr.ib()
    siteId: str = attr.ib(default="default")

    @classmethod
    def topic(cls, **kwargs) -> str:
        wakewordId = kwargs["wakewordId"]
        return f"hermes/hotword/{wakewordId}/detected"

    @classmethod
    def get_wakewordId(cls, topic: str) -> str:
        """Get wakewordId from a topic"""
        match = re.match(HotwordDetected.TOPIC_PATTERN, topic)
        assert match, "Not a detected topic"
        return match.group(1)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(HotwordDetected.TOPIC_PATTERN, topic) is not None
