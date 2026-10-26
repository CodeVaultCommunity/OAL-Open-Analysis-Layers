"""SQLite mechanism for the storage contract; no sales-stage policy."""
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
import sqlite3

from ..entities import Opportunity, InteractionNote, StageEvent
from ..errors import Conflict, Invalid, Missing, Unavailable

class SQLiteStore:
    """Persistence and atomic version checks; business transitions stay in cases."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self._connection() as db:
                db.executescript("""
                    CREATE TABLE IF NOT EXISTS opportunities (
                      id TEXT PRIMARY KEY, title TEXT NOT NULL, company TEXT NOT NULL,
                      owner TEXT NOT NULL, stage TEXT NOT NULL, version INTEGER NOT NULL,
                      created_at TEXT NOT NULL, updated_at TEXT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS notes (
                      id TEXT PRIMARY KEY, opportunity_id TEXT NOT NULL,
                      body TEXT NOT NULL, created_at TEXT NOT NULL,
                      FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
                    );
                    CREATE TABLE IF NOT EXISTS stage_events (
                      opportunity_id TEXT NOT NULL, source_stage TEXT,
                      destination_stage TEXT NOT NULL, actor TEXT NOT NULL,
                      created_at TEXT NOT NULL, resulting_version INTEGER NOT NULL,
                      FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
                    );
                """)
        except sqlite3.Error as error:
            raise Unavailable("storage unavailable") from error

    @contextmanager
    def _connection(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        try:
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def _card(row: sqlite3.Row) -> Opportunity:
        return Opportunity(**{field: row[field] for field in Opportunity.__dataclass_fields__})

    def create(self, card: Opportunity, actor: str) -> None:
        try:
            with self._connection() as db:
                db.execute("INSERT INTO opportunities VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           tuple(asdict(card).values()))
                db.execute("INSERT INTO stage_events VALUES (?, ?, ?, ?, ?, ?)",
                           (card.id, None, card.stage, actor, card.created_at, card.version))
        except sqlite3.IntegrityError as error:
            raise Conflict("identifier already exists") from error
        except sqlite3.Error as error:
            raise Unavailable("storage unavailable") from error

    def get(self, card_id: str) -> Opportunity:
        try:
            with self._connection() as db:
                row = db.execute("SELECT * FROM opportunities WHERE id = ?", (card_id,)).fetchone()
                if row is None:
                    raise Missing("opportunity not found")
                try:
                    return self._card(row)
                except (Invalid, TypeError, ValueError) as error:
                    raise Unavailable("stored data is invalid") from error
        except sqlite3.Error as error:
            raise Unavailable("storage unavailable") from error

    def mutate(self, card_id: str, expected_version: int, timestamp: str, actor: str,
               *, stage: str | None = None, note_id: str | None = None,
               note_body: str | None = None) -> Opportunity:
        try:
            with self._connection() as db:
                db.execute("BEGIN IMMEDIATE")
                row = db.execute("SELECT * FROM opportunities WHERE id = ?", (card_id,)).fetchone()
                if row is None:
                    raise Missing("opportunity not found")
                try:
                    previous = self._card(row)
                except (Invalid, TypeError, ValueError) as error:
                    raise Unavailable("stored data is invalid") from error
                if previous.version != expected_version:
                    raise Conflict("card changed; refresh the board")
                destination = stage or previous.stage
                updated = db.execute(
                    "UPDATE opportunities SET stage = ?, version = version + 1, updated_at = ? WHERE id = ? AND version = ?",
                    (destination, timestamp, card_id, expected_version),
                )
                if updated.rowcount != 1:
                    raise Conflict("card changed; refresh the board")
                if stage is not None:
                    db.execute("INSERT INTO stage_events VALUES (?, ?, ?, ?, ?, ?)",
                               (card_id, previous.stage, stage, actor, timestamp, expected_version + 1))
                if note_body is not None:
                    db.execute("INSERT INTO notes VALUES (?, ?, ?, ?)",
                               (note_id, card_id, note_body, timestamp))
                return Opportunity(card_id, previous.title, previous.company, previous.owner,
                                   destination, expected_version + 1, previous.created_at, timestamp)
        except sqlite3.IntegrityError as error:
            raise Conflict("identifier already exists") from error
        except sqlite3.Error as error:
            raise Unavailable("storage unavailable") from error

    def list_records(self) -> list[tuple[Opportunity, list[InteractionNote], list[StageEvent]]]:
        try:
            with self._connection() as db:
                records = []
                try:
                    for row in db.execute("SELECT * FROM opportunities").fetchall():
                        card = self._card(row)
                        notes = [InteractionNote(**dict(note)) for note in db.execute(
                            "SELECT id, opportunity_id, body, created_at FROM notes "
                            "WHERE opportunity_id = ? ORDER BY created_at, id", (card.id,))]
                        events = [StageEvent(**dict(event)) for event in db.execute(
                            "SELECT source_stage, destination_stage, actor, created_at, resulting_version "
                            "FROM stage_events WHERE opportunity_id = ? ORDER BY resulting_version", (card.id,))]
                        records.append((card, notes, events))
                except (Invalid, TypeError, ValueError) as error:
                    raise Unavailable("stored data is invalid") from error
                return records
        except sqlite3.Error as error:
            raise Unavailable("storage unavailable") from error
