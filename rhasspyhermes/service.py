"""Messages shared across services."""
import typing
from dataclasses import dataclass, field

from .base import Message


@dataclass
class ServiceGetStatus(Message):
    """Get status of a service."""

    categories: typing.List[str] = field(default_factory=list)
    id: str = ""
    siteId: str = "default"


@dataclass
class ServiceProblem:
    """Description of a problem a service has."""

    problemId: str = ""
    description: str = ""


@dataclass
class ServiceStatus(Message):
    """Status of service."""

    category: str = ""
    status: str = ""
    problems: typing.List[ServiceProblem] = field(default_factory=list)
    id: str = ""
    siteId: str = "default"
