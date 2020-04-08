"""Messages for intent handling."""
from dataclasses import dataclass

from .base import Message


@dataclass
class HandleToggleOn(Message):
    """Enable intent handling.

    Attributes
    ----------
    site_id: str = "default"
        Id of site to enable intent handling
    """

    site_id: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for message."""
        return "rhasspy/handle/toggleOn"


@dataclass
class HandleToggleOff(Message):
    """Disable intent handling.

    Attributes
    ----------
    site_id: str = "default"
        Id of site to disable intent handling
    """

    site_id: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for message."""
        return "rhasspy/handle/toggleOff"
