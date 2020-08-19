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

    .. admonition:: MQTT message

      Topic
        ``hermes/nlu/query``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - input
            - String
            - The text to send to the NLU component.
          * - siteId
            - String
            - The id of the site where the NLU component is located. Defaults to ``"default"``.
          * - id
            - String (optional)
            - A request identifier. If provided, it will be passed back in the response
              (:class:`NluIntentParsed` or :class:`NluIntentNotRecognized`).
          * - intentFilter
            - List of strings (optional)
            - A list of intent names to restrict the NLU resolution on.
          * - sessionId
            - String (optional)
            - The id of the session, if there is an active session.
          * - wakewordId
            - String (optional)
            - The id of the wakeword used to activate the ASR.
          * - lang
            - String (optional)
            - The language of the session.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'hermes/nlu/query' -m '{"input": "what time is it", "siteId": "default"}'

    Example
    -------

    >>> from rhasspyhermes.nlu import NluQuery
    >>> query = NluQuery(input='what time is it')
    >>> query.payload()
    '{"input": "what time is it", "siteId": "default", "id": null, "intentFilter": null, "sessionId": null, "wakewordId": null, "lang": null}'
    >>> query.topic()
    'hermes/nlu/query'
    """

    input: str
    """The text to send to the NLU component."""
    site_id: str = "default"
    """The id of the site where the NLU component is located.

    Note
    ----

    In contrast to the Snips Hermes protocol, the site id is compulsory.
    """
    id: typing.Optional[str] = None
    """A request identifier. If provided, it will be passed back in the response
    (:class:`NluIntentParsed` or :class:`NluIntentNotRecognized`)."""
    intent_filter: typing.Optional[typing.List[str]] = None
    """A list of intent names to restrict the NLU resolution on."""
    session_id: typing.Optional[str] = None
    """The id of the session, if there is an active session.

    Note
    ----

    In contrast to the Snips Hermes protocol, the session id is optional.
    """

    # ------------
    # Rhasspy only
    # ------------

    wakeword_id: typing.Optional[str] = None
    """Optional id of the wakeword used to activate the ASR.

    Note
    ----

    This is a Rhasspy-only attribute.
    """
    lang: typing.Optional[str] = None
    """Optional language of the session.

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
            ``"hermes/nlu/query"``
        """
        return "hermes/nlu/query"


@dataclass
class NluIntentParsed(Message):
    """An intent is successfully parsed.

    The NLU component returns this message as a result of the intent resolution
    requested by a :class:`NluQuery` message.

    .. admonition:: MQTT message

      Topic
        ``hermes/nlu/intentParsed``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - input
            - String
            - The user input that has generated this intent.
          * - intent
            - JSON object
            - Structured description of the intent classification.
          * - siteId
            - String
            - Site where the user interaction took place.
          * - id
            - String (optional)
            - The request identifier from the NLU query (:class:`NluQuery`), if any.
          * - slots
            - List of JSON objects (optional)
            - Structured description of the detected slots for this intent, if any.
          * - sessionId
            - String (optional)
            - Session id of the intent detection. The client code must use it to continue
              (:class:`rhasspyhermes.dialogue.DialogueContinueSession`) or end (:class:`rhasspyhermes.dialogue.DialogueEndSession`) the session.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/nlu/intentParsed'

    Note
    ----

    This is a low-level message. It preceeds the full intent message,
    :class:`NluIntent`. To detect a specific intent parsed by the NLU component,
    it is recommended to subscribe to the latter message type.
    """

    input: str
    """The user input that has generated this intent."""
    intent: Intent
    """Structured description of the intent classification."""
    site_id: str = "default"
    """Site where the user interaction took place.

    Note
    ----

    In contrast to the Snips Hermes protocol, the site id is compulsory.
    """
    id: typing.Optional[str] = None
    """The request identifier from the NLU query (:class:`NluQuery`), if any."""
    slots: typing.Optional[typing.List[Slot]] = None
    """Structured description of the detected slots for this intent, if any."""
    session_id: typing.Optional[str] = None
    """Session id of the intent detection. The client code must use it to continue
    (:class:`rhasspyhermes.dialogue.DialogueContinueSession`) or end (:class:`rhasspyhermes.dialogue.DialogueEndSession`) the session."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/nlu/intentParsed"``
        """
        return "hermes/nlu/intentParsed"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AsrTokenTime:
    """The time when an ASR token was detected."""

    start: float
    """Start time (in seconds) of token relative to beginning of utterance."""
    end: float
    """End time (in seconds) of token relative to beginning of utterance."""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AsrToken:
    """A token from an automated speech recognizer."""

    value: str
    """Text value of the token."""
    confidence: float
    """Confidence score of the token, between 0 and 1 (1 being confident)."""
    range_start: int
    """The start of the range in which the token is in the original input."""
    range_end: int
    """The end of the range in which the token is in the original input."""
    time: typing.Optional[AsrTokenTime] = None
    """Structured time when this token was detected."""


@dataclass
class NluIntent(Message):
    """Recognized intent.

    This is the main Rhasspy Hermes message an intent handler should subscribe to.
    It is sent by the dialogue manager when an intent has been detected.

    It's the intent handler's responsibility to inform the dialogue manager of what it
    should do with the current session. The handler should either send a :class:`rhasspyhermes.dialogue.DialogueContinueSession`
    or a :class:`rhasspyhermes.dialogue.DialogueEndSession` message with the current session id.

    .. admonition:: MQTT message

      Topic
        ``hermes/intent/<intentName>``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - input
            - String
            - The user input that has generated this intent.
          * - intent
            - JSON object
            - Structured description of the intent classification.
          * - siteId
            - String
            - Site where the user interaction took place. Defaults to ``"default"``.
          * - id
            - String (optional)
            - The request identifier from the NLU query (:class:`NluQuery`), if any.
          * - slots
            - List of JSON objects (optional)
            - Structured description of the detected slots for this intent, if any.
          * - sessionId
            - String (optional)
            - Session id of the intent detection. The client code must use it to continue
              (:class:`rhasspyhermes.dialogue.DialogueContinueSession`) or end (:class:`rhasspyhermes.dialogue.DialogueEndSession`) the session.
          * - customData
            - String (optional)
            - Custom data provided by message that started (:class:`rhasspyhermes.dialogue.DialogueStartSession`),
              continued (:class:`rhasspyhermes.dialogue.DialogueContinueSession`) or
              ended (:class:`rhasspyhermes.dialogue.DialogueEndSession`) the session.
          * - asrTokens
            - List of list of JSON objects (optional)
            - Structured description of the tokens the ASR captured for this intent.
              The first level of lists represents each invocation of the ASR, the second
              level represents the captured tokens in that invocation.
          * - asrConfidence
            - Number (optional)
            - Speech recognizer confidence score between 0 and 1 (1 being sure).

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/intent/<intentName>'

      Replace ``<intentName>`` by the name of the intent you're interested in.
      You can use the MQTT wildcard ``#`` is you want to receive all intents.

    Example
    -------

    >>> from rhasspyhermes.nlu import NluIntent
    >>> from rhasspyhermes.intent import Intent
    >>> nlu_intent = NluIntent("what time is it", Intent(intent_name="GetTime", confidence_score=0.95))
    >>> nlu_intent.payload()
    '{"input": "what time is it", "intent": {"intentName": "GetTime", "confidenceScore": 0.95}, "siteId": "default", "id": null, "slots": null, "sessionId": null, "customData": null, "asrTokens": null, "asrConfidence": null, "rawInput": null, "wakewordId": null, "lang": null}'
    """

    TOPIC_PATTERN = re.compile(r"^hermes/intent/(.+)$")

    input: str
    """The user input that has generated this intent."""
    intent: Intent
    """Structured description of the intent classification."""
    site_id: str = "default"
    """Site where the user interaction took place."""
    id: typing.Optional[str] = None
    """Request id from the NLU query (:class:`NluQuery`), if any.

    Note
    ----

    This is a Rhasspy-only attribute."""
    slots: typing.Optional[typing.List[Slot]] = None
    """Structured description of the detected slots for this intent, if any."""
    session_id: typing.Optional[str] = None
    """Session id of the intent detection. The client code must use it to continue
    (:class:`rhasspyhermes.dialogue.DialogueContinueSession`) or end (:class:`rhasspyhermes.dialogue.DialogueEndSession`) the session.

    Note
    ----

    In contrast to the Snips Hermes protocol, the session id is optional."""
    custom_data: typing.Optional[str] = None
    """Custom data provided by message that started (:class:`rhasspyhermes.dialogue.DialogueStartSession`),
    continued (:class:`rhasspyhermes.dialogue.DialogueContinueSession`) or
    ended (:class:`rhasspyhermes.dialogue.DialogueEndSession`) the session."""
    asr_tokens: typing.Optional[typing.List[typing.List[AsrToken]]] = None
    """Structured description of the tokens the ASR captured for this intent.
    The first level of lists represents each invocation of the ASR, the second
    level represents the captured tokens in that invocation."""
    asr_confidence: typing.Optional[float] = None
    """Speech recognizer confidence score between 0 and 1 (1 being sure)."""

    # ------------
    # Rhasspy only
    # ------------

    raw_input: typing.Optional[str] = None
    """Original query input before substitutions, such as number replacement.

    Note
    ----

    This is a Rhasspy-only attribute."""
    wakeword_id: typing.Optional[str] = None
    """Id of the wake word that triggered this session.

    Note
    ----

    This is a Rhasspy-only attribute."""
    lang: typing.Optional[str] = None
    """Language of the session.

    Note
    ----

    This is a Rhasspy-only attribute."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for a message of this type with intent name ``intent_name``.

        Returns
        -------
        str
            ``"hermes/intent/{intent_name}"``

        Example
        -------

        >>> from rhasspyhermes.nlu import NluIntent
        >>> NluIntent.topic()
        'hermes/intent/#'
        >>> NluIntent.topic(intent_name="GetTime")
        'hermes/intent/GetTime'
        """
        intent_name = kwargs.get("intent_name", "#")
        return f"hermes/intent/{intent_name}"

    @classmethod
    def get_intent_name(cls, topic: str) -> str:
        """Get intent_name from a topic."""
        match = re.match(NluIntent.TOPIC_PATTERN, topic)
        assert match, "Not an intent topic"
        return match.group(1)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template."""
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

    .. admonition:: MQTT message

      Topic
        ``hermes/nlu/intentNotRecognized``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - input
            - String
            - The user input, if any, that generated this event.
          * - siteId
            - String
            - Site where the user interaction took place. Defaults to ``"default"``.
          * - id
            - String (optional)
            - The request identifier from the NLU query (:class:`NluQuery`), if any.
          * - customData
            - String (optional)
            - Custom data provided by message that started (:class:`rhasspyhermes.dialogue.DialogueStartSession`),
              continued (:class:`rhasspyhermes.dialogue.DialogueContinueSession`) or
              ended (:class:`rhasspyhermes.dialogue.DialogueEndSession`) the session.
          * - sessionId
            - String (optional)
            - Session id of the intent detection. The client code must use it to continue
              (:class:`rhasspyhermes.dialogue.DialogueContinueSession`) or end (:class:`rhasspyhermes.dialogue.DialogueEndSession`) the session.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/nlu/intentNotRecognized'
    """

    input: str
    """The input, if any, that generated this event."""
    site_id: str = "default"
    """Site where the user interaction took place.

    Note
    ----

    In contrast to the Snips Hermes protocol, the site id is compulsory.
    """
    id: typing.Optional[str] = None
    """Request id from NLU query, if any."""
    custom_data: typing.Optional[str] = None
    """Custom data provided by message that started (:class:`rhasspyhermes.dialogue.DialogueStartSession`),
    continued (:class:`rhasspyhermes.dialogue.DialogueContinueSession`) or
    ended (:class:`rhasspyhermes.dialogue.DialogueEndSession`) the session."""
    session_id: typing.Optional[str] = None
    """Session identifier of the session that generated this intent not recognized event."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/nlu/intentNotRecognized"``
        """
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
    """This message is published by the NLU component if an error has occurred.

    .. admonition:: MQTT message

      Topic
        ``hermes/error/nlu``

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
            - Site where the error occurred. Defaults to ``"default"``.
          * - context
            - String (optional)
            - Additional information on the context in which the error occurred.
          * - sessionId
            - String (optional)
            - Session id, if there is an active session.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/error/nlu'

    Example
    -------

    >>> from rhasspyhermes.nlu import NluError
    >>> nlu_error = NluError(error="Unexpected error")
    >>> nlu_error.topic()
    'hermes/error/nlu'
    >>> nlu_error.payload()
    '{"error": "Unexpected error", "siteId": "default", "context": null, "sessionId": null}'
    """

    error: str
    """A description of the error that occurred."""
    site_id: str = "default"
    """The id of the site where the error occurred. Defaults to ``"default"``.

    Note
    ----

    In contrast to the Snips Hermes protocol, the site id is compulsory.
    """
    context: typing.Optional[str] = None
    """Additional information on the context in which the error occurred."""
    session_id: typing.Optional[str] = None
    """The id of the session, if there is an active session."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message.

        Returns
        -------
        str
            ``"hermes/error/nlu"``
        """
        return "hermes/error/nlu"


# ----------------------------------------------------------------------------
# Rhasspy-specific Messages
# ----------------------------------------------------------------------------


@dataclass
class NluTrain(Message):
    """Request to retrain NLU from intent graph.

    .. admonition:: MQTT message

      Topic
        ``rhasspy/nlu/<siteId>/train``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - graphPath
            - String
            - Path to the graph file.
          * - id
            - String (optional)
            - Unique id for the training request. Appended to reply topic (:class:`NluTrainSuccess`).
          * - graphFormat
            - String (optional)
            - Format of the graph file.
          * - sentences
            - Dictionary (optional)
            - TODO
          * - slots
            - Dictionary (optional)
            - TODO

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        TODO

    Note
    ----

    This is a Rhasspy-only message.
    """

    TOPIC_PATTERN = re.compile(r"^rhasspy/nlu/([^/]+)/train$")

    graph_path: str
    """Path to the graph file."""
    id: typing.Optional[str] = None
    """Unique id for the training request."""
    graph_format: typing.Optional[str] = None
    """Optional format of the graph file."""
    sentences: typing.Optional[typing.Dict[str, str]] = None
    """TODO"""
    slots: typing.Optional[typing.Dict[str, typing.List[str]]] = None
    """TODO"""

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"rhasspy/nlu/{site_id}/train"``
        """
        site_id = kwargs.get("site_id", "+")
        return f"rhasspy/nlu/{site_id}/train"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template."""
        return re.match(NluTrain.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from a topic."""
        match = re.match(NluTrain.TOPIC_PATTERN, topic)
        assert match, "Not a train topic"
        return match.group(1)


@dataclass
class NluTrainSuccess(Message):
    """Result from successful training.

    .. admonition:: MQTT message

      Topic
        ``rhasspy/nlu/<siteId>/trainSuccess``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - id
            - String (optional)
            - Unique id from the training request (:class:`NluTrain`).

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'rhasspy/nlu/<siteId>/trainSuccess'

    Note
    ----

    This is a Rhasspy-only message.
    """

    TOPIC_PATTERN = re.compile(r"^rhasspy/nlu/([^/]+)/trainSuccess$")

    id: typing.Optional[str] = None
    """Unique id from training request."""

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"rhasspy/nlu/{site_id}/trainSuccess"``
        """
        site_id = kwargs.get("site_id", "+")
        return f"rhasspy/nlu/{site_id}/trainSuccess"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(NluTrainSuccess.TOPIC_PATTERN, topic) is not None

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from a topic."""
        match = re.match(NluTrainSuccess.TOPIC_PATTERN, topic)
        assert match, "Not a trainSuccess topic"
        return match.group(1)
