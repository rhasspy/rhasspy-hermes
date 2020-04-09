"""Shared intent/slot classes for NLU."""
import typing
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Intent:
    """Intent name and confidence.

    Attributes
    ----------
    intent_name: str
        The name of the detected intent

    confidence_score: float
        The probability of the detection, between 0 and 1, 1 being sure
    """

    intent_name: str
    confidence_score: float


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SlotRange:
    """Index range of a slot in text.

    Attributes
    ----------
    start: int
        Beginning of the slot value in the substituted input

    end: int
        Exclusive end of the slot value in the substituted input

    raw_start: Optional[int] = None
        Beginning of the slot value in the unsubstituted input

    raw_end: Optional[int] = None
        Exclusive end of the slot value in the unsubstituted input
    """

    start: int
    end: int

    # ------------
    # Rhasspy only
    # ------------

    raw_start: typing.Optional[int] = None
    raw_end: typing.Optional[int] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Slot:
    """Named entity in an intent slot.

    Attributes
    ----------
    entity: str
        The entity of the slot

    value: typing.Dict[str, typing.Any]
        The resolved value of the slot.
        Contains at least a "value" key.

    slot_name: str
        The name of the slot

    raw_value: str
        The raw value of the slot, as is was in the input

    confidence: float = 0.0
        Confidence of the slot, between 0 and 1, 1 being confident

    range: typing.Optional[SlotRange] = None
        The range where the slot can be found in the input
    """

    entity: str
    value: typing.Dict[str, typing.Any]
    slot_name: str = None  # type: ignore
    raw_value: str = None  # type: ignore
    confidence: float = 0.0
    range: typing.Optional[SlotRange] = None

    def __post_init__(self):
        """dataclasses post-init"""
        if self.slot_name is None:
            self.slot_name = self.entity

        if self.raw_value is None:
            self.raw_value = self.value.get("value")

    @property
    def start(self) -> int:
        """Get start index of slot value"""
        if self.range:
            return self.range.start

        return 0

    @property
    def raw_start(self) -> int:
        """Get start index of raw slot value"""
        value = None
        if self.range:
            value = self.range.raw_start

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
    def raw_end(self) -> int:
        """Get end index (exclusive) of raw slot value"""
        value = None
        if self.range:
            value = self.range.raw_end

        if value is None:
            return self.end

        return value
