"""Messages for looking up/guessing word pronunciations."""
import typing
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

from rhasspyhermes.base import Message


@dataclass
class G2pPronounce(Message):
    """Get phonetic pronunciation for words.

    The response is sent in a :class:`G2pPhonemes` message.

    .. admonition:: MQTT message

      Topic
        ``rhasspy/g2p/pronounce``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - words
            - List of Strings
            - Words to guess pronunciations for.
          * - id
            - String (optional)
            - Unique id for request. Appended to reply topic (:class:`G2pPhonemes`).
          * - siteId
            - String
            - The id of the site where pronunciations were requested. Defaults to ``"default"``.
          * - sessionId
            - String (optional)
            - Id of active session, if there is one.
          * - numGuesses
            - Integer
            - Maximum number of guesses to return for words not in dictionary. Defaults to 5.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'rhasspy/g2p/pronounce' -m '{"words": ["word", "sentence"], "id": "test", "siteId": "default", "sessionId": null, "numGuesses": 5}'

    Example
    -------

    >>> from rhasspyhermes.g2p import G2pPronounce
    >>> p = G2pPronounce(words=["word", "sentence"], id="test")
    >>> p.payload()
    '{"words": ["word", "sentence"], "id": "test", "siteId": "default", "sessionId": null, "numGuesses": 5}'
    >>> p.topic()
    'rhasspy/g2p/pronounce'

    Note
    ----

    This is a Rhasspy-only message."""

    words: typing.List[str]
    """Words to guess pronunciations for."""
    id: typing.Optional[str] = None
    """Unique id for request. Appended to reply topic (:class:`G2pPhonemes`)."""
    site_id: str = "default"
    """Id of site to request pronunciations from."""
    session_id: typing.Optional[str] = None
    """Id of active session, if there is one."""
    num_guesses: int = 5
    """Maximum number of guesses to return for words not in dictionary."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"rhasspy/g2p/pronounce"``
        """
        return "rhasspy/g2p/pronounce"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class G2pPronunciation:
    """Phonetic pronunciation for a single word."""

    phonemes: typing.List[str]
    """Phonetic pronunciation for word."""
    guessed: typing.Optional[bool] = None
    """``True`` if this pronunciation was guessed using a g2p model.
    ``False`` if it came from a pronunciation dictionary."""


@dataclass
class G2pPhonemes(Message):
    """Response to :class:`G2pPronounce`.

    .. admonition:: MQTT message

      Topic
        ``rhasspy/g2p/phonemes``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - wordPhonemes
            - Dictionary
            - Guessed or looked up pronunciations.
          * - id
            - String (optional)
            - Unique id for a :class:`G2pPronounce` request.
          * - siteId
            - String
            - The id of the site where pronunciations were requested. Defaults to ``"default"``.
          * - sessionId
            - String (optional)
            - Id of active session, if there is one.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -t 'rhasspy/g2p/phonemes' -v

    Note
    ----

    This is a Rhasspy-only message."""

    word_phonemes: typing.Dict[str, typing.List[G2pPronunciation]]
    """Guessed or looked up pronunciations."""
    id: typing.Optional[str] = None
    """Unique id from a :class:`G2pPronounce` request."""
    site_id: str = "default"
    """Id of site where pronunciations were requested."""
    session_id: typing.Optional[str] = None
    """Id of active session, if there is one."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"rhasspy/g2p/phonemes"``

        """
        return "rhasspy/g2p/phonemes"


@dataclass
class G2pError(Message):
    """Error from G2P component.

    .. admonition:: MQTT message

      Topic
        ``rhasspy/error/g2p``

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
            - String
            - Additional information on the context in which the error occurred.
          * - sessionId
            - String (optional)
            - Id of active session, if there is one.

      Subscribe to this message type with ``mosquitto_sub``:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -t 'rhasspy/error/g2p' -v

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
            ``"rhasspy/error/g2p"``
        """
        return "rhasspy/error/g2p"
