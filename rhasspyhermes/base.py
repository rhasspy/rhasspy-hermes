"""Support for Snips Hermes protocol."""
import typing
from abc import ABC, abstractmethod

import attr


class Message(ABC):
    """Base class for Hermes messages."""

    @abstractmethod
    def topic(self, siteId: str, sessionId: str, **kwargs) -> str:
        """Get MQTT topic for this message."""
        pass
