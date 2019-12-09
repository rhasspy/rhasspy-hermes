import typing

import attr

from .base import Message


@attr.s
class AudioFrame(Message):
    """Captured sound frame."""

    wav_data: bytes = attr.ib()

    @classmethod
    def topic(cls, siteId: str, *args, **kwargs) -> str:
        return f"hermes/audioServer/{siteId}/audioFrame"
