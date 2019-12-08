import typing

import attr


@attr.s
class Intent:
    intentName: str = attr.ib()
    confidenceScore: float = attr.ib()


@attr.s
class SlotRange:
    start: int = attr.ib()
    end: int = attr.ib()


@attr.s
class Slot:
    entity: str = attr.ib()
    slotName: str = attr.ib()
    confidence: float = attr.ib()
    raw_value: str = attr.ib()
    value: str = attr.ib()
    range: typing.Optional[SlotRange] = attr.ib(default=None)
