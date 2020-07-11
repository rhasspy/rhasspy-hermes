"""Messages for text to speech."""
import typing
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

from .base import Message


@dataclass
class TtsSay(Message):
    """Send text to be spoken by the text to speech component.

    Note
    ----

    This is a low-level message. You should use the dialogue manager's
    :class:`rhasspyhermes.dialogue.DialogueStartSession` or
    :class:`rhasspyhermes.dialogue.DialogueContinueSession`
    messages.


    .. admonition:: MQTT message

      Topic
        ``hermes/tts/say``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - text
            - String
            - The text to be spoken.
          * - siteId
            - String
            - The id of the site where the text should be spoken. Defaults to ``"default"``.
          * - lang
            - String (optional)
            - The language code to use when saying the text.
          * - id
            - String (optional)
            - A request identifier. If provided, it will be passed back in the
              response message :class:`TtsSayFinished`.
          * - sessionId
            - String (optional)
            - The id of the session, if there is an active session.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'hermes/tts/say' -m '{"text": "Ciao!", "lang": "it_IT"}'

    Example
    -------

    >>> from rhasspyhermes.tts import TtsSay
    >>> say = TtsSay(text="Ciao!", lang="it_IT")
    >>> say.topic()
    'hermes/tts/say'
    >>> say.payload()
    '{"text": "Ciao!", "siteId": "default", "lang": "it_IT", "id": null, "sessionId": null}'
    """

    text: str
    """The text to be spoken."""
    site_id: str = "default"
    """The id of the site where the text should be spoken."""
    lang: typing.Optional[str] = None
    """The language code to use when saying the text."""
    id: typing.Optional[str] = None
    """A request identifier. If provided, it will be passed back in the
    response message :class:`TtsSayFinished`."""
    session_id: typing.Optional[str] = None
    """The id of the session, if there is an active session."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/tts/say"``
        """
        return "hermes/tts/say"


@dataclass
class TtsSayFinished(Message):
    """Response published when the text to speech component has finished speaking.

    .. admonition:: MQTT message

      Topic
        ``hermes/tts/sayFinished``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - siteId
            - String
            - The id of the site where the text was spoken. Defaults to ``"default"``.
          * - id
            - String (optional)
            - Identifier from the request (:class:`TtsSay`).
          * - sessionId
            - String (optional)
            - The id of the session, if there is an active session.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/tts/sayFinished'
    """

    site_id: str = "default"
    """The id of the site where the text was spoken. Defaults to ``"default"``."""
    id: typing.Optional[str] = None
    """Identifier from the request (:class:`TtsSay`)."""
    session_id: typing.Optional[str] = None
    """The id of the session, if there is an active session."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/tts/sayFinished"``
        """
        return "hermes/tts/sayFinished"


# -----------------------------------------------------------------------------
# Rhasspy Only
# -----------------------------------------------------------------------------


@dataclass
class GetVoices(Message):
    """Get the available voices for the text to speech system.

    Note
    ----
    This is a Rhasspy-only message.


    .. admonition:: MQTT message

      Topic
        ``hermes/tts/getVoices``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - id
            - String (optional)
            - Unique identifier passed to the response (:class:`Voices`).
          * - siteId
            - String
            - The id of the site to request voices from. Defaults to ``"default"``.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'hermes/tts/getVoices' -m '{"id": "abcd", "siteId": "default"}'

    Example
    -------
    >>> from rhasspyhermes.tts import GetVoices
    >>> g = GetVoices("abcd")
    >>> g.topic()
    'rhasspy/tts/getVoices'
    >>> g.payload()
    '{"id": "abcd", "siteId": "default"}'
    """

    id: typing.Optional[str] = None
    """Unique identifier passed to response (:class:`Voices`)."""
    site_id: str = "default"
    """Id of site to request voices from."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/tts/getVoices"``
        """
        return "rhasspy/tts/getVoices"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Voice:
    """Information about a single TTS voice."""

    voice_id: str
    """Unique identifier for voice."""
    description: typing.Optional[str] = None
    """Human-readable description of voice."""


@dataclass
class Voices(Message):
    """Response with the available voices for the text to speech system.
    This message is published in response to a :class:`GetVoices` request.

    Note
    ----
    This is a Rhasspy-only message.


    .. admonition:: MQTT message

      Topic
        ``hermes/tts/Voices``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - voices
            - List of JSON objects
            - List of available voices.
          * - id
            - String (optional)
            - Unique identifier from the request (:class:`GetVoices`).
          * - siteId
            - String
            - The id of the site where voices were requested. Defaults to ``"default"``.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/tts/voices'

    """

    voices: typing.List[Voice]
    """List of available voices."""
    id: typing.Optional[str] = None
    """Unique identifier from request (:class:`GetVoices`)."""
    site_id: str = "default"
    """Id of site where voices were requested."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"hermes/tts/voices"``
        """
        return "rhasspy/tts/voices"


@dataclass
class TtsError(Message):
    """This message is published by the text to speech system if an error has occurred.

    Note
    ----
    This is a Rhasspy-only message.


    .. admonition:: MQTT message

      Topic
        ``hermes/error/tts``

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
            - The id of the session, if there is an active session.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -v -t 'hermes/error/tts'

    Example
    -------

    >>> from rhasspyhermes.tts import TtsError
    >>> tts_error = TtsError(error="Unexpected error")
    >>> tts_error.topic()
    'hermes/error/tts'
    >>> tts_error.payload()
    '{"error": "Unexpected error", "siteId": "default", "context": null, "sessionId": null}'
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
            ``"hermes/error/tts"``
        """
        return "hermes/error/tts"
