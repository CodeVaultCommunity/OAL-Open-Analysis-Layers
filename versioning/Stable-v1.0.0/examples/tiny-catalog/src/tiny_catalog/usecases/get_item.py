"""UC-CAT-002 — Get item, including an inactive retained record."""
from collections.abc import Callable

from tiny_catalog.entities.item import Item, ItemKey
from tiny_catalog.errors import ItemNotFound, PersistenceUnavailable, StoreUnavailable
from tiny_catalog.tools.contracts import ItemStore
from tiny_catalog.authorization import require_actor


class GetItem:
    """Read an item by code without filtering its state."""

    ucs_id = "UC-CAT-002"

    def __init__(self, store: ItemStore, key_factory: Callable[[str], ItemKey]) -> None:
        self._store = store
        self._key_factory = key_factory

    def execute(self, code: str, *, principal: str | None = None) -> Item:
        """Distinguish invalid code, missing record, and unavailable persistence."""
        require_actor(self.ucs_id, principal)
        key = self._key_factory(code)
        try:
            item = self._store.get(key.code)
        except StoreUnavailable as error:
            raise PersistenceUnavailable("lookup could not be confirmed") from error
        if item is None:
            raise ItemNotFound("no item exists under this code")
        return item
