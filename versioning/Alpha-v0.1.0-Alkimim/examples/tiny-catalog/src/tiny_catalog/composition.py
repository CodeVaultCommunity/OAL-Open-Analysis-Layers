"""The sole production selection/wiring boundary for this example.

A CatalogApplication owns one instance of each use case. Every request reuses
those objects: application-scoped singleton lifetime without global mutable
registries or request data retained on a use case. Multiple test applications
remain independent. Singletons are still injected here; the exception is unused.
"""
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Mapping
from types import SimpleNamespace
import sqlite3

from tiny_catalog.entities.item import Item, ItemKey
from tiny_catalog.tools.contracts import ItemStore
from tiny_catalog.tools.record_codec import ItemRecordCodec
from tiny_catalog.tools.sqlite_connections import SQLiteConnections
from tiny_catalog.tools.sqlite_store import SQLiteItemStore
from tiny_catalog.usecases.deactivate_item import DeactivateItem
from tiny_catalog.usecases.get_item import GetItem
from tiny_catalog.usecases.list_available_items import ListAvailableItems
from tiny_catalog.usecases.register_item import RegisterItem


@dataclass(frozen=True)
class CatalogApplication:
    """Composition record, not an additional domain entity or use case."""

    register: RegisterItem
    get: GetItem
    list_available: ListAvailableItems
    deactivate: DeactivateItem
    use_cases: Mapping[str, object]

    def for_actor(self, actor: str):
        """Bind an authenticated actor to case calls without changing case identity."""
        class BoundCase:
            def __init__(self, case):
                self.case = case

            def execute(self, *args):
                return self.case.execute(*args, principal=actor)

        return SimpleNamespace(
            register=BoundCase(self.register),
            get=BoundCase(self.get),
            list_available=BoundCase(self.list_available),
            deactivate=BoundCase(self.deactivate),
        )


def compose(store: ItemStore) -> CatalogApplication:
    """Inject a store and all factories/collaborators; build exactly four use cases."""
    register = RegisterItem(store, Item)
    get = GetItem(store, ItemKey)
    list_available = ListAvailableItems(store)
    deactivate = DeactivateItem(get, store)
    registry = MappingProxyType({
        register.ucs_id: register,
        get.ucs_id: get,
        list_available.ucs_id: list_available,
        deactivate.ucs_id: deactivate,
    })
    return CatalogApplication(register, get, list_available, deactivate, registry)


def build_application(database: Path) -> CatalogApplication:
    """Choose the example's technical implementations; never called by a use case."""
    database = database.expanduser().resolve()
    database.parent.mkdir(parents=True, exist_ok=True)
    connections = SQLiteConnections(database, sqlite3.connect, timeout=2.0)
    codec = ItemRecordCodec(Item)
    store = SQLiteItemStore(connections, codec)
    store.initialize()
    return compose(store)
