"""Messages for natural language understanding."""
import re
import typing
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

from .base import Message
from .intent import Intent, Slot


@dataclass
class NluQuery(Message):
    """Request intent recognition from NLU component.

    Attributes
    ----------
    input: str
        The text to send to the NLU component

    site_id: str = "default"
        Id of site where NLU component is located

    id: Optional[str] = None
        Unique id for request

    intent_filter: Optional[List[str]] = None
        A list of intent names to restrict the NLU resolution on

    session_id: Optional[str] = None
        The id of the session, if there is an active session

    wakeword_id: Optional[str] = None
        Optional id of wakeword used to activate ASR

    lang: Optional[str] = None
        Language of the session
    """

    input: str
    site_id: str = "default"
    id: typing.Optional[str] = None
    intent_filter: typing.Optional[typing.List[str]] = None
    session_id: typing.Optional[str] = None

    # ------------
    # Rhasspy only
    # ------------

    wakeword_id: typing.Optional[str] = None
    lang: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/nlu/query"


@dataclass
class NluIntentParsed(Message):
    """Intent successfully parsed.

    Preceeds full intent message.

    Attributes
    ----------
    input: str
        The user input that has generated this intent

    intent: Intent
        Structured description of the intent classification

    site_id: str = "default"
        Site where the user interaction took place

    id: Optional[str] = None
        Request id from NLU query, if any

    slots: Optional[List[Slot]] = None
        Structured description of the detected slots for this intent if any

    session_id: Optional[str] = None
        Session of the intent detection. The client code must use it to continue
        or end the session.
    """

    input: str
    intent: Intent
    site_id: str = "default"
    id: typing.Optional[str] = None
    slots: typing.Optional[typing.List[Slot]] = None
    session_id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message."""
        return "hermes/nlu/intentParsed"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AsrTokenTime:
    """Time when ASR token was detected.

    Attributes
    ----------
    start: float
        Start time of token relative to beginning of utterance

    end: float
        End time of token relative to beginning of utterance
    """

    start: float
    end: float


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AsrToken:
    """Token from automated speech recognizer.

    Attributes
    ----------
    value: str
        Text value of token

    confidence: float
        Confidence of the token, between 0 and 1, 1 being confident

    range_start: int
        The start range in which the token is in the original input

    range_end: int
        The end range in which the token is in the original input

    time: Optional[AsrTokenTime] = None
        Structured time when this token was detected
    """

    value: str
    confidence: float
    range_start: int
    range_end: int
    time: typing.Optional[AsrTokenTime] = None


@dataclass
class NluIntent(Message):
    """Recognized intent.

    Attributes
    ----------
    input: str
        The user input that has generated this intent

    intent: Intent
        Structured description of the intent classification

    site_id: str = "default"
        Site where the user interaction took place

    id: Optional[str] = None
        Request id from NLU query, if any

    slots: Optional[List[Slot]] = None
        Structured description of the detected slots for this intent if any

    session_id: Optional[str] = None
        Session of the intent detection. The client code must use it to continue
        or end the session.

    custom_data: Optional[str] = None
        Custom data provided by start/continue/end session messages

    asr_tokens: Optional[List[List[AsrToken]]] = None
        Structured description of the tokens the ASR captured on for this intent

    asr_confidence: Optional[float] = None
        Speech recognizer confidence score between 0 and 1, 1 being sure

    raw_input: Optional[str] = None
        Original query input before substitutions, such as number replacement

    wakeword_id: Optional[str] = None
        Id of the wake word that triggered this session

    lang: Optional[str] = None
        Language of the session
    """

    TOPIC_PATTERN = re.compile(r"^hermes/intent/(.+)$")

    input: str
    intent: Intent
    site_id: str = "default"
    id: typing.Optional[str] = None
    slots: typing.Optional[typing.List[Slot]] = None
    session_id: typing.Optional[str] = None
    custom_data: typing.Optional[str] = None
    asr_tokens: typing.Optional[typing.List[typing.List[AsrToken]]] = None
    asr_confidence: typing.Optional[float] = None

    # ------------
    # Rhasspy only
    # ------------

    raw_input: typing.Optional[str] = None
    wakeword_id: typing.Optional[str] = None
    lang: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get topic for message (intent_name)."""
        intent_name = kwargs.get("intent_name", "#")
        return f"hermes/intent/{intent_name}"

    @classmethod
    def get_intent_name(cls, topic: str) -> str:
        """Get intent_name from a topic"""
        match = re.match(NluIntent.TOPIC_PATTERN, topic)
        assert match, "Not an intent topic"
        return match.group(1)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(NluIntent.TOPIC_PATTERN, topic) is not None

    def to_rhasspy_dict(self) -> typing.Dict[str, typing.Any]:
        """Convert to Rhasspy format."""
        return {
            "intent": {
                "name": self.intent.intent_name,
                "confidence": self.intent.confidence_score,
            },
            "entities": [
                {
                    "entity": s.slot_name,
                    "value": s.value.get("value"),
                    "value_details": s.value,
                    "raw_value": s.raw_value,
                    "start": s.start,
                    "end": s.end,
                    "raw_start": (s.raw_start if s.raw_start is not None else s.start),
                    "raw_end": (s.raw_end if s.raw_end is not None else s.end),
                }
                for s in self.slots or []
            ],
            "slots": {s.slot_name: s.value.get("value") for s in self.slots or []},
            "text": self.input,
            "raw_text": self.raw_input or "",
            "tokens": self.input.split(),
            "raw_tokens": (self.raw_input or self.input).split(),
            "wakeword_id": self.wakeword_id,
        }

    @classmethod
    def make_asr_tokens(cls, tokens: typing.List[typing.Any]) -> typing.List[AsrToken]:
        """Create ASR token objects from words."""
        asr_tokens: typing.List[AsrToken] = []
        start: int = 0

        for token in tokens:
            token_str = str(token)
            asr_tokens.append(
                AsrToken(
                    value=token_str,
                    confidence=1.0,
                    range_start=start,
                    range_end=(start + len(token_str)),
                )
            )

            start += len(token_str) + 1

        return asr_tokens


@dataclass
class NluIntentNotRecognized(Message):
    """Intent not recognized.

    Attributes
    ----------
    input: str
        The input, if any that generated this event

    site_id: str = "default"
        Site where the user interaction took place

    id: Optional[str] = None
        Request id from NLU query, if any

    custom_data: Optional[str] = None
        Custom data provided by start/continue/end session messages

    session_id: Optional[str] = None
        Session identifier of the session that generated this intent not recognized event
    """

    input: str
    site_id: str = "default"
    id: typing.Optional[str] = None
    custom_data: typing.Optional[str] = None
    session_id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/nlu/intentNotRecognized"

    def to_rhasspy_dict(self) -> typing.Dict[str, typing.Any]:
        """Return an empty Rhasspy intent dictionary."""
        tokens = self.input.split()
        return {
            "text": self.input,
            "raw_text": self.input,
            "tokens": tokens,
            "raw_tokens": tokens,
            "intent": {"name": "", "confidence": 0.0},
            "entities": [],
            "slots": {},
        }


@dataclass
class NluError(Message):
    """Error from NLU component.

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
        """Get MQTT topic for this message."""
        return "hermes/error/nlu"


# ----------------------------------------------------------------------------
# Rhasspy-specific Messages
# ----------------------------------------------------------------------------


@dataclass
class NluTrain(Message):
    """Request to retrain NLU from intent graph.

    Attributes
    ----------
    graph_path: str
        Path to the graph file

    id: Optional[str] = None
        Unique id for training request

    graph_format: typing.Optional[str] = None
        Optional format of the graph file
    """

    TOPIC_PATTERN = re.compile(r"^rhasspy/nlu/([^/]+)/train$")

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
        return f"rhasspy/nlu/{site_id}/train"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(NluTrain.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from a topic"""
        match = re.match(NluTrain.TOPIC_PATTERN, topic)
        assert match, "Not a train topic"
        return match.group(1)


@dataclass
class NluTrainSuccess(Message):
    """Result from successful training.

    Attributes
    ----------

    id: Optional[str] = None
        Unique id from training request
    """

    TOPIC_PATTERN = re.compile(r"^rhasspy/nlu/([^/]+)/trainSuccess$")

    id: typing.Optional[str] = None

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        site_id = kwargs.get("site_id", "+")
        return f"rhasspy/nlu/{site_id}/trainSuccess"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(NluTrainSuccess.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from a topic"""
        match = re.match(NluTrainSuccess.TOPIC_PATTERN, topic)
        assert match, "Not a trainSuccess topic"
        return match.group(1)
