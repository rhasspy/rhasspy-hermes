"""Messages shared across services."""
import typing

import attr

from .base import Message


@attr.s(auto_attribs=True, slots=True)
class ServiceGetStatus(Message):
    """Get status of a service."""

    categories: typing.List[str] = []
    id: str = ""
    siteId: str = "default"


@attr.s(auto_attribs=True, slots=True)
class ServiceProblem:
    """Description of a problem a service has."""

    problemId: str = ""
    description: str = ""


@attr.s(auto_attribs=True, slots=True)
class ServiceStatus(Message):
    """Status of service."""

    category: str = ""
    status: str = ""
    problems: typing.List[ServiceProblem] = []
    id: str = ""
    siteId: str = "default"
