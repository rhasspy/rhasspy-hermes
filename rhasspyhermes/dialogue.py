"""Messages for hermes/dialogueManager"""
import typing
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from dataclasses_json import DataClassJsonMixin, LetterCase, dataclass_json
from dataclasses_json.core import Json

from .base import Message


class DialogueActionType(str, Enum):
    """Type of session init objects.

    Values
    ------
    ACTION
        Use this type when you need the end user to respond

    NOTIFICATION
        Use this type when you only want to inform the user of something without
        expecting a response.
    """

    ACTION = "action"
    NOTIFICATION = "notification"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DialogueAction(DataClassJsonMixin):
    """Dialogue session action.

    Attributes
    ----------
    can_be_enqueued: bool
        If true, the session will start when there is no pending one on this
        site. Otherwise, the session is just dropped if there is running one.

    type: DialogueActionType = ACTION

    text: typing.Optional[str] = None
        Text that the TTS should say at the beginning of the session.

    intent_filter: typing.Optional[typing.List[str]] = None
        A list of intents names to restrict the NLU resolution on the first query.

    send_intent_not_recognized: bool = False
        Indicates whether the dialogue manager should handle non-recognized
        intents by itself or send them for the client to handle.
    """

    can_be_enqueued: bool
    type: DialogueActionType = DialogueActionType.ACTION
    text: typing.Optional[str] = None
    intent_filter: typing.Optional[typing.List[str]] = None
    send_intent_not_recognized: bool = False


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DialogueNotification(DataClassJsonMixin):
    """Dialogue session notification.

    Attributes
    ----------
    text: str
        Text the TTS should say

    type: DialogueActionType = NOTIFICATION
    """

    text: str
    type: DialogueActionType = DialogueActionType.NOTIFICATION


class DialogueSessionTerminationReason(str, Enum):
    """The reason why the session was ended.

    Values
    ------
    NOMINAL
        The session ended as expected (an endSession message was received)

    ABORTED_BY_USER
        The session aborted by the user

    INTENT_NOT_RECOGNIZED
        The session ended because no intent was successfully detected

    TIMEOUT
        The session timed out because no response from one of the components or
        no continue/end session message in a timely manner.

    ERROR
        The session failed with an error
    """

    NOMINAL = "nominal"
    ABORTED_BY_USER = "abortedByUser"
    INTENT_NOT_RECOGNIZED = "intentNotRecognized"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DialogueSessionTermination:
    """Dialogue session termination type.

    Attributes
    ----------
    reason: DialogueSessionTerminationReason
        The reason why the session was ended
    """

    reason: DialogueSessionTerminationReason


# -----------------------------------------------------------------------------


@dataclass
class DialogueStartSession(Message):
    """Start a dialogue session.

    You can send this message to programmatically initiate a new session. The
    Dialogue Manager will start the session by asking the TTS to say the text
    (if any) and wait for the answer of the end user.

    Attributes
    ----------
    init: Union[DialogueAction, DialogueNotification]
        Session initialization description

    site_id: str = "default"
        Site where to start the session

    custom_data: Optional[str] = None
        Additional information that can be provided by the handler. Each message
        related to the new session - sent by the Dialogue Manager - will contain
        this data.

    lang: Optional[str] = None
        Language of the session.
    """

    init: typing.Union[DialogueAction, DialogueNotification]
    site_id: str = "default"
    custom_data: typing.Optional[str] = None
    lang: typing.Optional[str] = None

    # pylint: disable=W0221
    @classmethod
    def from_dict(
        cls: typing.Type["DialogueStartSession"],
        message_dict: Json,
        *,
        infer_missing=False
    ) -> "DialogueStartSession":
        assert isinstance(message_dict, Mapping)
        init = message_dict.pop("init")
        if init["type"] == DialogueActionType.NOTIFICATION:
            message_dict["init"] = DialogueNotification.from_dict(init)
        else:
            message_dict["init"] = DialogueAction.from_dict(init)

        return super(DialogueStartSession, cls).from_dict(
            message_dict, infer_missing=infer_missing
        )

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/dialogueManager/startSession"


@dataclass
class DialogueSessionQueued(Message):
    """Sent when a dialogue session has been queued.

    Attributes
    ----------
    session_id: str
        Session identifier that was enqueued

    site_id: str = "default"
        Site where the user interaction will take place

    custom_data: typing.Optional[str] = None
        Custom data provided in the startSession message
    """

    session_id: str
    site_id: str = "default"
    custom_data: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "hermes/dialogueManager/sessionQueued"


@dataclass
class DialogueSessionStarted(Message):
    """Sent when a dialogue session has been started.

    Attributes
    ----------
    session_id: str
        Session identifier that was started

    site_id: str = "default"
        Site where the user interaction is taking place

    custom_data: typing.Optional[str] = None
        Custom data provided in the startSession message

    lang: Optional[str] = None
        Language of the session.
    """

    session_id: str
    site_id: str = "default"
    custom_data: typing.Optional[str] = None
    lang: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/dialogueManager/sessionStarted"


@dataclass
class DialogueContinueSession(Message):
    """Sent when a dialogue session should be continued.

    Attributes
    ----------
    session_id: str
        Identifier of the session to continue

    site_id: str = "default"
        Site where the user interaction is taking place

    text: Optional[str] = None
        The text the TTS should say to start this additional request of the
        session.

    intent_filter: Optional[List[str]] = None
        A list of intents names to restrict the NLU resolution on the answer of
        this query.

    custom_data: Optional[str] = None
        An update to the session's custom data. If not provided, the custom data
        will stay the same.

    send_intent_not_recognized: bool = False
        Indicates whether the dialogue manager should handle non recognized
        intents by itself or send them for the client to handle.

    slot: typing.Optional[str] = None
        Unused

    lang: Optional[str] = None
        Language of the session.
        Leave empty to use setting from start of session.
    """

    session_id: str
    site_id: str = "default"
    custom_data: typing.Optional[str] = None

    text: typing.Optional[str] = None
    intent_filter: typing.Optional[typing.List[str]] = None
    send_intent_not_recognized: bool = False
    slot: typing.Optional[str] = None

    # ------------
    # Rhasspy only
    # ------------

    lang: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/dialogueManager/continueSession"


@dataclass
class DialogueEndSession(Message):
    """Sent when a dialogue session should be ended.

    Attributes
    ----------
    session_id: str
        Identifier of the session to end

    site_id: str = "default"
        Site where the user interaction is taking place

    text: Optional[str] = None
        The text the TTS should say to end the session

    custom_data: Optional[str] = None
        An update to the session's custom data. If not provided, the custom data
        will stay the same.
    """

    session_id: str
    site_id: str = "default"
    text: typing.Optional[str] = None
    custom_data: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/dialogueManager/endSession"


@dataclass
class DialogueSessionEnded(Message):
    """Sent when a dialogue session has ended.

    Attributes
    ----------
    termination: DialogueSessionTermination
        Structured description of why the session has been ended

    session_id: str
        Session identifier of the ended session

    site_id: str = "default"
        Site where the user interaction took place

    custom_data: Optional[str] = None
        Custom data provided in the start/continue/end session messages
    """

    termination: DialogueSessionTermination
    session_id: str
    site_id: str = "default"
    custom_data: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/dialogueManager/sessionEnded"


@dataclass
class DialogueIntentNotRecognized(Message):
    """Intent not recognized.

    Only sent when send_intent_not_recognized is True.

    Attributes
    ----------
    session_id: str
        Session identifier of the session that generated this intent not
        recognized event.

    site_id: str = "default"
        Site where the user interaction took place

    input: typing.Optional[str] = None
        NLU input that generated this event

    custom_data: typing.Optional[str] = None
        Custom data provided by start/continue session messages
    """

    session_id: str
    site_id: str = "default"
    input: typing.Optional[str] = None
    custom_data: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/dialogueManager/intentNotRecognized"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DialogueConfigureIntent:
    """Enable/disable specific intent in configure message.

    Attributes
    ----------
    intent_id: str
        Name of intent to enable/disable

    enable: bool
        True if intent should be enabled
    """

    intent_id: str
    enable: bool


@dataclass
class DialogueConfigure(Message):
    """Enable/disable specific intents for future dialogue sessions.

    Attributes
    ----------
    intents: List[DialogueConfigureIntent]
        List of intents and whether to enable/disable htem

    site_id: str = "default"
        Id of site to configure
    """

    intents: typing.List[DialogueConfigureIntent]
    site_id: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "hermes/dialogueManager/configure"


# ----------------------------------------------------------------------------
# Rhasspy-Only Messages
# ----------------------------------------------------------------------------


@dataclass
class DialogueError(Message):
    """Error from dialogue manager component.

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
        """Get MQTT topic for this message type."""
        return "hermes/error/dialogueManager"
