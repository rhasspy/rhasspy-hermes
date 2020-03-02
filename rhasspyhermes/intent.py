"""Shared intent/slot classes"""
import typing

import attr


@attr.s(auto_attribs=True, slots=True)
class Intent:
    """Intent name and confidence."""

    intentName: str
    confidenceScore: float


@attr.s(auto_attribs=True, slots=True)
class SlotRange:
    """Index range of a slot in text."""

    start: int
    end: int
    raw_start: typing.Optional[int] = None
    raw_end: typing.Optional[int] = None


@attr.s(auto_attribs=True, slots=True)
class Slot:
    """Named entity in an intent."""

    entity: str
    slotName: str
    confidence: float
    raw_value: str
    value: str
    range: typing.Optional[SlotRange] = None

    @property
    def start(self) -> int:
        if self.range:
            return self.range.start

        return -1

    @property
    def raw_start(self) -> int:
        if self.range:
            value = self.range.raw_start

        if value is None:
            return self.start

        return value

    @property
    def end(self) -> int:
        if self.range:
            return self.range.end

        return -1

    @property
    def raw_end(self) -> int:
        if self.range:
            value = self.range.raw_end

        if value is None:
            return self.end

        return value

    @classmethod
    def from_dict(cls, object_dict: typing.Dict[str, typing.Any]):
        """Parse into Slot object from dictionary."""
        slot_range = object_dict.pop("range")
        slot = Slot(**object_dict)
        if slot_range:
            slot.range = SlotRange(**slot_range)

        return slot
