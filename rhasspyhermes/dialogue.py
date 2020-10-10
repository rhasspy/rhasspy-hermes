"""Messages for the Hermes dialogue manager."""
import typing
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from dataclasses_json import DataClassJsonMixin, LetterCase, dataclass_json
from dataclasses_json.core import Json

from .base import Message


class DialogueActionType(str, Enum):
    """Type of session init objects."""

    ACTION = "action"
    """Use this type when you need the user to respond."""
    NOTIFICATION = "notification"
    """Use this type when you only want to inform the user of something without
    expecting a response."""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DialogueAction(DataClassJsonMixin):
    """Dialogue session action."""

    can_be_enqueued: bool
    """If true, the session will start when there is no pending one on this
    site. Otherwise, the session is just dropped if there is running one."""
    type: DialogueActionType = DialogueActionType.ACTION
    """This value is always :class:`DialogueActionType.ACTION`."""
    text: typing.Optional[str] = None
    """Text that the TTS should say at the beginning of the session."""
    intent_filter: typing.Optional[typing.List[str]] = None
    """A list of intents names to restrict the NLU resolution on the first query."""
    send_intent_not_recognized: bool = False
    """Indicates whether the dialogue manager should handle non-recognized
    intents by itself or send them for the client to handle."""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DialogueNotification(DataClassJsonMixin):
    """Dialogue session notification."""

    text: str
    """Text the TTS should say."""
    type: DialogueActionType = DialogueActionType.NOTIFICATION
    """This value is always :class:`DialogueActionType.NOTIFICATION`."""


class DialogueSessionTerminationReason(str, Enum):
    """The reason why the session was ended."""

    NOMINAL = "nominal"
    """The session ended as expected (a :class:`DialogueEndSession` message was received)."""
    ABORTED_BY_USER = "abortedByUser"
    """The session was aborted by the user."""
    INTENT_NOT_RECOGNIZED = "intentNotRecognized"
    """The session ended because no intent was successfully detected."""
    TIMEOUT = "timeout"
    """The session timed out because there was no response from one of the components or
    no :class:`DialogueContinueSession` or :class:`DialogueEndSession` message in a timely manner."""
    ERROR = "error"
    """The session failed with an error."""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DialogueSessionTermination:
    """Dialogue session termination type."""

    reason: DialogueSessionTerminationReason
    """The reason why the session was ended."""


# -----------------------------------------------------------------------------


@dataclass
class DialogueStartSession(Message):
    """Start a dialogue session.

    You can send this message to programmatically initiate a new session. The
    Dialogue Manager will start the session by asking the TTS to say the text
    (if any) and wait for the answer of the user.

    .. admonition:: MQTT message

      Topic
        ``hermes/dialogueManager/startSession``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - siteId
            - String
            - The id of the site where to start the session.
          * - init
            - JSON object
            - Session initialization description.
          * - customData
            - String (optional)
            - Additional information that can be provided by the handler. Each message
              related to the new session - sent by the Dialogue Manager - will contain
              this data.
          * - lang
            - String (optional)
            - Language of the session.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'hermes/dialogueManager/startSession' -m '{"siteId": "livingroom", "init": {"type": "notification", "text": "Ready"}, "lang": "en"}'

    Example
    -------
    >>> from rhasspyhermes.dialogue import DialogueStartSession, DialogueNotification
    >>> start_session = DialogueStartSession(init=DialogueNotification(text="Ready"), site_id="livingroom", lang="en")
    >>> start_session
    DialogueStartSession(init=DialogueNotification(text='Ready', type=<DialogueActionType.NOTIFICATION: 'notification'>), site_id='livingroom', custom_data=None, lang='en')
    >>> start_session.payload()
    '{"init": {"text": "Ready", "type": "notification"}, "siteId": "livingroom", "customData": null, "lang": "en"}'
    """

    init: typing.Union[DialogueAction, DialogueNotification]
    """Session initialization description."""
    site_id: str = "default"
    """The id of the site where to start the session."""
    custom_data: typing.Optional[str] = None
    """Additional information that can be provided by the handler. Each message
    related to the new session - sent by the Dialogue Manager - will contain
    this data."""
    lang: typing.Optional[str] = None
    """Language of the session.

    Note
    ----

    This is a Rhasspy-only attribute.
    """

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
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/dialogueManager/startSession"``
        """
        return "hermes/dialogueManager/startSession"


@dataclass
class DialogueSessionQueued(Message):
    """Sent by the dialogue manager when it receives a :class:`DialogueStartSession` message
    and the site where the interaction should take place is busy. When the site is free again,
    the session will be started.

    Only :class:`DialogueStartSession` messages with an ``init`` attribute of the following type
    can be enqueued:

    - :class:`DialogueNotification`
    - :class:`DialogueAction` with the attribute ``canBeEnqueued`` set to ``True``.

    .. admonition:: MQTT message

      Topic
        ``hermes/dialogueManager/sessionQueued``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - sessionId
            - String
            - The id of the session that was enqueued.
          * - siteId
            - String
            - The id of the site where the user interaction will take place.
          * - customData
            - String (optional)
            - Custom data provided in the :class:`DialogueStartSession` message.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/dialogueManager/sessionQueued'
    """

    session_id: str
    """The id of the session that was enqueued."""
    site_id: str = "default"
    """The id of the site where the user interaction will take place."""
    custom_data: typing.Optional[str] = None
    """Custom data provided in the :class:`DialogueStartSession` message."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/dialogueManager/sessionQueued"``
        """
        return "hermes/dialogueManager/sessionQueued"


@dataclass
class DialogueSessionStarted(Message):
    """Sent when a dialogue session has been started.

    .. admonition:: MQTT message

      Topic
        ``hermes/dialogueManager/sessionStarted``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - sessionId
            - String
            - The id of the session that was started.
          * - siteId
            - String
            - The id of the site where the user interaction is taking place.
          * - customData
            - String (optional)
            - Custom data provided in the :class:`DialogueStartSession` message.
          * - lang
            - String (optional)
            - Language of the session.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/dialogueManager/sessionStarted'
    """

    session_id: str
    """The id of the session that was started."""
    site_id: str = "default"
    """The id of the site where the user interaction is taking place."""
    custom_data: typing.Optional[str] = None
    """Custom data provided in the :class:`DialogueStartSession` message."""
    lang: typing.Optional[str] = None
    """Language of the session.

    Note
    ----

    This is a Rhasspy-only attribute.
    """

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/dialogueManager/sessionStarted"``

        """
        return "hermes/dialogueManager/sessionStarted"


@dataclass
class DialogueContinueSession(Message):
    """Sent when a dialogue session should be continued.

    You should send this message after receiving a :class:`rhasspyhermes.nlu.NluIntent` message
    if you want to continue the session. This can be used for example to ask
    additional information to the user.

    Make sure to use the same ``sessionId`` as the original :class:`rhasspyhermes.nlu.NluIntent`
    message.

    .. admonition:: MQTT message

      Topic
        ``hermes/dialogueManager/continueSession``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - sessionId
            - String
            - The id of the session to continue.
          * - customData
            - String (optional)
            - An update to the session's custom data. If not provided, the custom data
              will stay the same.
          * - text
            - String (optional)
            - The text the TTS should say to start this additional request of the
              session.
          * - intentFilter
            - List of Strings (optional)
            - A list of intent names to restrict the NLU resolution on the answer of
              this query.
          * - sendIntentNotRecognized
            - Boolean
            - Indicates whether the dialogue manager should handle non recognized
              intents by itself or send them for the client to handle.
          * - slot
            - String (optional)
            - Unused.
          * - lang
            - String (optional)
            - Language of the session.
              Leave empty to use setting from start of session.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'hermes/dialogueManager/continueSession' -m '{"sessionId": "foobar", "customData": null, "text": "Are you sure?", "intentFilter": null, "sendIntentNotRecognized": false, "slot": null, "lang": null}'

    Example
    -------
    >>> from rhasspyhermes.dialogue import DialogueContinueSession
    >>> session = DialogueContinueSession(session_id="foobar", text="Are you sure?")
    >>> session
    DialogueContinueSession(session_id='foobar', custom_data=None, text='Are you sure?', intent_filter=None, send_intent_not_recognized=False, slot=None, lang=None)
    >>> session.payload()
    '{"sessionId": "foobar", "customData": null, "text": "Are you sure?", "intentFilter": null, "sendIntentNotRecognized": false, "slot": null, "lang": null}'
    """

    session_id: str
    """The id of the session to continue."""
    site_id: str = "default"
    """The id of the site where to continue the session."""
    custom_data: typing.Optional[str] = None
    """An update to the session's custom data. If not provided, the custom data
    will stay the same."""
    text: typing.Optional[str] = None
    """The text the TTS should say to start this additional request of the
    session."""
    intent_filter: typing.Optional[typing.List[str]] = None
    """A list of intent names to restrict the NLU resolution on the answer of
    this query."""
    send_intent_not_recognized: bool = False
    """Indicates whether the dialogue manager should handle non recognized
    intents by itself or send them for the client to handle."""
    slot: typing.Optional[str] = None
    """Unused."""

    # ------------
    # Rhasspy only
    # ------------

    lang: typing.Optional[str] = None
    """Language of the session.
    Leave empty to use setting from start of session.

    Note
    ----

    This is a Rhasspy-only attribute.
    """

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/dialogueManager/continueSession"``
        """
        return "hermes/dialogueManager/continueSession"


@dataclass
class DialogueEndSession(Message):
    """Sent when a dialogue session should be ended.

    You should send this message after receiving a :class:`rhasspyhermes.nlu.NluIntent` message
    if you want to end the session.

    Make sure to use the same ``sessionId`` as the original :class:`rhasspyhermes.nlu.NluIntent`
    message.

    .. admonition:: MQTT message

      Topic
        ``hermes/dialogueManager/continueSession``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - sessionId
            - String
            - The id of the session to continue.
          * - customData
            - String (optional)
            - An update to the session's custom data. If not provided, the custom data
              will stay the same.
          * - text
            - String (optional)
            - The text the TTS should say to end the session.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'hermes/dialogueManager/endSession' -m '{"sessionId": "foobar", "customData": null, "text": "OK, turning off the light"}'

    Example
    -------
    >>> from rhasspyhermes.dialogue import DialogueEndSession
    >>> session = DialogueEndSession(session_id="foobar", text="OK, turning off the light")
    >>> session
    DialogueEndSession(session_id='foobar', text='OK, turning off the light', custom_data=None)
    >>> session.payload()
    '{"sessionId": "foobar", "text": "OK, turning off the light", "customData": null}'
    """

    session_id: str
    """The id of the session to end."""
    site_id: str = "default"
    """The id of the site where to end the session."""
    text: typing.Optional[str] = None
    """The text the TTS should say to end the session."""
    custom_data: typing.Optional[str] = None
    """An update to the session's custom data. If not provided, the custom data
    will stay the same."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/dialogueManager/endSession"``
        """
        return "hermes/dialogueManager/endSession"


@dataclass
class DialogueSessionEnded(Message):
    """Sent when a dialogue session has ended.

    .. admonition:: MQTT message

      Topic
        ``hermes/dialogueManager/sessionEnded``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - termination
            - JSON Object
            - Structured description of why the session has been ended. See
              :class:`DialogueSessionTerminationReason` for the possible values.
          * - sessionId
            - String
            - The id of the ended session.
          * - siteId
            - String
            - The id of the site where the user interaction took place.
          * - customData
            - String (optional)
            - Custom data provided in the :class:`DialogueStartSession`,
              :class:`DialogueContinueSession` or :class:`DialogueEndSession` messages.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/dialogueManager/sessionEnded'
    """

    termination: DialogueSessionTermination
    """Structured description of why the session has been ended."""
    session_id: str
    """The id of the ended session."""
    site_id: str = "default"
    """The id of the site where the user interaction took place."""
    custom_data: typing.Optional[str] = None
    """Custom data provided in the :class:`DialogueStartSession`,
    :class:`DialogueContinueSession` or :class:`DialogueEndSession` messages."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/dialogueManager/sessionEnded"``
        """
        return "hermes/dialogueManager/sessionEnded"


@dataclass
class DialogueIntentNotRecognized(Message):
    """Intent not recognized.

    Only sent when ``send_intent_not_recognized`` is ``True``.

    .. admonition:: MQTT message

      Topic
        ``hermes/dialogueManager/intentNotRecognized``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - sessionId
            - String
            - The id of the session that generated this event.
          * - siteId
            - String
            - The id of the site where the user interaction took place.
          * - input
            - String (optional)
            - The NLU input that generated this event.
          * - customData
            - String (optional)
            - Custom data provided in the :class:`DialogueStartSession` or
              :class:`DialogueContinueSession` messages.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/dialogueManager/intentNotRecognized'
    """

    session_id: str
    """The id of the session that generated this event."""
    site_id: str = "default"
    """The id of the site where the user interaction took place."""
    input: typing.Optional[str] = None
    """The NLU input that generated this event."""
    custom_data: typing.Optional[str] = None
    """Custom data provided in the :class:`DialogueStartSession` or
    :class:`DialogueContinueSession` messages."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/dialogueManager/intentNotRecognized"``
        """
        return "hermes/dialogueManager/intentNotRecognized"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DialogueConfigureIntent:
    """Enable/disable a specific intent in a :class:`DialogueConfigure` message."""

    intent_id: str
    """Name of the intent to enable/disable."""
    enable: bool
    """``True`` if the intent should be enabled."""


@dataclass
class DialogueConfigure(Message):
    """Enable/disable specific intents for future dialogue sessions.

    If an intent is enabled, the :class:`rhasspyhermes.nlu.NluIntent` message is triggered when
    the intent is detected.

    Rhasspy enables all intents by default unless specified otherwise.

    .. admonition:: MQTT message

      Topic
        ``hermes/dialogueManager/configure``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - intents
            - List of JSON Objects
            - The list of intents and whether to enable/disable them.
          * - siteId
            - String
            - The id of the site to configure.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'hermes/dialogueManager/configure' -m '{"intents": [{"intentId": "GetTime", "enable": true}, {"intentId": "GetTemperature", "enable": false}], "siteId": "livingroom"}'

    Example
    -------
    >>> from rhasspyhermes.dialogue import DialogueConfigureIntent, DialogueConfigure
    >>> configure = DialogueConfigure([DialogueConfigureIntent("GetTime", True), DialogueConfigureIntent("GetTemperature", False)], "livingroom")
    >>> configure
    DialogueConfigure(intents=[DialogueConfigureIntent(intent_id='GetTime', enable=True), DialogueConfigureIntent(intent_id='GetTemperature', enable=False)], site_id='livingroom')
    >>> configure.payload()
    '{"intents": [{"intentId": "GetTime", "enable": true}, {"intentId": "GetTemperature", "enable": false}], "siteId": "livingroom"}'
    """

    intents: typing.List[DialogueConfigureIntent]
    """The list of intents and whether to enable/disable them."""
    site_id: str = "default"
    """The id of the site to configure."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/dialogueManager/configure"``
        """
        return "hermes/dialogueManager/configure"


# ----------------------------------------------------------------------------
# Rhasspy-Only Messages
# ----------------------------------------------------------------------------


@dataclass
class DialogueError(Message):
    """This message is published by the dialogue manager component if an error has occurred.

    .. admonition:: MQTT message

      Topic
        ``hermes/error/dialogueManager``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - error
            - String
            - A description of the error that occurred.
          * - siteId
            - String
            - The id of the site where the error occurred.
          * - context
            - String (optional)
            - Additional information on the context in which the error occurred.
          * - sessionId
            - String (optional)
            - The id of the session, if there is an active session.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/error/dialogueManager'

    Example
    -------

    >>> from rhasspyhermes.dialogue import DialogueError
    >>> dialogue_error = DialogueError(error="Unexpected error")
    >>> dialogue_error.topic()
    'hermes/error/dialogueManager'
    >>> dialogue_error.payload()
    '{"error": "Unexpected error", "siteId": "default", "context": null, "sessionId": null}'

    Note
    ----

    This is a Rhasspy-only message.
    """

    error: str
    """A description of the error that occurred."""
    site_id: str = "default"
    """The id of the site where the error occurred."""
    context: typing.Optional[str] = None
    """Additional information on the context in which the error occurred."""
    session_id: typing.Optional[str] = None
    """The id of the session, if there is an active session."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/error/dialogueManager"``
        """
        return "hermes/error/dialogueManager"
