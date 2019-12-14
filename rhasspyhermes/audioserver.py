"""Messages for hermes/audioServer"""
from uuid import uuid4

import attr

from .base import Message


@attr.s
class AudioFrame(Message):
    """Captured sound frame."""

    wav_data: bytes = attr.ib()

    @classmethod
    def topic(cls, **kwargs) -> str:
        siteId = kwargs.get("siteId", "default")
        return f"hermes/audioServer/{siteId}/audioFrame"


@attr.s
class AudioPlayBytes(Message):
    """Play WAV sound on specific site."""

    wav_data: bytes = attr.ib()

    @classmethod
    def topic(cls, **kwargs) -> str:
        siteId = kwargs.get("siteId", "default")
        request_id = kwargs.get("request_id") or str(uuid4())
        return f"hermes/audioServer/{siteId}/playBytes/{request_id}"


@attr.s
class AudioPlayFinished(Message):
    """Sent when audio service has finished playing a sound."""

    id: str = attr.ib(default="")
    sessionId: str = attr.ib(default="")

    @classmethod
    def topic(cls, **kwargs) -> str:
        siteId = kwargs.get("siteId", "default")
        return f"hermes/audioServer/{siteId}/playFinished"
