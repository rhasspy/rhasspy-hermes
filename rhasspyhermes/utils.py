"""Utility methods for Rhasspy Hermes messages."""
import dataclasses
import typing


def only_fields(
    cls, message_dict: typing.Dict[str, typing.Any]
) -> typing.Dict[str, typing.Any]:
    """Return a dict with only valid fields."""
    if dataclasses.is_dataclass(cls):
        field_names = set(f.name for f in dataclasses.fields(cls))
        valid_fields = set(message_dict.keys()).intersection(field_names)
        return {key: message_dict[key] for key in valid_fields}

    return message_dict
