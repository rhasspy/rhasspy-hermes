"""Messages for hermes/audioServer"""
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
