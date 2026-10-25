"""Connection provisioning is a concrete technical tool, never a use-case duty."""
from collections.abc import Callable
from pathlib import Path
from typing import Protocol
import sqlite3


class ConnectionProvider(Protocol):
    """Supply a fresh SQLite connection; its caller owns closing it."""

    def open(self) -> sqlite3.Connection:
        """Return a connection configured for explicit context-managed transactions."""
        ...


class SQLiteConnections:
    """Each operation gets its own connection; no shared mutable connection state."""

    def __init__(
        self,
        database: Path,
        connect: Callable[..., sqlite3.Connection],
        timeout: float,
    ) -> None:
        self._database = database
        self._connect = connect
        self._timeout = timeout

    def open(self) -> sqlite3.Connection:
        """Use the injected driver factory, with transaction behavior explicit."""
        return self._connect(
            str(self._database),
            timeout=self._timeout,
            isolation_level="DEFERRED",
            autocommit=sqlite3.LEGACY_TRANSACTION_CONTROL,
        )
