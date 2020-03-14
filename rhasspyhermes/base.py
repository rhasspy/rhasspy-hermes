"""Support for Snips Hermes protocol."""
import typing
from abc import ABC, abstractmethod

from . import utils


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
        return cls(**utils.only_fields(cls, message_dict))

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic is for this message type."""
        return topic == cls.topic()

    @classmethod
    def only_fields(
        cls, message_dict: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        """Return dict with only valid fields."""
        return utils.only_fields(cls, message_dict)
