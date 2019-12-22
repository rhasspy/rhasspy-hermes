"""Messages for hermes/audioServer"""
import re
from uuid import uuid4

import attr

from .base import Message


@attr.s
class AudioFrame(Message):
    """Captured sound frame."""

    TOPIC_PATTERN = re.compile(r"^hermes/audioServer/([^/]+)/audioFrame$")

    wav_data: bytes = attr.ib()

    @classmethod
    def topic(cls, **kwargs) -> str:
        siteId = kwargs.get("siteId", "default")
        return f"hermes/audioServer/{siteId}/audioFrame"

    @classmethod
    def get_siteId(cls, topic: str):
        """Get siteId from a topic"""
        match = re.match(AudioFrame.TOPIC_PATTERN, topic)
        assert match, "Not an audioFrame topic"
        return match.group(1)


@attr.s
class AudioPlayBytes(Message):
    """Play WAV sound on specific site."""

    TOPIC_PATTERN = re.compile(r"^hermes/audioServer/([^/]+)/playBytes/([^/]+)$")

    wav_data: bytes = attr.ib()

    @classmethod
    def topic(cls, **kwargs) -> str:
        siteId = kwargs.get("siteId", "default")
        requestId = kwargs.get("requestId") or str(uuid4())
        return f"hermes/audioServer/{siteId}/playBytes/{requestId}"

    @classmethod
    def get_siteId(cls, topic: str):
        """Get siteId from a topic"""
        match = re.match(AudioPlayBytes.TOPIC_PATTERN, topic)
        assert match, "Not a playBytes topic"
        return match.group(1)

    @classmethod
    def get_requestId(cls, topic: str):
        """Get requestId from a topic"""
        match = re.match(AudioPlayBytes.TOPIC_PATTERN, topic)
        assert match, "Not a playBytes topic"
        return match.group(2)


@attr.s
class AudioPlayFinished(Message):
    """Sent when audio service has finished playing a sound."""

    TOPIC_PATTERN = re.compile(r"^hermes/audioServer/([^/]+)/playFinished$")

    id: str = attr.ib(default="")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        siteId = kwargs.get("siteId", "default")
        return f"hermes/audioServer/{siteId}/playFinished"

    @classmethod
    def get_siteId(cls, topic: str):
        """Get siteId from a topic"""
        match = re.match(AudioPlayFinished.TOPIC_PATTERN, topic)
        assert match, "Not a playFinished topic"
        return match.group(1)
