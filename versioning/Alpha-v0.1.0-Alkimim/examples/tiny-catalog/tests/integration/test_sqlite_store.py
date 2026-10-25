"""Tools only. SQLiteStore consumes real connection and codec tools.

SQLite is embedded, not an external service. Composition with these other tools
is what makes these integration tests under this repository's convention.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier
import sqlite3
import pytest

from tiny_catalog.entities.item import Item
from tiny_catalog.errors import StoreConflict, StoreMissing, StoreUnavailable
from tiny_catalog.tools.record_codec import ItemRecordCodec
from tiny_catalog.tools.sqlite_connections import SQLiteConnections
from tiny_catalog.tools.sqlite_store import SQLiteItemStore


def make_store(path: Path) -> SQLiteItemStore:
    store = SQLiteItemStore(SQLiteConnections(path, sqlite3.connect, 2.0), ItemRecordCodec(Item))
    store.initialize()
    return store


def test_insert_get_replace_list_and_detached_records(tmp_path):
    store = make_store(tmp_path / "data.sqlite3")
    inserted = store.insert(Item("A", "Pencil", True))
    inserted.name = "Not persisted"
    loaded = store.get("A")
    assert loaded is not None and loaded.name == "Pencil"
    loaded.active = False
    assert store.get("A").active is True
    store.replace(loaded)
    assert store.get("A").active is False
    assert [(x.code, x.active) for x in store.list_all()] == [("A", False)]
    assert store.get("MISSING") is None


def test_reopening_preserves_confirmed_record(tmp_path):
    path = tmp_path / "data.sqlite3"
    make_store(path).insert(Item("A", "Pencil", True))
    assert make_store(path).get("A").name == "Pencil"


def test_replace_does_not_silently_insert_missing_record(tmp_path):
    store = make_store(tmp_path / "data.sqlite3")
    with pytest.raises(StoreMissing):
        store.replace(Item("MISSING", "Absent", False))
    assert store.list_all() == []


def test_duplicate_insert_preserves_original(tmp_path):
    store = make_store(tmp_path / "data.sqlite3")
    store.insert(Item("A", "Original", True))
    with pytest.raises(StoreConflict):
        store.insert(Item("A", "Replacement", False))
    assert store.get("A").name == "Original"


def test_atomic_unique_key_with_independent_connections(tmp_path):
    path = tmp_path / "data.sqlite3"
    stores = [make_store(path), make_store(path)]
    barrier = Barrier(2)

    def insert(index):
        barrier.wait(timeout=5)
        try:
            stores[index].insert(Item("A", f"Writer {index}", True))
            return "inserted"
        except StoreConflict:
            return "conflict"

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(insert, (0, 1))) == ["conflict", "inserted"]
    assert len(stores[0].list_all()) == 1


def test_sql_characters_in_name_are_data_not_a_statement(tmp_path):
    store = make_store(tmp_path / "data.sqlite3")
    name = "Robert'); DROP TABLE items;--"
    store.insert(Item("A", name, True))
    assert store.get("A").name == name
    assert len(store.list_all()) == 1


def test_connection_failure_is_not_reported_as_missing(tmp_path):
    # An existing directory cannot be opened as an SQLite database file.
    store = SQLiteItemStore(SQLiteConnections(tmp_path, sqlite3.connect, 0.1), ItemRecordCodec(Item))
    with pytest.raises(StoreUnavailable):
        store.get("A")


def test_invalid_stored_data_is_reported_as_unavailable(tmp_path):
    path = tmp_path / "data.sqlite3"
    store = make_store(path)
    store.insert(Item("A", "Valid", True))
    with sqlite3.connect(path) as connection:
        connection.execute("UPDATE items SET name = '' WHERE code = 'A'")
    connection.close()
    with pytest.raises(StoreUnavailable):
        store.get("A")
