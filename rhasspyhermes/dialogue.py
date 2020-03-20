"""Messages for hermes/dialogueManager"""
import typing
from enum import Enum

import attr

from .base import Message


class DialogueActionType(str, Enum):
    """Type of session init objects."""

    ACTION = "action"
    NOTIFICATION = "notification"


@attr.s(auto_attribs=True, slots=True)
class DialogueAction:
    """Dialogue session action."""

    canBeEnqueued: bool
    type: DialogueActionType = DialogueActionType.ACTION
    text: str = ""
    intentFilter: typing.Optional[typing.List[str]] = None
    sendIntentNotRecognized: bool = False


@attr.s(auto_attribs=True, slots=True)
class DialogueNotification:
    """Dialogue session notification."""

    text: str
    type: DialogueActionType = DialogueActionType.NOTIFICATION


class DialogueSessionTerminationReason(str, Enum):
    """The reason why the session was ended."""

    NOMINAL = "nominal"
    ABORTED_BY_USER = "abortedByUser"
    INTENT_NOT_RECOGNIZED = "intentNotRecognized"
    TIMEOUT = "timeout"
    ERROR = "error"


@attr.s(auto_attribs=True, slots=True)
class DialogueSessionTermination:
    """Dialogue session termination type."""

    reason: DialogueSessionTerminationReason


# -----------------------------------------------------------------------------


@attr.s(auto_attribs=True, slots=True)
class DialogueStartSession(Message):
    """Start a dialogue session."""

    init: typing.Union[DialogueAction, DialogueNotification]
    siteId: str = "default"
    customData: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/startSession"

    @classmethod
    def from_dict(cls, message_dict: typing.Dict[str, typing.Any]):
        """Construct message from dictionary."""
        message_dict = cls.only_fields(message_dict)
        init_dict = message_dict.pop("init")
        assert init_dict, "init is required"

        if init_dict["type"] == "action":
            return DialogueStartSession(  # type: ignore
                **message_dict, init=DialogueAction(**init_dict)
            )

        return DialogueStartSession(  # type: ignore
            **message_dict, init=DialogueNotification(**init_dict)
        )


@attr.s(auto_attribs=True, slots=True)
class DialogueSessionQueued(Message):
    """Sent when a dialogue session has been queued."""

    siteId: str = "default"
    sessionId: str = ""
    customData: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/sessionQueued"


@attr.s(auto_attribs=True, slots=True)
class DialogueSessionStarted(Message):
    """Sent when a dialogue session has been started."""

    siteId: str = "default"
    sessionId: str = ""
    customData: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/sessionStarted"


@attr.s(auto_attribs=True, slots=True)
class DialogueContinueSession(Message):
    """Sent when a dialogue session should be continued."""

    sessionId: str = ""
    customData: str = ""

    text: str = ""
    intentFilter: typing.Optional[typing.List[str]] = None
    sendIntentNotRecognized: bool = False
    slot: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/continueSession"


@attr.s(auto_attribs=True, slots=True)
class DialogueEndSession(Message):
    """Sent when a dialogue session should be ended."""

    sessionId: str = ""
    customData: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/endSession"


@attr.s(auto_attribs=True, slots=True)
class DialogueSessionEnded(Message):
    """Sent when a dialogue session has ended."""

    termination: DialogueSessionTermination
    sessionId: str = ""
    customData: str = ""
    siteId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/sessionEnded"


@attr.s(auto_attribs=True, slots=True)
class DialogueIntentNotRecognized(Message):
    """Intent not recognized."""

    input: str = ""
    sessionId: str = ""
    customData: str = ""
    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/intentNotRecognized"
