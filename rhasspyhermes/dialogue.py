"""Messages for hermes/dialogueManager"""
import typing
from enum import Enum

import attr

from .base import Message


class DialogueActionType(str, Enum):
    """Type of session init objects."""

    ACTION = "action"
    NOTIFICATION = "notification"


@attr.s
class DialogueAction:
    """Dialogue session action."""

    canBeEnqueued: bool = attr.ib()
    type: DialogueActionType = attr.ib(default=DialogueActionType.ACTION)
    text: str = attr.ib(default="")
    intentFilter: typing.Optional[typing.List[str]] = attr.ib(default=None)
    sendIntentNotRecognized: bool = attr.ib(default=False)


@attr.s
class DialogueNotification:
    """Dialogue session notification."""

    text: str = attr.ib()
    type: DialogueActionType = attr.ib(default=DialogueActionType.NOTIFICATION)


class DialogueSessionTerminationReason(str, Enum):
    """The reason why the session was ended."""

    NOMINAL = "nominal"
    ABORTED_BY_USER = "abortedByUser"
    INTENT_NOT_RECOGNIZED = "intentNotRecognized"
    TIMEOUT = "timeout"
    ERROR = "error"


@attr.s
class DialogueSessionTermination:
    """Dialogue session termination type."""

    reason: DialogueSessionTerminationReason = attr.ib()


# -----------------------------------------------------------------------------


@attr.s
class DialogueStartSession(Message):
    """Start a dialogue session."""

    init: typing.Union[DialogueAction, DialogueNotification] = attr.ib()
    siteId: str = attr.ib(default="default")
    customData: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/startSession"


@attr.s
class DialogueSessionQueued(Message):
    """Sent when a dialogue session has been queued."""

    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")
    customData: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/sessionQueued"


@attr.s
class DialogueSessionStarted(Message):
    """Sent when a dialogue session has been started."""

    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")
    customData: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/sessionStarted"


@attr.s
class DialogueContinueSession(Message):
    """Sent when a dialogue session should be continued."""

    sessionId: str = attr.ib(default="")
    customData: str = attr.ib(default="")

    text: str = attr.ib(default="")
    intentFilter: typing.Optional[typing.List[str]] = attr.ib(default=None)
    sendIntentNotRecognized: bool = attr.ib(default=False)
    slot: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/continueSession"


@attr.s
class DialogueEndSession(Message):
    """Sent when a dialogue session should be ended."""

    sessionId: str = attr.ib(default="")
    customData: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/endSession"


@attr.s
class DialogueSessionEnded(Message):
    """Sent when a dialogue session has ended."""

    termination: DialogueSessionTermination = attr.ib()
    sessionId: str = attr.ib(default="")
    customData: str = attr.ib(default="")
    siteId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/sessionEnded"


@attr.s
class DialogueIntentNotRecognized(Message):
    """Intent not recognized."""

    input: str = attr.ib(default="")
    sessionId: str = attr.ib(default="")
    customData: str = attr.ib(default="")
    siteId: str = attr.ib(default="default")

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/intentNotRecognized"
