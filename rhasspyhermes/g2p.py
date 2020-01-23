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

    word: str = attr.ib(default="")

    # Phonetic pronunciation for word
    phonemes: typing.List[str] = attr.ib(factory=list)


@attr.s
class G2pPhonemes:
    """Response to G2pPronunciation."""

    # Guessed or looked up pronunciations
    phonemes: typing.Dict[str, typing.List[G2pPronunciation]] = attr.ib(factory=dict)

    # User id from request
    id: str = attr.ib(default="")

    # Hermes siteId/sessionId
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/g2p/phonemes"


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
