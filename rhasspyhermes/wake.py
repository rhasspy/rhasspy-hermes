"""Messages for wake word detection."""
import re
import typing
from dataclasses import dataclass
from enum import Enum

from dataclasses_json import LetterCase, dataclass_json

from .base import Message


class HotwordToggleReason(str, Enum):
    """Reason for hotword toggle on/off."""

    UNKNOWN = ""
    """Overrides all other reasons."""
    DIALOGUE_SESSION = "dialogueSession"
    """Dialogue session is active."""
    PLAY_AUDIO = "playAudio"
    """Audio is currently playing."""
    TTS_SAY = "ttsSay"
    """Text to speech system is currently speaking."""


@dataclass
class HotwordToggleOn(Message):
    """Activate the wake word component, so pronouncing a wake word will trigger a
    :class:`HotwordDetected` message.

    .. admonition:: MQTT message

      Topic
        ``hermes/hotword/toggleOn``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - siteId
            - String
            - The id of the site where the wake word component should be enabled.
          * - reason
            - String
            - The reason for enabling the wake word component.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'hermes/hotword/toggleOn' -m '{"siteId": "default", "reason": "dialogueSession"}'
    """

    site_id: str = "default"
    """The id of the site where the wake word component should be enabled."""

    # ------------
    # Rhasspy only
    # ------------

    reason: HotwordToggleReason = HotwordToggleReason.UNKNOWN
    """The reason for enabling the wake word component.

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
            ``"hermes/hotword/toggleOn"``
        """
        return "hermes/hotword/toggleOn"


@dataclass
class HotwordToggleOff(Message):
    """Deactivate the wake word component, so pronouncing a wake word won't trigger a
    :class:`HotwordDetected` message.

    .. admonition:: MQTT message

      Topic
        ``hermes/hotword/toggleOff``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - siteId
            - String
            - The id of the site where the wake word component should be disabled.
          * - reason
            - String
            - The reason for disabling the wake word component.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'hermes/hotword/toggleOff' -m '{"siteId": "default", "reason": "dialogueSession"}'
    """

    site_id: str = "default"
    """The id of the site where the wake word component should be disabled."""

    # ------------
    # Rhasspy only
    # ------------

    reason: HotwordToggleReason = HotwordToggleReason.UNKNOWN
    """The reason for disabling the wake word component.

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
            ``"hermes/hotword/toggleOff"``
        """
        return "hermes/hotword/toggleOff"


@dataclass
class HotwordDetected(Message):
    """Message sent by the wake word component when it has detected a specific wake word.

    .. admonition:: MQTT message

      Topic
        ``hermes/hotword/<WAKEWORD_ID>/detected``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - modelId
            - String
            - The id of the model that triggered the wake word.
          * - modelVersion
            - String
            - The version of the model.
          * - modelType
            - String
            - The type of the model. Possible values are ``"universal"`` and ``"personal"``.
          * - currentSensitivity
            - Float
            - The sensitivity configured in the model at the time of the detection.
          * - siteId
            - String
            - The id of the site where the wake word component should be disabled.
          * - sessionId
            - String (optional)
            - The id of the dialogue session created after detection.
          * - send_audio_captured
            - Boolean (optional)
            - ``True`` if audio captured from the ASR should be emitted on
              ``rhasspy/asr/{site_id}/{session_id}/audioCaptured``.
          * - lang
            - String (optional)
            - Language of the detected wake word.
              Copied by the dialogue manager into subsequent ASR and NLU messages.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/hotword/default/detected'
    """

    TOPIC_PATTERN = re.compile(r"^hermes/hotword/([^/]+)/detected$")

    model_id: str
    """The id of the model that triggered the wake word."""
    model_version: str = ""
    """The version of the model."""
    model_type: str = "personal"
    """The type of the model. Possible values are ``"universal"`` and ``"personal"``."""
    current_sensitivity: float = 1.0
    """The sensitivity configured in the model at the time of the detection."""
    site_id: str = "default"
    """The id of the site where the wake word was detected."""

    # ------------
    # Rhasspy only
    # ------------

    session_id: typing.Optional[str] = None
    """The desired id of the dialogue session created after detection.
    Leave empty to have one auto-generated.

    Note
    ----

    This is a Rhasspy-only attribute.
    """
    send_audio_captured: typing.Optional[bool] = None
    """``True`` if audio captured from the ASR should be emitted on
    ``rhasspy/asr/{site_id}/{session_id}/audioCaptured``.

    Note
    ----

    This is a Rhasspy-only attribute.
    """
    lang: typing.Optional[str] = None
    """Language of the detected wake word.
    Copied by the dialogue manager into subsequent ASR and NLU messages.

    Note
    ----

    This is a Rhasspy-only attribute.
    """

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Arguments
        ---------
        wakeword_id: str
            The id of the wake word.

        Returns
        -------
        str
            MQTT topic for this message type with the given wake word id.

        Example
        -------
        >>> from rhasspyhermes.wake import HotwordDetected
        >>> HotwordDetected.topic(wakeword_id="example-02.wav")
        'hermes/hotword/example-02.wav/detected'
        """
        wakeword_id = kwargs.get("wakeword_id", "+")
        return f"hermes/hotword/{wakeword_id}/detected"

    @classmethod
    def get_wakeword_id(cls, topic: str) -> str:
        """Get wakeword id from MQTT topic.

        Arguments
        ---------
        topic
            MQTT topic.

        Returns
        -------
        str
            Wake word ID extracted from the MQTT topic.

        Example
        -------
        >>> from rhasspyhermes.wake import HotwordDetected
        >>> HotwordDetected.get_wakeword_id("hermes/hotword/example-02.wav/detected")
        'example-02.wav'
        """
        match = re.match(HotwordDetected.TOPIC_PATTERN, topic)
        assert match, "Not a detected topic"
        return match.group(1)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template."""
        return re.match(HotwordDetected.TOPIC_PATTERN, topic) is not None


# -----------------------------------------------------------------------------
# Rhasspy Only Messages
# -----------------------------------------------------------------------------


@dataclass
class HotwordError(Message):
    """Error from wake word component.

    .. admonition:: MQTT message

      Topic
        ``hermes/error/hotword``

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

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/error/hotword'

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
            ``"hermes/error/hotword"``
        """
        return "hermes/error/hotword"


@dataclass
class GetHotwords(Message):
    """Request to list available hotwords. The wake word component responds with a
    :class:`Hotwords` message.

    .. admonition:: MQTT message

      Topic
        ``rhasspy/hotword/getHotwords``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - siteId
            - String
            - The id of the site where the wake word component exists.
          * - id
            - String (optional)
            - Unique id passed to the response in the :class:`Hotwords` message.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'rhasspy/hotword/getHotwords' -m '{"siteId": "default", "id": "foobar"}'

    Note
    ----

    This is a Rhasspy-only message.
    """

    site_id: str = "default"
    """The id of the site where the wake word component exists."""
    id: typing.Optional[str] = None
    """Unique id passed to the response in the :class:`Hotwords` message."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"rhasspy/hotword/getHotwords"``
        """
        return "rhasspy/hotword/getHotwords"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Hotword:
    """Description of a single hotword."""

    model_id: str
    """Unique ID of hotword model."""
    model_words: str
    """Actual words used to activate hotword."""
    model_version: str = ""
    """Model version."""
    model_type: str = "personal"
    """Model type (personal, unversal)."""


@dataclass
class Hotwords(Message):
    """The list of available hotwords. The wake word component sends this message
    in response to a request in a :class:`GetHotwords` message.

    .. admonition:: MQTT message

      Topic
        ``rhasspy/hotword/hotwords``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - models
            - List of JSON objects
            - The list of available hotwords.
          * - siteId
            - String
            - The id of the site where hotwords were requested.
          * - id
            - String (optional)
            - Unique id passed from the request in the :class:`GetHotwords` message.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'rhasspy/hotword/hotwords'

    Note
    ----

    This is a Rhasspy-only message.
    """

    models: typing.List[Hotword]
    """The list of available hotwords."""
    site_id: str = "default"
    """The id of the site where hotwords were requested."""
    id: typing.Optional[str] = None
    """Unique id passed from the request in the :class:`GetHotwords` message."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"rhasspy/hotword/hotwords"``
        """
        return "rhasspy/hotword/hotwords"


@dataclass
class RecordHotwordExample(Message):
    """Request to record examples of a hotword. The wake word component responds with a
    :class:`HotwordExampleRecorded` message.

    .. admonition:: MQTT message

      Topic
        ``rhasspy/hotword/recordExample``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - id
            - String
            - Unique id used in the response message (:class:`HotwordExampleRecorded`).
          * - siteId
            - String
            - The id of the site where the wake word component exists.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'rhasspy/hotword/recordExample' -m '{"siteId": "default", "id": "foobar"}'

    Note
    ----

    This is a Rhasspy-only message.
    """

    id: str
    """Unique id used in the response message (:class:`HotwordExampleRecorded`)."""
    site_id: str = "default"
    """The id of the site where the wake word component exists."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"rhasspy/hotword/recordExample"``
        """
        return "rhasspy/hotword/recordExample"


@dataclass
class HotwordExampleRecorded(Message):
    """Response when a hotword example has been recorded. Sent by the wake word component
    in response to a :class:`RecordHotwordExample` message.

    .. admonition:: MQTT message

      Topic
        ``rhasspy/hotword/<SITE_ID>/exampleRecorded/<REQUEST_ID>``

      Payload (binary)
        Audio from the recorded sample in WAV format.

      Subscribe to this message type with ``mosquitto_sub`` and show the binary payload as hexadecimal numbers:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -t 'rhasspy/hotword/<SITE_ID>/exampleRecorded/<REQUEST_ID>' -F %x

    Note
    ----

    This is a Rhasspy-only message.
    """

    TOPIC_PATTERN = re.compile(r"^rhasspy/hotword/([^/]+)/exampleRecorded/([^/]+)$")

    wav_bytes: bytes
    """Audio from recorded sample in WAV format."""

    def payload(self) -> typing.Union[str, bytes]:
        """Get binary/string for this message."""
        return self.wav_bytes

    @classmethod
    def is_binary_payload(cls) -> bool:
        """True if payload is not JSON.

        Returns
        -------
        bool
            ``True``
        """
        return True

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is in topic.

        Returns
        -------
        bool
            ``True``
        """
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Arguments
        ---------
        site_id: str
            The id of the site where the wake word component exists.
        request_id: str
            Unique id of the request message.

        Returns
        -------
        str
            MQTT topic for this message type with the given site id and request id.

        Example
        -------
        >>> from rhasspyhermes.wake import HotwordExampleRecorded
        >>> HotwordExampleRecorded.topic(site_id="default", request_id="foobar")
        'rhasspy/hotword/default/exampleRecorded/foobar'
        """
        site_id = kwargs.get("site_id", "+")
        request_id = kwargs.get("request_id", "#")
        return f"rhasspy/hotword/{site_id}/exampleRecorded/{request_id}"

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Get site id from MQTT topic.

        Arguments
        ---------
        topic
            MQTT topic.

        Returns
        -------
        str
            Site ID extracted from the MQTT topic.

        Example
        -------
        >>> from rhasspyhermes.wake import HotwordExampleRecorded
        >>> HotwordExampleRecorded.get_site_id("rhasspy/hotword/default/exampleRecorded/foobar")
        'default'
        """
        match = re.match(HotwordExampleRecorded.TOPIC_PATTERN, topic)
        assert match, "Not an exampleRecorded topic"
        return match.group(1)

    @classmethod
    def get_request_id(cls, topic: str) -> str:
        """Get request id from MQTT topic.

        Arguments
        ---------
        topic
            MQTT topic.

        Returns
        -------
        str
            Request ID extracted from the MQTT topic.

        Example
        -------
        >>> from rhasspyhermes.wake import HotwordExampleRecorded
        >>> HotwordExampleRecorded.get_request_id("rhasspy/hotword/default/exampleRecorded/foobar")
        'foobar'
        """
        match = re.match(HotwordExampleRecorded.TOPIC_PATTERN, topic)
        assert match, "Not an exampleRecorded topic"
        return match.group(2)

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(HotwordExampleRecorded.TOPIC_PATTERN, topic) is not None
