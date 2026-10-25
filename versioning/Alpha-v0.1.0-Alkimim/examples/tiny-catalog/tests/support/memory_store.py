"""A controlled substitute, not a persistence implementation for production.

Its dictionary can model retained records within one test application. It does
not offer restart durability. The SQLite profile is used for restart/concurrency
evidence. Returned entities are detached to avoid hiding missing explicit writes.
"""
from collections.abc import Callable

from tiny_catalog.entities.item import Item
from tiny_catalog.errors import StoreConflict, StoreMissing


class MemoryItemStore:
    """Test-double implementation of the observable record-store operations."""

    def __init__(self, factory: Callable[[str, str, bool], Item]) -> None:
        self._factory = factory
        self._records: dict[str, tuple[str, str, bool]] = {}

    def insert(self, item: Item) -> Item:
        if item.code in self._records:
            raise StoreConflict("code already exists")
        self._records[item.code] = (item.code, item.name, item.active)
        return self._factory(*self._records[item.code])

    def get(self, code: str) -> Item | None:
        record = self._records.get(code)
        return None if record is None else self._factory(*record)

    def list_all(self) -> list[Item]:
        return [self._factory(*record) for record in self._records.values()]

    def replace(self, item: Item) -> Item:
        if item.code not in self._records:
            raise StoreMissing("code does not exist")
        self._records[item.code] = (item.code, item.name, item.active)
        return self._factory(*self._records[item.code])
