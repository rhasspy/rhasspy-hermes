"""Messages for hermes/hotword"""
import re
import typing
from dataclasses import dataclass
from enum import Enum

from dataclasses_json import LetterCase, dataclass_json

from .base import Message


class HotwordToggleReason(str, Enum):
    """Reason for hotword toggle on/off."""

    UNKNOWN = ""
    DIALOGUE_SESSION = "dialogueSession"
    PLAY_AUDIO = "playAudio"
    TTS_SAY = "ttsSay"


@dataclass
class HotwordToggleOn(Message):
    """Activate the wake word component."""

    site_id: str = "default"

    # ------------
    # Rhasspy only
    # ------------

    reason: HotwordToggleReason = HotwordToggleReason.UNKNOWN

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/hotword/toggleOn"


@dataclass
class HotwordToggleOff(Message):
    """Deactivate the wake word component."""

    site_id: str = "default"

    # ------------
    # Rhasspy only
    # ------------

    reason: HotwordToggleReason = HotwordToggleReason.UNKNOWN

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/hotword/toggleOff"


@dataclass
class HotwordDetected(Message):
    """Wake word component has detected a specific wake word."""

    TOPIC_PATTERN = re.compile(r"^hermes/hotword/([^/]+)/detected$")

    model_id: str
    model_version: str = ""
    model_type: str = "personal"
    current_sensitivity: float = 1.0
    site_id: str = "default"

    # Rhasspy specific
    session_id: str = ""
    send_audio_captured: typing.Optional[bool] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message (wakeword_id)."""
        wakeword_id = kwargs.get("wakeword_id", "+")
        return f"hermes/hotword/{wakeword_id}/detected"

    @classmethod
    def get_wakeword_id(cls, topic: str) -> str:
        """Get wakeword_id from a topic"""
        match = re.match(HotwordDetected.TOPIC_PATTERN, topic)
        assert match, "Not a detected topic"
        return match.group(1)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(HotwordDetected.TOPIC_PATTERN, topic) is not None


# -----------------------------------------------------------------------------
# Rhasspy Only Messages
# -----------------------------------------------------------------------------


@dataclass
class HotwordError(Message):
    """Error from Hotword component.

    Attributes
    ----------
    error: str
        A description of the error that occurred

    site_id: str = "default"
        The id of the site where the error occurred

    context: Optional[str] = None
        Additional information on the context in which the error occurred

    session_id: Optional[str] = None
        The id of the session, if there is an active session
    """

    error: str
    site_id: str = "default"
    context: typing.Optional[str] = None
    session_id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "hermes/error/hotword"


@dataclass
class GetHotwords(Message):
    """Request to list available hotwords."""

    site_id: str = "default"
    id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/hotword/getHotwords"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Hotword:
    """Description of a single hotword (used in hotwords message)."""

    # Unique ID of hotword model
    model_id: str

    # Actual words used to activate hotword
    modelWords: str

    # Model version
    model_version: str = ""

    # Model type (personal, unversal)
    model_type: str = "personal"


@dataclass
class Hotwords(Message):
    """Response to getHotwords."""

    models: typing.Dict[str, Hotword]
    site_id: str = "default"
    id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "rhasspy/hotword/hotwords"
