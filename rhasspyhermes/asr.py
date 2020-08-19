"""Messages for automated speech recognition."""
import re
import typing
from dataclasses import dataclass
from enum import Enum

from .base import Message
from .nlu import AsrToken


class AsrToggleReason(str, Enum):
    """Reason for ASR toggle on/off.

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
class AsrToggleOn(Message):
    """Activate the ASR component.

    Attributes
    ----------
    site_id: str = "default"
        The id of the site where ASR should be turned on

    reason: AsrToggleReason = UNKNOWN
        Reason why ASR was toggled on
    """

    site_id: str = "default"

    # ------------
    # Rhasspy only
    # ------------

    reason: AsrToggleReason = AsrToggleReason.UNKNOWN

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/asr/toggleOn"


@dataclass
class AsrToggleOff(Message):
    """Deactivate the ASR component.

    Attributes
    ----------
    site_id: str = "default"
        The id of the site where ASR should be turned off

    reason: AsrToggleReason = UNKNOWN
        Reason why ASR was toggled off
    """

    site_id: str = "default"

    # ------------
    # Rhasspy only
    # ------------

    reason: AsrToggleReason = AsrToggleReason.UNKNOWN

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/asr/toggleOff"


@dataclass
class AsrStartListening(Message):
    """Tell the ASR component to start listening.

    Attributes
    ----------
    site_id: str = "default"
        The site that must be listened too

    session_id: Optional[str] = None
        An optional session id if there is a related session

    stop_on_silence: bool = True
        If true, ASR should automatically detect end of voice command

    send_audio_captured: bool = False
        If true, ASR emits asr/audioCaptured message with recorded audio

    wakeword_id: Optional[str] = None
        Optional id of wakeword used to activate ASR

    intent_filter: Optional[List[str]] = None
        A list of intent names to restrict the ASR on

    lang: Optional[str] = None
        Language of the incoming audio stream.
        Typically set in hotword detected or dialogue startSession messages.
    """

    site_id: str = "default"
    session_id: typing.Optional[str] = None
    lang: typing.Optional[str] = None

    # ------------
    # Rhasspy only
    # ------------

    stop_on_silence: bool = True
    send_audio_captured: bool = False
    wakeword_id: typing.Optional[str] = None
    intent_filter: typing.Optional[typing.List[str]] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/asr/startListening"


@dataclass
class AsrStopListening(Message):
    """Tell the ASR component to stop listening.

    Attributes
    ----------
    site_id: str = "default"
        The id of the site where the ASR should stop listening

    session_id: Optional[str] = None
        The id of the session, if there is an active session
    """

    site_id: str = "default"
    session_id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/asr/stopListening"


@dataclass
class AsrTextCaptured(Message):
    """Full ASR transcription results.

    Attributes
    ----------
    text: str
        The text captured

    likelihood: float
        The likelihood of the capture

    seconds: float
        The duration it took to do the processing

    site_id: str = "default"
        The id of the site where the text was captured

    session_id: Optional[str] = None
        The id of the session, if there is an active session

    wakeword_id: Optional[str] = None
        Optional id of wakeword used to activate ASR

    asr_tokens: Optional[List[List[AsrToken]]] = None
        Structured description of the tokens the ASR captured on for this intent

    lang: Optional[str] = None
        Language of the session
    """

    text: str
    likelihood: float
    seconds: float

    site_id: str = "default"
    session_id: typing.Optional[str] = None

    # ------------
    # Rhasspy only
    # ------------

    wakeword_id: typing.Optional[str] = None
    asr_tokens: typing.Optional[typing.List[typing.List[AsrToken]]] = None
    lang: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/asr/textCaptured"


# ----------------------------------------------------------------------------
# Rhasspy-only Messages
# ----------------------------------------------------------------------------


@dataclass
class AsrError(Message):
    """Error from ASR component.

    Attributes
    ----------
    site_id: str = "default"
        The id of the site where the error occurred

    error: str
        A description of the error that occurred

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
        """Get MQTT topic for this message type."""
        return "hermes/error/asr"


@dataclass
class AsrTrain(Message):
    """Request to retrain ASR from intent graph.

    Attributes
    ----------
    graph_path: str
        Path to the graph file

    id: Optional[str] = None
        Unique id for training request

    graph_format: typing.Optional[str] = None
        Optional format of the graph file
    """

    TOPIC_PATTERN = re.compile(r"^rhasspy/asr/([^/]+)/train$")

    graph_path: str
    id: typing.Optional[str] = None
    graph_format: typing.Optional[str] = None
    sentences: typing.Optional[typing.Dict[str, str]] = None
    slots: typing.Optional[typing.Dict[str, typing.List[str]]] = None

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        site_id = kwargs.get("site_id", "+")
        return f"rhasspy/asr/{site_id}/train"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AsrTrain.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from a topic"""
        match = re.match(AsrTrain.TOPIC_PATTERN, topic)
        assert match, "Not a train topic"
        return match.group(1)


@dataclass
class AsrTrainSuccess(Message):
    """Result from successful training.

    Attributes
    ----------

    id: Optional[str] = None
        Unique id from training request
    """

    TOPIC_PATTERN = re.compile(r"^rhasspy/asr/([^/]+)/trainSuccess$")

    id: typing.Optional[str] = None

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        site_id = kwargs.get("site_id", "+")
        return f"rhasspy/asr/{site_id}/trainSuccess"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AsrTrainSuccess.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from a topic"""
        match = re.match(AsrTrainSuccess.TOPIC_PATTERN, topic)
        assert match, "Not a trainSuccess topic"
        return match.group(1)


@dataclass
class AsrAudioCaptured(Message):
    """Audio captured from ASR session.

    Attributes
    ----------
    wav_bytes: bytes
        Captured audio in WAV format
    """

    TOPIC_PATTERN = re.compile(r"^rhasspy/asr/([^/]+)/([^/]+)/audioCaptured$")

    wav_bytes: bytes

    def payload(self) -> typing.Union[str, bytes]:
        """Get binary/string for this message."""
        return self.wav_bytes

    @classmethod
    def is_binary_payload(cls) -> bool:
        """True if payload is not JSON."""
        return True

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic."""
        return True

    @classmethod
    def is_session_in_topic(cls) -> bool:
        """True if session id is in topic."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        site_id = kwargs.get("site_id", "+")
        session_id = kwargs.get("site_id", "+")
        return f"rhasspy/asr/{site_id}/{session_id}/audioCaptured"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AsrAudioCaptured.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from a topic"""
        match = re.match(AsrAudioCaptured.TOPIC_PATTERN, topic)
        assert match, "Not an audioCaptured topic"
        return match.group(1)

    @classmethod
    def get_session_id(cls, topic: str) -> typing.Optional[str]:
        """Get session id from a topic"""
        match = re.match(AsrAudioCaptured.TOPIC_PATTERN, topic)
        assert match, "Not an audioCaptured topic"
        return match.group(2)
