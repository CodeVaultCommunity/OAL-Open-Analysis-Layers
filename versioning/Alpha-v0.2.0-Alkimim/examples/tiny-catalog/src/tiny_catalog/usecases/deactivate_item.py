"""UC-CAT-004 — Deactivate item without deleting the retained record."""
from typing import Protocol

from tiny_catalog.entities.item import Item
from tiny_catalog.errors import ItemNotFound, PersistenceUnavailable, StoreMissing, StoreUnavailable
from tiny_catalog.tools.contracts import ItemStore
from tiny_catalog.authorization import require_actor


class ItemLookup(Protocol):
    """Contract of the already specified UC-CAT-002, not an additional use case."""

    def execute(self, code: str, *, principal: str | None = None) -> Item:
        """Return a validated item, or its specified rejection/failure."""
        ...


class DeactivateItem:
    """Compose lookup and persistence, making the transition decision here."""

    ucs_id = "UC-CAT-004"

    def __init__(self, lookup: ItemLookup, store: ItemStore) -> None:
        self._lookup = lookup
        self._store = store

    def execute(self, code: str, *, principal: str | None = None) -> Item:
        """Repeated deactivation is successful and leaves the record unchanged."""
        require_actor(self.ucs_id, principal)
        item = self._lookup.execute(code, principal=principal)
        if not item.active:
            return item
        item.active = False
        try:
            return self._store.replace(item)
        except StoreMissing as error:
            raise ItemNotFound("no item exists under this code") from error
        except StoreUnavailable as error:
            raise PersistenceUnavailable("deactivation could not be confirmed") from error
