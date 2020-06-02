"""Messages for hermes/hotword"""
import re
import typing
from dataclasses import dataclass
from enum import Enum

from dataclasses_json import LetterCase, dataclass_json

from .base import Message


class HotwordToggleReason(str, Enum):
    """Reason for hotword toggle on/off.

    Values
    ------
    UNKNOWN
        Overrides all other reasons

    DIALOGUE_SESSION
        Dialogue session is active

    PLAY_AUDIO
        Audio is currently playing

    TTS_SAY
        Text to speech system is currently speaking
    """

    UNKNOWN = ""
    DIALOGUE_SESSION = "dialogueSession"
    PLAY_AUDIO = "playAudio"
    TTS_SAY = "ttsSay"


@dataclass
class HotwordToggleOn(Message):
    """Activate the wake word component.

    Attributes
    ----------
    site_id: str = "default"
        Id of the site where the hotword component should be enabled

    reason: HotwordToggleReason = UNKNOWN
        Reason for enabling the hotword component
    """

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
    """Deactivate the wake word component.

    Attributes
    ----------
    site_id: str = "default"
        Id of the site where the hotword component should be disabled

    reason: HotwordToggleReason = UNKNOWN
        Reason for disabling the hotword component
    """

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
    """Wake word component has detected a specific wake word.

    Attributes
    ----------
    model_id: str
        The id of the model that triggered the wake word

    model_version: str = ""
        The version of the model

    model_type: str = "personal"
        The type of the model. Possible values: universal or personal

    current_sensitivity: float = 1.0
        The sensitivity configured in the model at the time of the detection

    site_id: str = "default"
        The id of the site where the wake word was detected

    session_id: Optional[str] = None
        The desired id of the dialogue session created after detection.
        Leave empty to have one auto-generated.

    send_audio_captured: Optional[bool] = None
        True if audio captured from ASR should be emitted on
        rhasspy/asr/{site_id}/{session_id}/audioCaptured

    lang: Optional[str] = None
        Language of the detected wake word.
        Copied by dialogue manager into subsequent ASR, NLU messages.
    """

    TOPIC_PATTERN = re.compile(r"^hermes/hotword/([^/]+)/detected$")

    model_id: str
    model_version: str = ""
    model_type: str = "personal"
    current_sensitivity: float = 1.0
    site_id: str = "default"

    # ------------
    # Rhasspy only
    # ------------

    session_id: typing.Optional[str] = None
    send_audio_captured: typing.Optional[bool] = None
    lang: typing.Optional[str] = None

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
    """Request to list available hotwords.

    Attributes
    ----------
    site_id: str = "default"
        Id of site where hotword component exists

    id: typing.Optional[str] = None
        Unique id passed to response
    """

    site_id: str = "default"
    id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/hotword/getHotwords"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Hotword:
    """Description of a single hotword.

    Attributes
    ----------
    model_id: str
        Unique ID of hotword model

    model_words: str
        Actual words used to activate hotword

    model_version: str = ""
        Model version

    model_type: str = "personal"
        Model type (personal, unversal)
    """

    model_id: str
    model_words: str
    model_version: str = ""
    model_type: str = "personal"


@dataclass
class Hotwords(Message):
    """Response to getHotwords.

    Attributes
    ----------
    models: typing.List[Hotword]
        List of available hotwords

    site_id: str = "default"
        Id of site where hotwords were requested

    id: typing.Optional[str] = None
        Unique id passed from request
    """

    models: typing.List[Hotword]
    site_id: str = "default"
    id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "rhasspy/hotword/hotwords"
