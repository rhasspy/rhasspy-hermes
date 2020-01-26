"""Shared intent/slot classes"""
import typing

import attr


@attr.s(auto_attribs=True)
class Intent:
    """Intent name and confidence."""

    intentName: str
    confidenceScore: float


@attr.s(auto_attribs=True)
class SlotRange:
    """Index range of a slot in text."""

    start: int
    end: int


@attr.s(auto_attribs=True)
class Slot:
    """Named entity in an intent."""

    entity: str
    slotName: str
    confidence: float
    raw_value: str
    value: str
    range: typing.Optional[SlotRange] = None
