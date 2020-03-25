"""Messages for rhasspy/g2p"""
import typing
from dataclasses import dataclass, field

from rhasspyhermes.base import Message


@dataclass
class G2pPronounce(Message):
    """Get phonetic pronunciation for words."""

    # User id that will be returned in response
    id: str = ""

    # Words to guess pronunciations for
    words: typing.List[str] = field(default_factory=list)

    # Hermes siteId/sessionId
    siteId: str = "default"
    sessionId: str = ""

    # Maximum number of guesses to return
    numGuesses: int = 5

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/g2p/pronounce"


@dataclass
class G2pPronunciation:
    """Phonetic pronunciation for a single word (in G2pPhonemes)."""

    # Phonetic pronunciation for word
    phonemes: typing.List[str] = field(default_factory=list)

    # True if this pronunciation was guessed using a g2p model.
    # False if it came from a pronunciation dictionary.
    guessed: bool = False


@dataclass
class G2pPhonemes(Message):
    """Response to G2pPronunciation."""

    # Guessed or looked up pronunciations
    wordPhonemes: typing.Dict[str, typing.List[G2pPronunciation]] = field(
        default_factory=dict
    )

    # User id from request
    id: str = ""

    # Hermes siteId/sessionId
    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/g2p/phonemes"

    @classmethod
    def from_dict(cls, message_dict: typing.Dict[str, typing.Any]):
        """Construct message from dictionary."""
        message_dict = cls.only_fields(message_dict)
        word_phonemes = message_dict.pop("wordPhonemes", {})
        message = G2pPhonemes(**message_dict)
        message.wordPhonemes = {
            word: [G2pPronunciation(**word_pron) for word_pron in word_phonemes[word]]
            for word in word_phonemes
        }

        return message


@dataclass
class G2pError(Message):
    """Error from G2P component."""

    error: str
    context: str = ""
    id: str = ""
    siteId: str = "default"
    sessionId: str = ""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/error/g2p"
