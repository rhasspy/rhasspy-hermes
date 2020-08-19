"""Messages for looking up/guessing word pronunciations."""
import typing
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

from rhasspyhermes.base import Message


@dataclass
class G2pPronounce(Message):
    """Get phonetic pronunciation for words.

    Attributes
    ----------
    id: Optional[str] = None
        Unique id for request

    site_id: str = "default"
        Id of site to request pronunciations from

    words: List[str]
        Words to guess pronunciations for

    session_id: typing.Optional[str] = None
        Id of active session, if there is one

    num_guesses: int = 5
        Maximum number of guesses to return for words not in dictionary
    """

    words: typing.List[str]
    id: typing.Optional[str] = None
    site_id: str = "default"
    session_id: typing.Optional[str] = None
    num_guesses: int = 5

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message."""
        return "rhasspy/g2p/pronounce"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class G2pPronunciation:
    """Phonetic pronunciation for a single word.

    Attributes
    ----------
    phonemes: List[str]
        Phonetic pronunciation for word

    guessed: bool = False
        True if this pronunciation was guessed using a g2p model.
        False if it came from a pronunciation dictionary.
    """

    phonemes: typing.List[str]
    guessed: typing.Optional[bool] = None


@dataclass
class G2pPhonemes(Message):
    """Response to g2p/pronounce.

    Attributes
    ----------
    id: Optional[str] = None
        Unique id from request

    site_id: str = "default"
        Id of site where pronunciations were requested

    word_phonemes: Dict[str, List[G2pPronunciation]]
        Guessed or looked up pronunciations

    session_id: typing.Optional[str] = None
        Id of active session, if there is one
    """

    word_phonemes: typing.Dict[str, typing.List[G2pPronunciation]]
    id: typing.Optional[str] = None
    site_id: str = "default"
    session_id: typing.Optional[str] = None

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message."""
        return "rhasspy/g2p/phonemes"


@dataclass
class G2pError(Message):
    """Error from G2P component.

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
        """Get MQTT topic for this message."""
        return "rhasspy/error/g2p"
