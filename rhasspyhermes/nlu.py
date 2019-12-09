import typing

import attr

from .base import Message
from .intent import Intent, Slot


@attr.s
class NluQuery(Message):
    """Send text to the NLU component."""

    input: str = attr.ib()
    intent_filter: typing.List[str] = attr.ib(factory=list)
    id: [str] = attr.ib(default="")
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, *args, **kwargs) -> str:
        return "hermes/nlu/query"


@attr.s
class NluIntent(Message):
    """Intent recognized."""

    input: str = attr.ib()
    intent: Intent = attr.ib()
    slots: typing.List[Slot] = attr.ib(factory=list)
    id: str = attr.ib(default="")
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")
    customData: str = attr.ib(default="")

    @classmethod
    def topic(cls, intent_name: str, *args, **kwargs) -> str:
        return f"hermes/intent/{intent_name}"


@attr.s
class NluIntentNotRecognized(Message):
    """Intent not recognized."""

    input: str = attr.ib()
    id: str = attr.ib(default="")
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, *args, **kwargs) -> str:
        return "hermes/nlu/intentNotRecognized"


@attr.s
class NluError(Message):
    """Error from NLU component."""

    error: str = attr.ib()
    context: str = attr.ib(default="")
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, *args, **kwargs) -> str:
        return "hermes/error/nlu"
