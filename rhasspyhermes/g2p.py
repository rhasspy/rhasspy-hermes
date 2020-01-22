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
    words: [str] = attr.ib(default="")

    # Hermes siteId/sessionId
    siteId: str = attr.ib(default="default")
    sessionId: str = attr.ib(default="")

    # G2P models to use when guessing.
    # None = don't guess (only dictionaries)
    # Empty = use all available models
    # Non-empty = use specific models
    models: typing.Optional[typing.List[str]] = attr.ib(factory=list)

    # Pronunciation dictionaries to use.
    # None = don't use a dictionary (only guess)
    # Empty = use all available dictionaries
    # Non-Empty = use only specific dictionaries
    dictionaries: typing.Optional[typing.List[str]] = attr.ib(factory=list)

    # Maximum number of guesses to return
    numGuesses: int = attr.ib(default=5)

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic"""
        return "rhasspy/g2p/pronounce"


@attr.s
class G2pPronunciation:
    """Phonetic pronunciation for a single word"""

    word: str = attr.ib()

    # Phonetic pronunciation for word
    phonemes: typing.List[str] = attr.ib()

    # G2P model id used to guess pronunciation
    modelId: typing.Optional[str] = attr.ib(default=None)

    # Phonetic dictionary used for pronunciation
    dictionaryId: typing.Optional[str] = attr.ib(default=None)


@attr.s
class G2pPhonemes:
    """Phonetic pronunciations for words."""

    # Guessed or looked up pronunciations
    phonemes: typing.Dict[str, typing.List[G2pPronunciation]] = attr.ib()

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
