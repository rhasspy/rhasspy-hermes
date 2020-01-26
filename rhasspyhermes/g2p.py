"""Messages for rhasspy/g2p"""
import typing

import attr
from rhasspyhermes.base import Message


@attr.s
class G2pPronounce(Message):
    """Get phonetic pronunciation for words."""

    # User id that will be returned in response
    id: str = attr.ib(default="")

    # Words to guess pronunciations for
    words: typing.List[str] = attr.ib(factory=list)

    # Hermes siteId/sessionId
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    # Maximum number of guesses to return
    numGuesses: int = attr.ib(default=5)

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/g2p/pronounce"


@attr.s
class G2pPronunciation:
    """Phonetic pronunciation for a single word (in G2pPhonemes)."""

    # Phonetic pronunciation for word
    phonemes: typing.List[str] = attr.ib(factory=list)

    # True if this pronunciation was guessed using a g2p model.
    # False if it came from a pronunciation dictionary.
    guessed: bool = attr.ib(default=False)


@attr.s
class G2pPhonemes(Message):
    """Response to G2pPronunciation."""

    # Guessed or looked up pronunciations
    wordPhonemes: typing.Dict[str, typing.List[G2pPronunciation]] = attr.ib(
        factory=dict
    )

    # User id from request
    id: str = attr.ib(default="")

    # Hermes siteId/sessionId
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/g2p/phonemes"

    @classmethod
    def from_dict(cls, message_dict: typing.Dict[str, typing.Any]):
        """Construct message from dictionary."""
        message = super().from_dict(message_dict)
        message.wordPhonemes = {
            word: [
                G2pPronunciation(**word_pron)
                for word_pron in message.wordPhonemes[word]
            ]
            for word in message.wordPhonemes
        }

        return message


@attr.s
class G2pError(Message):
    """Error from G2P component."""

    error: str = attr.ib()
    context: str = attr.ib(default="")
    id: str = attr.ib(default="")
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/error/g2p"
