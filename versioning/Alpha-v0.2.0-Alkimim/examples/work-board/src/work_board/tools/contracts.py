"""Capabilities injected into the use cases.

Contract for every implementation:

- `create` persists a new item and raises `Conflict` for a duplicated identifier.
- `get` returns the stored item or raises `Missing` when it is absent.
- `assign` and `transition` perform an atomic compare-and-set: the change is
  written only when the stored version equals `version`, and the stored version
  then increases by one. A version mismatch raises `Conflict` and an absent item
  raises `Missing`; neither case changes the stored item.
- `add_comment` raises `Missing` for an absent item and `Conflict` for a
  duplicated comment identifier, without persisting a partial row.
- Every operation may raise `Unavailable`. Its `write_outcome` is
  `not_applied` only for a known pre-write failure or confirmed rollback before
  commit. It is `unknown` when commit or rollback cannot be confirmed. The
  caller must inspect state before retrying an unknown write outcome.
- The positive expected-version input has no storage-specific upper bound.
  A value that cannot match any stored version still yields Conflict or Missing.
  Exhaustion of the concrete store's counter capacity is Unavailable before
  mutation, not a new business validation rule.
- Returned items and comments reflect the operation's committed state.
  `comments` returns comments in chronological order (`created_at`, then `id`),
  and `list_items` applies its filters and returns items ordered by project,
  title, and id.
"""
from typing import Protocol

from ..entities import Comment, WorkItem


class WorkStore(Protocol):
    def create(self, item: WorkItem) -> WorkItem:
        """Persist a new item and return it; a duplicate ID raises Conflict."""

    def get(self, item_id: str) -> WorkItem:
        """Return the stored item; an absent item raises Missing."""

    def assign(self, item_id: str, assignee: str, version: int) -> WorkItem:
        """Atomically set the assignee when the stored version equals `version`."""

    def transition(self, item_id: str, status: str, version: int) -> WorkItem:
        """Atomically set the status when the stored version equals `version`."""

    def add_comment(self, comment: Comment) -> Comment:
        """Persist a comment; a missing item or duplicate comment ID is rejected."""

    def list_items(self, project: str | None, status: str | None) -> list[WorkItem]:
        """Return filtered items ordered by project, title, and id."""

    def comments(self, item_id: str) -> list[Comment]:
        """Return the item's comments in chronological order; Missing if absent."""
