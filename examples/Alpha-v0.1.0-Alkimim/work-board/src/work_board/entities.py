"""Work-item data and field validity; workflow decisions belong to cases."""
from dataclasses import dataclass

from .errors import Invalid


STATUSES = ("backlog", "in_progress", "done")
PRIORITIES = ("low", "normal", "high")


def required_text(value: str, field: str, limit: int) -> str:
    if not isinstance(value, str):
        raise Invalid(f"{field} must be text")
    value = value.strip()
    if not value or len(value) > limit:
        raise Invalid(f"{field} must have 1–{limit} characters")
    return value


@dataclass(frozen=True)
class WorkItem:
    id: str
    project: str
    title: str
    description: str
    priority: str
    status: str
    assignee: str | None
    version: int


@dataclass(frozen=True)
class Comment:
    id: str
    item_id: str
    author: str
    body: str
    created_at: str

