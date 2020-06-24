"""Rhasspy-only messages for intent handling."""
from dataclasses import dataclass

from .base import Message


@dataclass
class HandleToggleOn(Message):
    """Enable intent handling.

    The corresponding MQTT message has the following properties:

    Topic: ``rhasspy/handle/toggleOn``

    Payload (JSON):

    .. list-table::
      :widths: 10 10 80
      :header-rows: 1

      * - Key
        - Type
        - Description
      * - siteId
        - string
        - The id of the site where intent handling should be enabled. Defaults to ``"default"``.

    Example
    -------

    In Python:

    >>> from rhasspyhermes.handle import HandleToggleOn
    >>> on = HandleToggleOn()
    >>> on
    HandleToggleOn(site_id='default')
    >>> on.payload()
    '{"siteId": "default"}'
    >>> on.topic()
    'rhasspy/handle/toggleOn'

    Publish this message type with ``mosquitto_pub``:

    .. code-block:: shell

      mosquitto_pub -h <HOSTNAME> -t 'rhasspy/handle/toggleOn' -m '{"siteId": "default"}'

    Note
    ----

    This is a Rhasspy-only message."""

    site_id: str = "default"
    """The id of the site where intent handling should be enabled"""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"rhasspy/handle/toggleOn"``
        """
        return "rhasspy/handle/toggleOn"


@dataclass
class HandleToggleOff(Message):
    """Disable intent handling.

    The corresponding MQTT message has the following properties:

    Topic: ``rhasspy/handle/toggleOff``

    Payload (JSON):

    .. list-table::
      :widths: 10 10 80
      :header-rows: 1

      * - Key
        - Type
        - Description
      * - siteId
        - string
        - The id of the site where intent handling should be disabled. Defaults to ``"default"``.

    Example
    -------

    In Python:

    >>> from rhasspyhermes.handle import HandleToggleOff
    >>> off = HandleToggleOff()
    >>> off
    HandleToggleOff(site_id='default')
    >>> off.payload()
    '{"siteId": "default"}'
    >>> off.topic()
    'rhasspy/handle/toggleOff'

    Publish this message type with ``mosquitto_pub``:

    .. code-block:: shell

      mosquitto_pub -h <HOSTNAME> -t 'rhasspy/handle/toggleOff' -m '{"siteId": "default"}'

    Note
    ----

    This is a Rhasspy-only message."""

    site_id: str = "default"
    """The id of the site where intent handling should be disabled"""

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            ``"rhasspy/handle/toggleOff"``
        """
        return "rhasspy/handle/toggleOff"
