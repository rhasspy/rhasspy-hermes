"""Messages for hermes/hotword"""
import re
import typing
from dataclasses import dataclass

from .base import Message


@dataclass
class HotwordToggleOn(Message):
    """Activate the wake word component."""

    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/hotword/toggleOn"


@dataclass
class HotwordToggleOff(Message):
    """Deactivate the wake word component."""

    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/hotword/toggleOff"


@dataclass
class HotwordDetected(Message):
    """Wake word component has detected a specific wake word."""

    TOPIC_PATTERN = re.compile(r"^hermes/hotword/([^/]+)/detected$")

    modelId: str
    modelVersion: str = ""
    modelType: str = "personal"
    currentSensitivity: float = 1.0
    siteId: str = "default"

    # Rhasspy specific
    sessionId: str = ""
    sendAudioCaptured: typing.Optional[bool] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message (wakewordId)."""
        wakewordId = kwargs.get("wakewordId", "+")
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


# -----------------------------------------------------------------------------
# Rhasspy Only
# -----------------------------------------------------------------------------


@dataclass
class HotwordError(Message):
    """Error from Hotword component."""

    error: str
    context: str = ""
    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get Hermes topic"""
        return "hermes/error/hotword"


@dataclass
class GetHotwords(Message):
    """Request to list available hotwords."""

    id: str = ""
    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/hotword/getHotwords"


@dataclass
class Hotword:
    """Description of a single hotword (used in hotwords message)."""

    # Unique ID of hotword model
    modelId: str

    # Actual words used to activate hotword
    modelWords: str

    modelVersion: str = ""
    modelType: str = "personal"


@dataclass
class Hotwords(Message):
    """Response to getHotwords."""

    models: typing.Dict[str, Hotword] = field(default_factory=dict)
    id: str = ""
    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/hotword/hotwords"
