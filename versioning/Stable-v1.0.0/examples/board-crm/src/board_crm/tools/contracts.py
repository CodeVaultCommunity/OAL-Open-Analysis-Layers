"""Storage contract consumed by use cases; independent of SQLite.

create and mutate commit their opportunity, note, and event changes together.
Unknown IDs raise Missing, stale versions raise Conflict, storage failures raise
Unavailable. Reads return independent entities and never impose board policy.
"""
from typing import Protocol
from ..entities import Opportunity, InteractionNote, StageEvent

class IdentifierProvider(Protocol):
    """Return a new opaque nonempty ID; callers handle storage collisions."""

    def __call__(self) -> str: ...


class Clock(Protocol):
    """Return a timezone-aware, lexically sortable timestamp."""

    def __call__(self) -> str: ...


class Store(Protocol):
    def create(self, card: Opportunity, actor: str) -> None: ...
    def get(self, card_id: str) -> Opportunity: ...
    def mutate(self, card_id: str, expected_version: int, timestamp: str, actor: str,
               *, stage: str | None = None, note_id: str | None = None,
               note_body: str | None = None) -> Opportunity: ...
    def list_records(self) -> list[tuple[Opportunity, list[InteractionNote], list[StageEvent]]]: ...
