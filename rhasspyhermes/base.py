"""Support for Snips Hermes protocol."""
import typing
from abc import ABCMeta

from dataclasses_json import DataClassJsonMixin, LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
class Message(DataClassJsonMixin, metaclass=ABCMeta):
    """Base class for Hermes messages."""

    def __init__(self, **kwargs):
        DataClassJsonMixin.__init__(self, letter_case=LetterCase.CAMEL)

    def payload(self) -> typing.Union[str, bytes]:
        """Get binary/string for this message."""
        return self.to_json()

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Extract site id from message topic."""
        return None

    @classmethod
    def get_session_id(cls, topic: str) -> typing.Optional[str]:
        """Extract session id from message topic."""
        return None

    @classmethod
    def is_binary_payload(cls) -> bool:
        """True if message payload is not JSON."""
        return False

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if site id is part of topic."""
        return False

    @classmethod
    def is_session_in_topic(cls) -> bool:
        """True if session id is part of topic."""
        return False

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic is for this message type."""
        return topic == cls.topic()
