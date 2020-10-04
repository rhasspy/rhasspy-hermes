"""Support for the Rhasspy Hermes protocol.

The Rhasspy Hermes protocol is an extension of the Snips Hermes protocol.
"""
import typing
from abc import ABCMeta

from dataclasses_json import DataClassJsonMixin, LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
class Message(DataClassJsonMixin, metaclass=ABCMeta):
    """Base class for Hermes messages.

    All classes implementing Hermes messages are subclasses of this class."""

    def __init__(self, **kwargs):
        DataClassJsonMixin.__init__(self, letter_case=LetterCase.CAMEL)

    def payload(self) -> typing.Union[str, bytes]:
        """Get the payload for this message.

        Returns
        -------

        Union[str, bytes]
            The payload as a JSON string or bytes

        Example
        -------

        >>> from rhasspyhermes.handle import HandleToggleOn
        >>> on = HandleToggleOn(site_id='satellite')
        >>> on.payload()
        '{"siteId": "satellite"}'
        """
        return self.to_json(ensure_ascii=False)

    @classmethod
    def get_site_id(cls, topic: str) -> typing.Optional[str]:
        """Extract site id from message topic.

        Arguments
        ---------
        topic
            message topic

        Returns
        -------
        Optional[str]
            The optional site id for this message topic

        Example
        -------

        >>> from rhasspyhermes.audioserver import AudioSessionFrame
        >>> topic = "hermes/audioServer/satellite/abcd/audioSessionFrame"
        >>> AudioSessionFrame.get_site_id(topic)
        'satellite'
        """
        return None

    @classmethod
    def get_session_id(cls, topic: str) -> typing.Optional[str]:
        """Extract session id from message topic.

        Arguments
        ---------
        topic
            message topic

        Returns
        -------
        Optional[str]
            The optional session id for this message topic

        Example
        -------

        >>> from rhasspyhermes.audioserver import AudioSessionFrame
        >>> topic = "hermes/audioServer/satellite/abcd/audioSessionFrame"
        >>> AudioSessionFrame.get_session_id(topic)
        'abcd'
        """
        return None

    @classmethod
    def is_binary_payload(cls) -> bool:
        """Check for binary payload of message.

        Returns
        -------
        bool
            ``True`` if message payload is not JSON

        Example
        -------

        >>> from rhasspyhermes.audioserver import AudioFrame
        >>> AudioFrame.is_binary_payload()
        True
        """
        return False

    @classmethod
    def is_site_in_topic(cls) -> bool:
        """Check for site id in topic.

        Returns
        -------
        bool
            ``True`` if site id is part of topic

        Example
        -------

        >>> from rhasspyhermes.asr import AsrTrain
        >>> AsrTrain.is_site_in_topic()
        True
        """
        return False

    @classmethod
    def is_session_in_topic(cls) -> bool:
        """Check for session id in topic.

        Returns
        -------
        bool
            ``True`` if session id is part of topic

        Example
        -------

        >>> from rhasspyhermes.asr import AsrAudioCaptured
        >>> AsrAudioCaptured.is_session_in_topic()
        True
        """
        return False

    @classmethod
    def topic(cls, **kwargs) -> str:
        """Get MQTT topic for this message type.

        Returns
        -------
        str
            The MQTT topic for this message type

        Example
        -------

        >>> from rhasspyhermes.nlu import NluIntent
        >>> NluIntent.topic()
        'hermes/intent/#'
        """

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
        --------

        >>> from rhasspyhermes.wake import HotwordDetected
        >>> HotwordDetected.is_topic("hermes/hotword/precise/detected")
        True
        """
        return topic == cls.topic()
