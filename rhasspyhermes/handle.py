"""Messages for rhasspy/handle"""
import attr

from .base import Message


@attr.s(auto_attribs=True, slots=True)
class HandleToggleOn(Message):
    """Enable intent handling."""

    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "rhasspy/handle/toggleOn"


@attr.s(auto_attribs=True, slots=True)
class HandleToggleOff(Message):
    """Disable intent handling."""

    siteId: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        return "rhasspy/handle/toggleOff"
