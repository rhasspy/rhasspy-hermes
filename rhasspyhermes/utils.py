"""Utility methods."""
import typing

import attr


def only_fields(
    cls, message_dict: typing.Dict[str, typing.Any]
) -> typing.Dict[str, typing.Any]:
    """Return dict with only valid fields."""
    try:
        field_names = set(attr.fields_dict(cls).keys())
        valid_fields = set(message_dict.keys()).intersection(field_names)
        return {key: message_dict[key] for key in valid_fields}
    except attr.exceptions.NotAnAttrsClassError:
        return message_dict
