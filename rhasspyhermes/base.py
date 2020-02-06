"""Support for Snips Hermes protocol."""
import typing
from abc import ABC, abstractmethod


class Message(ABC):
    """Base class for Hermes messages."""

    def __init__(self, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""

    @classmethod
    def from_dict(cls, message_dict: typing.Dict[str, typing.Any]):
        """Construct message from dictionary."""
        return cls(**message_dict)
