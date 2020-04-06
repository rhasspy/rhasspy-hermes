"""Shared intent/slot classes"""
import typing
from dataclasses import dataclass

from . import utils


@dataclass
class Intent:
    """Intent name and confidence."""

    intentName: str
    confidenceScore: float


@dataclass
class SlotRange:
    """Index range of a slot in text."""

    start: int
    end: int
    rawStart: typing.Optional[int] = None
    rawEnd: typing.Optional[int] = None


@dataclass
class Slot:
    """Named entity in an intent."""

    entity: str
    value: typing.Dict[str, typing.Any]
    slotName: str = None  # type: ignore
    rawValue: str = None  # type: ignore
    confidence: float = 0.0
    range: typing.Optional[SlotRange] = None

    def __post_init__(self):
        """dataclasses post-init"""
        if self.slotName is None:
            self.slotName = self.entity

        if self.rawValue is None:
            self.rawValue = self.value.get("value")

    @property
    def start(self) -> int:
        """Get start index of slot value"""
        if self.range:
            return self.range.start

        return 0

    @property
    def rawStart(self) -> int:
        """Get start index of raw slot value"""
        value = None
        if self.range:
            value = self.range.rawStart

        if value is None:
            return self.start

        return value

    @property
    def end(self) -> int:
        """Get end index (exclusive) of slot value"""
        if self.range:
            return self.range.end

        return 1

    @property
    def rawEnd(self) -> int:
        """Get end index (exclusive) of raw slot value"""
        value = None
        if self.range:
            value = self.range.rawEnd

        if value is None:
            return self.end

        return value

    @classmethod
    def from_dict(cls, object_dict: typing.Dict[str, typing.Any]):
        """Parse into Slot object from dictionary."""
        object_dict = utils.only_fields(cls, object_dict)
        value = object_dict.pop("value", None)

        if not value:
            value = {"value": ""}

        if "slotName" not in object_dict:
            object_dict["slotName"] = object_dict.get("entity")

        if "rawValue" not in object_dict:
            object_dict["rawValue"] = value

        slot_range = object_dict.pop("range", None)
        slot = Slot(value=value, **object_dict)
        if slot_range:
            slot.range = SlotRange(**slot_range)

        return slot
