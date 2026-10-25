"""UC-CAT-001 — Register item. One specification identity, one implementation."""
from collections.abc import Callable

from tiny_catalog.entities.item import Item
from tiny_catalog.errors import DuplicateItem, PersistenceUnavailable, StoreConflict, StoreUnavailable
from tiny_catalog.tools.contracts import ItemStore
from tiny_catalog.authorization import require_actor


class RegisterItem:
    """Register a valid item as active, rejecting an already allocated code."""

    ucs_id = "UC-CAT-001"

    def __init__(self, store: ItemStore, item_factory: Callable[[str, str, bool], Item]) -> None:
        self._store = store
        self._item_factory = item_factory

    def execute(self, code: str, name: str, *, principal: str | None = None) -> Item:
        """Validate before persistence; ask the tool to preserve atomic uniqueness."""
        require_actor(self.ucs_id, principal)
        item = self._item_factory(code, name, True)
        try:
            return self._store.insert(item)
        except StoreConflict as error:
            raise DuplicateItem("an item with this code already exists") from error
        except StoreUnavailable as error:
            raise PersistenceUnavailable("registration could not be confirmed") from error
