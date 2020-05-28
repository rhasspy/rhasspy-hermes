"""Messages for training."""
import re
import typing
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json

from .base import Message


@dataclass
class IntentGraphRequest(Message):
    """Request publication of intent graph from training.

    Attributes
    ----------
    id: str
        Unique id for request. Appended to reply topic.

    site_id: str = "default"
        The id of the site where training occurred
    """

    id: str
    site_id: str = "default"

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        return "rhasspy/train/getIntentGraph"


@dataclass
class IntentGraph(Message):
    """Intent graph from training.

    Attributes
    ----------
    graph_bytes: bytes
        Gzipped pickle bytes containing networkx intent graph
    """

    TOPIC_PATTERN = re.compile(r"^rhasspy/train/intentGraph/([^/]+)$")

    graph_bytes: bytes

    def payload(self) -> typing.Union[str, bytes]:
        """Get binary/string for this message."""
        return self.graph_bytes

    @classmethod
    def is_binary_payload(cls) -> bool:
        """True if payload is not JSON."""
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type."""
        request_id = kwargs.get("request_id", "#")
        return f"rhasspy/train/intentGraph/{request_id}"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """True if topic matches template"""
        return re.match(IntentGraph.TOPIC_PATTERN, topic) is not None
