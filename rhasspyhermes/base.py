"""Support for Snips Hermes protocol."""
import typing
from abc import ABC, abstractmethod

import attr


class Message(ABC):
    """Base class for Hermes messages."""

    @classmethod
    @abstractmethod
    def topic(cls, *args, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        pass
