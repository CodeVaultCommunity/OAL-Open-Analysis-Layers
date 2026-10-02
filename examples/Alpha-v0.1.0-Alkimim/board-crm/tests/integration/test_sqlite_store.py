"""SQLite tool behavior with its database resource; no use case under test."""
import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from board_crm.entities import Opportunity
from board_crm.errors import Conflict, Missing
from board_crm.tools.sqlite_store import SQLiteStore


class SQLiteStoreTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="oal-crm-store-")
        self.addCleanup(temporary.cleanup)
        self.store = SQLiteStore(Path(temporary.name) / "crm.sqlite3")

    def test_create_and_atomic_stage_note_update(self):
        card = Opportunity("id", "Title", "Company", "Ana", "NEW", 1, "t1", "t1")
        self.store.create(card, "Ana")
        updated = self.store.mutate("id", 1, "t2", "Ana", stage="QUALIFIED",
                                    note_id="n1", note_body="Called")
        self.assertEqual((updated.stage, updated.version), ("QUALIFIED", 2))
        records = self.store.list_records()
        self.assertEqual((records[0][0].version, len(records[0][1]), len(records[0][2])), (2, 1, 2))
        with self.assertRaises(Conflict):
            self.store.mutate("id", 1, "t3", "Ana", stage="PROPOSAL",
                              note_id="n2", note_body="Stale")
        self.assertEqual((len(self.store.list_records()[0][1]), len(self.store.list_records()[0][2])), (1, 2))

    def test_unknown_and_duplicate_ids(self):
        with self.assertRaises(Missing):
            self.store.get("missing")
        card = Opportunity("id", "Title", "Company", "Ana", "NEW", 1, "t1", "t1")
        self.store.create(card, "Ana")
        with self.assertRaises(Conflict):
            self.store.create(card, "Ana")
        self.assertEqual(len(self.store.list_records()), 1)


if __name__ == "__main__":
    unittest.main()
