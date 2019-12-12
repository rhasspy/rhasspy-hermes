"""Support for Snips Hermes protocol."""
from abc import ABC, abstractmethod


class Message(ABC):
    """Base class for Hermes messages."""

    @classmethod
    @abstractmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        pass
