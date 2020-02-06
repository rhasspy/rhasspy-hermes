"""Messages for hermes/hotword"""
import re

import attr

from .base import Message


@attr.s(auto_attribs=True, slots=True)
class HotwordToggleOn(Message):
    """Activate the wake word component."""

    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/hotword/toggleOn"


@attr.s(auto_attribs=True, slots=True)
class HotwordToggleOff(Message):
    """Deactivate the wake word component."""

    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/hotword/toggleOff"


@attr.s(auto_attribs=True, slots=True)
class HotwordDetected(Message):
    """Wake word component has detected a specific wake word."""

    TOPIC_PATTERN = re.compile(r"^hermes/hotword/([^/]+)/detected$")

    modelId: str
    modelVersion: str
    modelType: str
    currentSensitivity: float
    siteId: str = "default"

    # Rhasspy specific
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message (wakewordId)."""
        wakewordId = kwargs.get("wakewordId", "default")
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


@attr.s(auto_attribs=True)
class HotwordError(Message):
    """Error from Hotword component."""

    error: str
    context: str = ""
    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get Hermes topic"""
        return "hermes/error/hotword"
