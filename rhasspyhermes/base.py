"""Support for Snips Hermes protocol."""
import dataclasses
import json
import typing

from . import utils


class Message:
    """Base class for Hermes messages."""

    def __init__(self, **kwargs):
        pass

    def asdict(self) -> typing.Dict[str, typing.Any]:
        """Convert message to dict."""
        return dataclasses.asdict(self)

    def payload(self) -> typing.Union[str, bytes]:
        """Get binary/string for this message."""
        if dataclasses.is_dataclass(self):
            return json.dumps(self.asdict(), default=str)

        return json.dumps(self.__dict__, default=str)

    @classmethod
    def get_siteId(cls, topic: str) -> typing.Optional[str]:
        """Extract siteId from message topic."""
        return None

    @classmethod
    def get_sessionId(cls, topic: str) -> typing.Optional[str]:
        """Extract sessionId from message topic."""
        return None

    @classmethod
    def is_binary_payload(cls) -> bool:
        """True if message payload is not JSON."""
        return False

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """True if siteId is part of topic."""
        return False

    @classmethod
    def is_session_in_topic(cls) -> bool:
        """True if sessionId is part of topic."""
        return False

    @classmethod
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
