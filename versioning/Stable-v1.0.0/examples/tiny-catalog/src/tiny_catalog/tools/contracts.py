"""Technology-independent tool contracts consumed by use cases.

A method signature alone is not the contract: guarantees and failure semantics
are described here and in OAL-P2/adpm/tool-contracts.md. Python protocols are a choice
of this example, not a ADPM requirement.
"""
from typing import Protocol

from tiny_catalog.entities.item import Item


class ItemStore(Protocol):
    """Preserve unique codes, independent returned entities, and confirmed writes.

    Normal write returns mean that the selected mechanism acknowledged the
    commit. StoreUnavailable does NOT guarantee the absence of a write.
    """

    def insert(self, item: Item) -> Item:
        """Atomically insert or raise StoreConflict; never overwrite an existing key."""
        ...

    def get(self, code: str) -> Item | None:
        """Return an independent record, or None; StoreUnavailable is not absence."""
        ...

    def list_all(self) -> list[Item]:
        """Return independent records; no availability filtering or business ordering."""
        ...

    def replace(self, item: Item) -> Item:
        """Atomically replace an existing key or raise StoreMissing; never insert."""
        ...


class RecordCodec(Protocol):
    """Translate between entity data and the storage record representation."""

    def encode(self, item: Item) -> tuple[str, str, int]:
        """Produce a detached record representation."""
        ...

    def decode(self, record: tuple[object, ...]) -> Item:
        """Produce an independent, validated entity or raise ValueError/InvalidData."""
        ...
