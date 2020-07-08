"""Rhasspy-only messages for intent training."""
import re
from dataclasses import dataclass

from .base import Message


@dataclass
class IntentGraphRequest(Message):
    """Request publication of intent graph from training.

    .. admonition:: MQTT message

      Topic
        ``rhasspy/train/getIntentGraph``

      Payload (JSON)
        .. list-table::
          :widths: 10 10 80
          :header-rows: 1

          * - Key
            - Type
            - Description
          * - id
            - String
            - Unique id for request. Appended to reply topic (:class:`IntentGraph`).
          * - siteId
            - String
            - The id of the site where training occurred. Defaults to ``"default"``.

      Publish this message type with ``mosquitto_pub``:

      .. code-block:: shell

        mosquitto_pub -h <HOSTNAME> -t 'rhasspy/train/getIntentGraph' -m '{"id": "abcd", "siteId": "default"}'

    Example
    -------

    >>> from rhasspyhermes.train import IntentGraphRequest
    >>> request = IntentGraphRequest(id='abcd')
    >>> request.payload()
    '{"id": "abcd", "siteId": "default"}'
    >>> request.topic()
    'rhasspy/train/getIntentGraph'

    Note
    ----

    This is a Rhasspy-only message."""

    id: str
    """Unique id for request. Appended to reply topic (:class:`IntentGraph`)."""
    site_id: str = "default"
    """The id of the site where training occurred."""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"rhasspy/train/getIntentGraph"``
        """
        return "rhasspy/train/getIntentGraph"


@dataclass
class IntentGraph(Message):
    """Intent graph from training.

    .. admonition:: MQTT message

      Topic
        ``rhasspy/train/intentGraph``

      Payload (binary)
        gzipped pickle bytes containing a NetworkX_ intent graph

      .. _NetworkX: https://networkx.github.io/

      Subscribe to this message type with ``mosquitto_sub`` and show the binary payload as hexadecimal numbers:

      .. code-block:: shell

        mosquitto_sub -h <HOSTNAME> -t 'rhasspy/train/intentGraph' -F %x

    Note
    ----

    This is a Rhasspy-only message."""

    TOPIC_PATTERN = re.compile(r"^rhasspy/train/intentGraph/([^/]+)$")

    graph_bytes: bytes
    """Gzipped pickle bytes containing a NetworkX intent graph"""

    def payload(self) -> bytes:
        """Get the binary payload for this message.

        Returns
        -------

        bytes
            The binary payload as gzipped pickle bytes containing a NetworkX intent graph.
        """
        return self.graph_bytes

    @classmethod
    def is_binary_payload(cls) -> bool:
        """Check for binary payload of message.

        Returns
        -------
        bool
            ``True``
        """
        return True

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Arguments
        ---------
        request_id: str
            Unique id for request. Supplied in request topic (:class:`IntentGraphRequest`)

        Returns
        -------
        str
            ``"rhasspy/train/intentGraph/{request_id}"``

        Example
        -------

        >>> from rhasspyhermes.train import IntentGraph
        >>> IntentGraph.topic(request_id="abcd")
        'rhasspy/train/intentGraph/abcd'
        """
        request_id = kwargs.get("request_id", "#")
        return f"rhasspy/train/intentGraph/{request_id}"

    @classmethod
    def is_topic(cls, topic: str) -> bool:
        """Check whether topic is for this message type.

        Arguments
        ---------
        topic
            message topic

        Returns
        -------
        bool
            ``True`` if topic is for this message type

        Example
        -------

        >>> from rhasspyhermes.train import IntentGraph
        >>> IntentGraph.is_topic("rhasspy/train/intentGraph/abcd")
        True
        """
        return re.match(IntentGraph.TOPIC_PATTERN, topic) is not None
