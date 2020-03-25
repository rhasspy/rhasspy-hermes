"""Messages for rhasspy/handle"""
from dataclasses import dataclass

from .base import Message


@dataclass
class HandleToggleOn(Message):
    """Enable intent handling."""

    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "rhasspy/handle/toggleOn"


@dataclass
class HandleToggleOff(Message):
    """Disable intent handling."""

    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "rhasspy/handle/toggleOff"
