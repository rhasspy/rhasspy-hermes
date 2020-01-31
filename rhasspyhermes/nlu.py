"""Messages for hermes/nlu"""
import re
import typing

import attr

from .base import Message
from .intent import Intent, Slot


@attr.s(auto_attribs=True, slots=True)
class NluQuery(Message):
    """Send text to the NLU component."""

    input: str
    intentFilter: typing.Optional[typing.List[str]] = None
    id: str = ""
    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/nlu/query"


@attr.s(auto_attribs=True, slots=True)
class NluIntent(Message):
    """Intent recognized."""

    TOPIC_PATTERN = re.compile(r"^hermes/intent/([^/]+)$")

    input: str
    intent: Intent
    slots: typing.List[Slot] = attr.Factory(list)
    id: str = ""
    siteId: str = "default"
    sessionId: str = ""
    customData: str = ""
    asrTokens: typing.List[str] = attr.Factory(list)
    asrConfidence: float = 1.0

    @classmethod
    def topic(cls, intentName: str, **kwargs) -> str:
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


@attr.s(auto_attribs=True, slots=True)
class NluIntentNotRecognized(Message):
    """Intent not recognized."""

    input: str
    id: str = ""
    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/nlu/intentNotRecognized"


@attr.s(auto_attribs=True, slots=True)
class NluError(Message):
    """Error from NLU component."""

    error: str
    context: str = ""
    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/error/nlu"
