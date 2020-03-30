"""Messages for hermes/nlu"""
import re
import typing
from dataclasses import dataclass, field

from .base import Message
from .intent import Intent, Slot


@dataclass
class NluQuery(Message):
    """Send text to the NLU component."""

    input: str
    intentFilter: typing.Optional[typing.List[str]] = None
    id: str = ""
    siteId: str = "default"
    sessionId: str = ""

    # Rhasspy only
    wakewordId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/nlu/query"


@dataclass
class NluIntentParsed(Message):
    """Intent successfully parsed."""

    input: str
    intent: Intent
    slots: typing.List[Slot] = field(default_factory=list)
    id: str = ""
    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        return f"hermes/nlu/intentParsed"


@dataclass
class NluIntent(Message):
    """Intent recognized."""

    TOPIC_PATTERN = re.compile(r"^hermes/intent/([^/]+)$")

    input: str
    intent: Intent
    slots: typing.List[Slot] = field(default_factory=list)
    id: str = ""
    siteId: str = "default"
    sessionId: str = ""
    customData: str = ""
    asrTokens: typing.List[str] = field(default_factory=list)
    asrConfidence: float = 1.0

    # Rhasspy only
    wakewordId: str = ""
    rawAsrTokens: typing.List[str] = field(default_factory=list)

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message (intentName)."""
        intentName = kwargs.get("intentName", "#")
        return f"hermes/intent/{intentName}"

    @classmethod
    def get_intentName(cls, topic: str) -> str:
        """Get intentName from a topic"""
        match = re.match(NluIntent.TOPIC_PATTERN, topic)
        assert match, "Not an intent topic"
        return match.group(1)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(NluIntent.TOPIC_PATTERN, topic) is not None

    @classmethod
    def from_dict(cls, message_dict: typing.Dict[str, typing.Any]):
        """Construct message from dictionary."""
        message_dict = cls.only_fields(message_dict)
        intent_dict = message_dict.pop("intent", {})
        slot_dicts = message_dict.pop("slots", [])
        message = NluIntent(  # type: ignore
            **message_dict, intent=Intent(**intent_dict)
        )
        message.slots = [Slot.from_dict(s) for s in slot_dicts]

        return message

    @property
    def raw_input(self):
        """Get raw input from ASR."""
        if self.rawAsrTokens:
            return " ".join(self.rawAsrTokens)

        if self.asrTokens:
            return " ".join(self.asrTokens)

        return self.input

    def to_rhasspy_dict(self) -> typing.Dict[str, typing.Any]:
        """Convert to Rhasspy format."""
        return {
            "intent": {
                "name": self.intent.intentName,
                "confidence": self.intent.confidenceScore,
            },
            "entities": [
                {
                    "entity": s.slotName,
                    "value": s.value,
                    "raw_value": s.raw_value,
                    "start": s.start,
                    "end": s.end,
                    "raw_start": (s.raw_start if s.raw_start is not None else s.start),
                    "raw_end": (s.raw_end if s.raw_end is not None else s.end),
                }
                for s in self.slots
            ],
            "slots": {s.slotName: s.value for s in self.slots},
            "text": self.input,
            "raw_text": self.raw_input,
            "tokens": self.asrTokens,
            "raw_tokens": self.rawAsrTokens,
            "wakewordId": self.wakewordId,
        }


@dataclass
class NluIntentNotRecognized(Message):
    """Intent not recognized."""

    input: str
    id: str = ""
    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/nlu/intentNotRecognized"

    # pylint: disable=R0201
    def to_rhasspy_dict(self) -> typing.Dict[str, typing.Any]:
        """Return an empty Rhasspy intent dictionary."""
        return {
            "text": self.input,
            "raw_text": self.input,
            "intent": {"name": "", "confidence": 0},
            "entities": [],
            "slots": {},
        }


@dataclass
class NluError(Message):
    """Error from NLU component."""

    error: str
    context: str = ""
    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/error/nlu"


# ----------------------------------------------------------------------------
# Rhasspy-specific Messages
# ----------------------------------------------------------------------------


@dataclass
class NluTrain(Message):
    """Request to retrain from sentences"""

    TOPIC_PATTERN = re.compile(r"^rhasspy/nlu/([^/]+)/train$")

    id: str
    graph_path: str
    graph_format: str = "pickle-gzip"

    @classmethod
    def is_site_in_topic(cls) -> bool:
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        siteId = kwargs.get("siteId", "+")
        return f"rhasspy/nlu/{siteId}/train"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(NluTrain.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_siteId(cls, topic: str) -> typing.Optional[str]:
        """Get siteId from a topic"""
        match = re.match(NluTrain.TOPIC_PATTERN, topic)
        assert match, "Not a train topic"
        return match.group(1)


@dataclass
class NluTrainSuccess(Message):
    """Result from successful training"""

    TOPIC_PATTERN = re.compile(r"^rhasspy/nlu/([^/]+)/trainSuccess$")

    id: str

    @classmethod
    def is_site_in_topic(cls) -> bool:
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        siteId = kwargs.get("siteId", "+")
        return f"rhasspy/nlu/{siteId}/trainSuccess"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(NluTrainSuccess.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_siteId(cls, topic: str) -> typing.Optional[str]:
        """Get siteId from a topic"""
        match = re.match(NluTrainSuccess.TOPIC_PATTERN, topic)
        assert match, "Not a trainSuccess topic"
        return match.group(1)
