"""SQLite implementation of the work-store contract."""
from contextlib import contextmanager
import sqlite3
from pathlib import Path

from ..entities import Comment, WorkItem
from ..errors import Conflict, Missing


class SQLiteStore:
    def __init__(self, path: Path):
        self.path = path.expanduser().resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY, project TEXT NOT NULL, title TEXT NOT NULL,
                description TEXT NOT NULL, priority TEXT NOT NULL, status TEXT NOT NULL,
                assignee TEXT, version INTEGER NOT NULL)""")
            db.execute("""CREATE TABLE IF NOT EXISTS comments (
                id TEXT PRIMARY KEY, item_id TEXT NOT NULL REFERENCES items(id),
                author TEXT NOT NULL, body TEXT NOT NULL, created_at TEXT NOT NULL)""")

    @contextmanager
    def _connect(self):
        db = sqlite3.connect(self.path, timeout=3)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def _item(row) -> WorkItem:
        return WorkItem(**dict(row))

    def create(self, item: WorkItem) -> WorkItem:
        with self._connect() as db:
            try:
                db.execute("INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           tuple(vars(item).values()))
            except sqlite3.IntegrityError as error:
                raise Conflict("work-item identifier already exists") from error
        return item

    def get(self, item_id: str) -> WorkItem:
        with self._connect() as db:
            row = db.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
        if row is None:
            raise Missing("work item not found")
        return self._item(row)

    def _update(self, item_id: str, field: str, value: str, version: int) -> WorkItem:
        if field not in {"assignee", "status"}:
            raise ValueError("unsupported update field")
        with self._connect() as db:
            cursor = db.execute(
                f"UPDATE items SET {field}=?, version=version+1 WHERE id=? AND version=?",
                (value, item_id, version),
            )
            if cursor.rowcount == 0:
                exists = db.execute("SELECT 1 FROM items WHERE id=?", (item_id,)).fetchone()
                if exists is None:
                    raise Missing("work item not found")
                raise Conflict("work item changed; reload before retrying")
        return self.get(item_id)

    def assign(self, item_id: str, assignee: str, version: int) -> WorkItem:
        return self._update(item_id, "assignee", assignee, version)

    def transition(self, item_id: str, status: str, version: int) -> WorkItem:
        return self._update(item_id, "status", status, version)

    def add_comment(self, comment: Comment) -> Comment:
        with self._connect() as db:
            try:
                db.execute("INSERT INTO comments VALUES (?, ?, ?, ?, ?)",
                           tuple(vars(comment).values()))
            except sqlite3.IntegrityError as error:
                raise Missing("work item not found") from error
        return comment

    def list_items(self, project: str | None, status: str | None) -> list[WorkItem]:
        clauses, parameters = [], []
        if project:
            clauses.append("project=?")
            parameters.append(project)
        if status:
            clauses.append("status=?")
            parameters.append(status)
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        with self._connect() as db:
            rows = db.execute("SELECT * FROM items" + where + " ORDER BY project, title, id",
                              parameters).fetchall()
        return [self._item(row) for row in rows]

    def comments(self, item_id: str) -> list[Comment]:
        self.get(item_id)
        with self._connect() as db:
            rows = db.execute("SELECT * FROM comments WHERE item_id=? ORDER BY created_at, id",
                              (item_id,)).fetchall()
        return [Comment(**dict(row)) for row in rows]
