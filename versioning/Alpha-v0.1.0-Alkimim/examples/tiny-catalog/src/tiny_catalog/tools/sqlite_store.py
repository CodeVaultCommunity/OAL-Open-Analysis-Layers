"""Concrete persistence: composes connection and record-codec tools.

SQL, transaction handling, and driver errors stay here. This implementation
fulfils the unique-key contract mechanically; the use case chooses the meaning
of that conflict for registration.
"""
from contextlib import closing
import sqlite3

from tiny_catalog.entities.item import Item
from tiny_catalog.errors import InvalidData, StoreConflict, StoreMissing, StoreUnavailable
from tiny_catalog.tools.contracts import RecordCodec
from tiny_catalog.tools.sqlite_connections import ConnectionProvider


class SQLiteItemStore:
    """File-backed storage for a single local catalog."""

    def __init__(self, connections: ConnectionProvider, codec: RecordCodec) -> None:
        self._connections = connections
        self._codec = codec

    def initialize(self) -> None:
        """Create the example schema at the composition boundary, not in a use case."""
        try:
            with closing(self._connections.open()) as connection, connection:
                connection.execute(
                    "CREATE TABLE IF NOT EXISTS items ("
                    "code TEXT PRIMARY KEY NOT NULL, "
                    "name TEXT NOT NULL, "
                    "active INTEGER NOT NULL CHECK(active IN (0, 1)))"
                )
        except sqlite3.Error as error:
            raise StoreUnavailable("storage initialization failed") from error

    def insert(self, item: Item) -> Item:
        """Atomic unique-key insert; a normal return follows commit acknowledgement."""
        record = self._codec.encode(item)
        try:
            with closing(self._connections.open()) as connection, connection:
                connection.execute("INSERT INTO items(code, name, active) VALUES (?, ?, ?)", record)
        except sqlite3.IntegrityError as error:
            if getattr(error, "sqlite_errorcode", None) in (
                sqlite3.SQLITE_CONSTRAINT_PRIMARYKEY,
                sqlite3.SQLITE_CONSTRAINT_UNIQUE,
            ):
                raise StoreConflict("code already exists") from error
            raise StoreUnavailable("storage rejected the record") from error
        except sqlite3.Error as error:
            raise StoreUnavailable("storage cannot confirm insertion") from error
        return self._decode(record)

    def get(self, code: str) -> Item | None:
        """Query by parameter binding; absence and unavailable storage are distinct."""
        try:
            with closing(self._connections.open()) as connection:
                record = connection.execute(
                    "SELECT code, name, active FROM items WHERE code = ?", (code,)
                ).fetchone()
        except sqlite3.Error as error:
            raise StoreUnavailable("storage cannot confirm lookup") from error
        return None if record is None else self._decode(record)

    def list_all(self) -> list[Item]:
        """Read records only; availability policy and ordering are use-case decisions."""
        try:
            with closing(self._connections.open()) as connection:
                records = connection.execute("SELECT code, name, active FROM items").fetchall()
        except sqlite3.Error as error:
            raise StoreUnavailable("storage cannot confirm listing") from error
        return [self._decode(record) for record in records]

    def replace(self, item: Item) -> Item:
        """Update one existing key without an upsert or a create-on-missing policy."""
        code, name, active = self._codec.encode(item)
        try:
            with closing(self._connections.open()) as connection, connection:
                cursor = connection.execute(
                    "UPDATE items SET name = ?, active = ? WHERE code = ?",
                    (name, active, code),
                )
                if cursor.rowcount != 1:
                    raise StoreMissing("code does not exist")
        except sqlite3.Error as error:
            raise StoreUnavailable("storage cannot confirm replacement") from error
        return self._decode((code, name, active))

    def _decode(self, record: tuple[object, ...]) -> Item:
        """Treat invalid stored data as storage failure, not as valid business input."""
        try:
            return self._codec.decode(record)
        except (ValueError, InvalidData) as error:
            raise StoreUnavailable("stored data is invalid") from error
