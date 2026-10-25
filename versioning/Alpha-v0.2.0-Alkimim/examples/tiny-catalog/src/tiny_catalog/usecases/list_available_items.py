"""UC-CAT-003 — List available items, ordered by code."""
from tiny_catalog.entities.item import Item
from tiny_catalog.errors import PersistenceUnavailable, StoreUnavailable
from tiny_catalog.tools.contracts import ItemStore
from tiny_catalog.authorization import require_actor


class ListAvailableItems:
    """The active-only rule belongs here, not in an entity or SQL adapter."""

    ucs_id = "UC-CAT-003"

    def __init__(self, store: ItemStore) -> None:
        self._store = store

    def execute(self, *, principal: str | None = None) -> list[Item]:
        """Return only active records in ascending ASCII code order."""
        require_actor(self.ucs_id, principal)
        try:
            items = self._store.list_all()
        except StoreUnavailable as error:
            raise PersistenceUnavailable("listing could not be confirmed") from error
        return sorted((item for item in items if item.active), key=lambda item: item.code)
