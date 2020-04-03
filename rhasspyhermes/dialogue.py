"""Messages for hermes/dialogueManager"""
import typing
from dataclasses import dataclass
from enum import Enum

from .base import Message


class DialogueActionType(str, Enum):
    """Type of session init objects."""

    ACTION = "action"
    NOTIFICATION = "notification"


@dataclass
class DialogueAction:
    """Dialogue session action."""

    canBeEnqueued: bool
    type: DialogueActionType = DialogueActionType.ACTION
    text: str = ""
    intentFilter: typing.Optional[typing.List[str]] = None
    sendIntentNotRecognized: bool = False


@dataclass
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


@dataclass
class DialogueSessionTermination:
    """Dialogue session termination type."""

    reason: DialogueSessionTerminationReason


# -----------------------------------------------------------------------------


@dataclass
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


@dataclass
class DialogueSessionQueued(Message):
    """Sent when a dialogue session has been queued."""

    siteId: str = "default"
    sessionId: str = ""
    customData: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/sessionQueued"


@dataclass
class DialogueSessionStarted(Message):
    """Sent when a dialogue session has been started."""

    siteId: str = "default"
    sessionId: str = ""
    customData: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/sessionStarted"


@dataclass
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


@dataclass
class DialogueEndSession(Message):
    """Sent when a dialogue session should be ended."""

    sessionId: str = ""
    text: str = ""
    customData: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/endSession"


@dataclass
class DialogueSessionEnded(Message):
    """Sent when a dialogue session has ended."""

    termination: DialogueSessionTermination
    sessionId: str = ""
    customData: str = ""
    siteId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/sessionEnded"


@dataclass
class DialogueIntentNotRecognized(Message):
    """Intent not recognized."""

    input: str = ""
    sessionId: str = ""
    customData: str = ""
    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/intentNotRecognized"


# ----------------------------------------------------------------------------
# Rhasspy-specific Messages
# ----------------------------------------------------------------------------


@dataclass
class DialogueError(Message):
    """Error from dialogue manager component."""

    error: str
    context: str = ""
    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/error/dialogueManager"
