"""Shared intent/slot classes"""
import typing

import attr


@attr.s
class Intent:
    """Intent name and confidence."""

    intentName: str = attr.ib()
    confidenceScore: float = attr.ib()


@attr.s
class SlotRange:
    """Index range of a slot in text."""

    start: int = attr.ib()
    end: int = attr.ib()


@attr.s
class Slot:
    """Named entity in an intent."""

    entity: str = attr.ib()
    slotName: str = attr.ib()
    confidence: float = attr.ib()
    raw_value: str = attr.ib()
    value: str = attr.ib()
    range: typing.Optional[SlotRange] = attr.ib(default=None)
