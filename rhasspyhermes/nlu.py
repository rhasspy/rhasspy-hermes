"""Messages for hermes/nlu"""
import re
import typing

import attr

from .base import Message
from .intent import Intent, Slot


@attr.s
class NluQuery(Message):
    """Send text to the NLU component."""

    input: str = attr.ib()
    intentFilter: typing.Optional[typing.List[str]] = attr.ib(default=None)
    id: str = attr.ib(default="")
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/nlu/query"


@attr.s
class NluIntent(Message):
    """Intent recognized."""

    TOPIC_PATTERN = re.compile(r"^hermes/intent/([^/]+)$")

    input: str = attr.ib()
    intent: Intent = attr.ib()
    slots: typing.List[Slot] = attr.ib(factory=list)
    id: str = attr.ib(default="")
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")
    customData: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        intentName = kwargs["intentName"]
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


@attr.s
class NluIntentNotRecognized(Message):
    """Intent not recognized."""

    input: str = attr.ib()
    id: str = attr.ib(default="")
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/nlu/intentNotRecognized"


@attr.s
class NluError(Message):
    """Error from NLU component."""

    error: str = attr.ib()
    context: str = attr.ib(default="")
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/error/nlu"
