"""Intent and slot classes for NLU."""
import typing
from dataclasses import dataclass

from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Intent:
    """Intent object with a name and confidence score."""

    intent_name: str
    """The name of the detected intent."""
    confidence_score: float
    """The probability of the detection, between 0 and 1 (1 being sure)."""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SlotRange:
    """The range where a slot is found in the input text."""

    start: int
    """Index of the beginning (inclusive) of the slot value in the substituted input."""
    end: int
    """Index of the end (exclusive) of the slot value in the substituted input."""

    # ------------
    # Rhasspy only
    # ------------

    raw_start: typing.Optional[int] = None
    """Index of the beginning (inclusive) of the slot value in the unsubstituted input.

    Note
    ----

    This is a Rhasspy-only attribute."""
    raw_end: typing.Optional[int] = None
    """Index of the end (exclusive) of the slot value in the unsubstituted input.

    Note
    ----

    This is a Rhasspy-only attribute."""


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Slot:
    """Named entity in an intent slot."""

    entity: str
    """The entity of the slot."""
    value: typing.Dict[str, typing.Any]
    """The resolved value of the slot. Contains at least a ``"value"`` key."""
    slot_name: str = None  # type: ignore
    """The name of the slot."""
    raw_value: str = None  # type: ignore
    """The raw value of the slot, as it was in the input."""
    confidence: float = 0.0
    """Confidence score of the slot, between 0 and 1 (1 being confident)."""
    range: typing.Optional[SlotRange] = None
    """The range where the slot is found in the input text."""

    def __post_init__(self) -> None:
        """dataclasses post-init"""
        if self.slot_name is None:
            self.slot_name = self.entity

        if self.raw_value is None:
            self.raw_value = self.value.get("value")

    @property
    def start(self) -> int:
        """Get the start index (inclusive) of the slot value."""
        if self.range:
            return self.range.start

        return 0

    @property
    def raw_start(self) -> int:
        """Get the start index (inclusive) of the raw slot value."""
        value = None
        if self.range:
            value = self.range.raw_start

        if value is None:
            return self.start

        return value

    @property
    def end(self) -> int:
        """Get the end index (exclusive) of the slot value."""
        if self.range:
            return self.range.end

        return 1

    @property
    def raw_end(self) -> int:
        """Get the end index (exclusive) of the raw slot value."""
        value = None
        if self.range:
            value = self.range.raw_end

        if value is None:
            return self.end

        return value
