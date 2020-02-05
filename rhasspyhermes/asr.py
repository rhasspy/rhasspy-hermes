"""Messages for hermes/asr"""
import re
import typing

import attr

from .base import Message


@attr.s(auto_attribs=True, slots=True)
class AsrToggleOn(Message):
    """Activate the ASR component."""

    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/toggleOn"


@attr.s(auto_attribs=True, slots=True)
class AsrToggleOff(Message):
    """Deactivate the ASR component."""

    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/toggleOff"


@attr.s(auto_attribs=True, slots=True)
class AsrStartListening(Message):
    """Tell the ASR component to start listening."""

    siteId: str = "default"
    sessionId: str = ""

    # Rhasspy-specific
    stopOnSilence: bool = True

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/startListening"


@attr.s(auto_attribs=True, slots=True)
class AsrStopListening(Message):
    """Tell the ASR component to stop listening."""

    siteId: str = "default"
    sessionId: str = ""

    # Rhasspy-specific
    sendAudioCaptured: bool = False

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/asr/stopListening"


@attr.s(auto_attribs=True, slots=True)
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


# ----------------------------------------------------------------------------
# Rhasspy-specific Messages
# ----------------------------------------------------------------------------


@attr.s(auto_attribs=True, slots=True)
class AsrError(Message):
    """Error from ASR component."""

    error: str
    context: str = ""
    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/error/asr"


@attr.s(auto_attribs=True, slots=True)
class AsrTrain(Message):
    """Request to retrain from intent graph"""

    TOPIC_PATTERN = re.compile(r"^rhasspy/asr/([^/]+)/train$")

    id: str
    graph_dict: typing.Dict[str, typing.Any]

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        siteId = kwargs.get("siteId", "default")
        return f"rhasspy/asr/{siteId}/train"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AsrTrain.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_siteId(cls, topic: str) -> str:
        """Get siteId from a topic"""
        match = re.match(AsrTrain.TOPIC_PATTERN, topic)
        assert match, "Not a train topic"
        return match.group(1)


@attr.s(auto_attribs=True, slots=True)
class AsrTrainSuccess(Message):
    """Result from successful training"""

    TOPIC_PATTERN = re.compile(r"^rhasspy/asr/([^/]+)/trainSuccess$")

    id: str

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        siteId = kwargs.get("siteId", "default")
        return f"rhasspy/asr/{siteId}/trainSuccess"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AsrTrainSuccess.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_siteId(cls, topic: str) -> str:
        """Get siteId from a topic"""
        match = re.match(AsrTrainSuccess.TOPIC_PATTERN, topic)
        assert match, "Not a trainSuccess topic"
        return match.group(1)


@attr.s(auto_attribs=True, slots=True)
class AsrAudioCaptured(Message):
    """Audio captured from ASR session."""

    TOPIC_PATTERN = re.compile(r"^rhasspy/asr/([^/]+)/([^/]+)/audioCaptured$")

    wav_bytes: bytes

    @classmethod
    def topic(cls, **kwargs) -> str:
        siteId = kwargs.get("siteId", "default")
        sessionId = kwargs.get("siteId", "")
        return f"hermes/asr/{siteId}/{sessionId}/audioCaptured"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(AsrAudioCaptured.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_siteId(cls, topic: str) -> str:
        """Get siteId from a topic"""
        match = re.match(AsrAudioCaptured.TOPIC_PATTERN, topic)
        assert match, "Not an audioCaptured topic"
        return match.group(1)

    @classmethod
    def get_sessionId(cls, topic: str) -> str:
        """Get sessionId from a topic"""
        match = re.match(AsrAudioCaptured.TOPIC_PATTERN, topic)
        assert match, "Not an audioCaptured topic"
        return match.group(2)
