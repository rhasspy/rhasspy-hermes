import typing

import attr

from .base import Message
from .intent import Intent, Slot


@attr.s
class NluQuery(Message):
    TOPIC = "hermes/nlu/query"

    input: str = attr.ib()
    intent_filter: typing.List[str] = attr.ib(factory=list)
    id: [str] = attr.ib(default="")
    sessionId: str = attr.ib(default="")

    def topic(self, *args, **kwargs) -> str:
        return NluQuery.TOPIC


@attr.s
class NluIntent(Message):
    input: str = attr.ib()
    intent: Intent = attr.ib()
    slots: typing.List[Slot] = attr.ib(factory=list)
    id: str = attr.ib(default="")
    sessionId: str = attr.ib(default="")
    customData: str = attr.ib(default="")

    def topic(self, intent_name: str, *args, **kwargs) -> str:
        return f"hermes/intent/{intent_name}"


@attr.s
class NluIntentNotRecognized(Message):
    TOPIC = "hermes/nlu/intentNotRecognized"

    input: str = attr.ib()
    id: str = attr.ib(default="")
    sessionId: str = attr.ib(default="")

    def topic(self, *args, **kwargs) -> str:
        return NluIntentNotRecognized.TOPIC


@attr.s
class NluError(Message):
    TOPIC = "hermes/error/nlu"

    error: str = attr.ib()
    context: str = attr.ib(default="")
    sessionId: str = attr.ib(default="")

    def topic(self, *args, **kwargs) -> str:
        return NluError.TOPIC
