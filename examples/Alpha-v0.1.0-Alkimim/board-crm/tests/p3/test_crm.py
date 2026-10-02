"""Behavioral scenarios linked to the UCS acceptance criteria."""
from __future__ import annotations

from functools import wraps
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from board_crm.composition import build_application
from board_crm.errors import AccessDenied, AuthenticationRequired, Conflict, Invalid


def criterion(*ids: str):
    def decorate(test):
        @wraps(test)
        def run(*args, **kwargs):
            return test(*args, **kwargs)
        run.ucs_criteria = ids
        return run
    return decorate


class CrmScenarios(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="oal-board-crm-")
        self.addCleanup(self.temporary.cleanup)
        self.app = build_application(Path(self.temporary.name) / "crm.sqlite3").for_actor("manager")

    def create(self, title="Renewal", owner="Ana"):
        return self.app.create(title, "Horizon", owner)

    @criterion("AC-CRM-001-04", "AC-CRM-002-05", "AC-CRM-003-04",
               "AC-CRM-004-04", "AC-CRM-005-04", "AC-CRM-006-04")
    def test_case_permissions_deny_before_effects(self):
        raw = build_application(Path(self.temporary.name) / "permissions.sqlite3")
        with self.assertRaises(AuthenticationRequired):
            raw.create("A", "B", "C")
        with self.assertRaises(AuthenticationRequired):
            raw.board()
        viewer = raw.for_actor("viewer")
        self.assertEqual(viewer.board()["NEW"], [])
        with self.assertRaises(AccessDenied):
            viewer.create("A", "B", "C")
        with self.assertRaises(AccessDenied):
            viewer.move("missing", "QUALIFIED", 1, "viewer")
        with self.assertRaises(AccessDenied):
            viewer.note("missing", "note", 1, "viewer")
        with self.assertRaises(AccessDenied):
            viewer.won("missing", "reason", 1, "viewer")
        with self.assertRaises(AccessDenied):
            viewer.lost("missing", "reason", 1, "viewer")
        operator = raw.for_actor("operator")
        with self.assertRaises(AccessDenied):
            operator.won("missing", "reason", 1, "operator")
        with self.assertRaises(AccessDenied):
            operator.lost("missing", "reason", 1, "operator")
        with self.assertRaises(AccessDenied):
            raw.for_actor("unknown").board()
        self.assertEqual(raw.for_actor("manager").board()["NEW"], [])

    @criterion("AC-CRM-001-01", "AC-CRM-001-02", "AC-CRM-001-03")
    def test_create_checks_fields_and_initial_event(self):
        card = self.create()
        self.assertEqual((card.stage, card.version), ("NEW", 1))
        self.assertEqual(len(self.app.board()["NEW"]), 1)
        self.assertEqual(len(self.app.board()["NEW"][0]["history"]), 1)
        with self.assertRaises(Invalid):
            self.create("   ")
        with self.assertRaises(Invalid):
            self.create("x" * 81)
        self.assertEqual(len(self.app.board()["NEW"]), 1)

    @criterion("AC-CRM-002-01", "AC-CRM-002-02", "AC-CRM-002-03", "AC-CRM-002-04")
    def test_move_is_adjacent_and_versioned(self):
        card = self.create()
        with self.assertRaises(Invalid):
            self.app.move(card.id, "PROPOSAL", 1, "Ana")
        moved = self.app.move(card.id, "QUALIFIED", 1, "Ana")
        self.assertEqual((moved.stage, moved.version), ("QUALIFIED", 2))
        self.assertEqual(len(self.app.board()["QUALIFIED"][0]["history"]), 2)
        with self.assertRaises(Conflict):
            self.app.move(card.id, "PROPOSAL", 1, "Ana")
        self.assertEqual(len(self.app.board()["QUALIFIED"][0]["history"]), 2)
        lost = self.app.lost(card.id, "Budget withdrawn", 2, "Ana")
        with self.assertRaises(Invalid):
            self.app.move(card.id, "PROPOSAL", lost.version, "Ana")

    @criterion("AC-CRM-003-01", "AC-CRM-003-02", "AC-CRM-003-03")
    def test_notes_increment_once_and_work_after_closure(self):
        card = self.create()
        result = self.app.note(card.id, " Called prospect ", 1, "Ana")
        self.assertEqual(result["version"], 2)
        self.assertEqual(self.app.board()["NEW"][0]["notes"][0]["body"], "Called prospect")
        with self.assertRaises(Invalid):
            self.app.note(card.id, "   ", 2, "Ana")
        with self.assertRaises(Invalid):
            self.app.note(card.id, "x" * 501, 2, "Ana")
        self.assertEqual(self.app.board()["NEW"][0]["version"], 2)
        closed = self.app.lost(card.id, "No demand", 2, "Ana")
        self.app.note(card.id, "Follow-up archived", closed.version, "Ana")
        self.assertEqual(len(self.app.board()["LOST"][0]["notes"]), 3)

    @criterion("AC-CRM-004-01", "AC-CRM-004-02", "AC-CRM-004-03")
    def test_board_includes_all_columns_and_exact_owner_filter(self):
        first = self.create("A", "Ana")
        second = self.create("B", "Bia")
        moved = self.app.move(first.id, "QUALIFIED", 1, "Ana")
        self.app.move(first.id, "PROPOSAL", moved.version, "Ana")
        board = self.app.board()
        self.assertEqual(set(board), {"NEW", "QUALIFIED", "PROPOSAL", "WON", "LOST"})
        self.assertEqual(board["NEW"][0]["id"], second.id)
        self.assertEqual(board["PROPOSAL"][0]["id"], first.id)
        self.assertEqual(len(self.app.board("Ana")["PROPOSAL"]), 1)
        self.assertEqual(len(self.app.board("ana")["PROPOSAL"]), 0)
        self.assertEqual(self.app.board(), board)

    @criterion("AC-CRM-005-01", "AC-CRM-005-02", "AC-CRM-005-03")
    def test_won_requires_proposal_and_records_reason(self):
        card = self.create()
        with self.assertRaises(Invalid):
            self.app.won(card.id, "Signed", 1, "Ana")
        qualified = self.app.move(card.id, "QUALIFIED", 1, "Ana")
        proposal = self.app.move(card.id, "PROPOSAL", qualified.version, "Ana")
        won = self.app.won(card.id, "Signed agreement", proposal.version, "Ana")
        self.assertEqual((won.stage, won.version), ("WON", 4))
        self.assertEqual(len(self.app.board()["WON"][0]["history"]), 4)
        self.assertEqual(self.app.board()["WON"][0]["notes"][0]["body"], "Signed agreement")
        with self.assertRaises(Invalid):
            self.app.won(card.id, "Again", won.version, "Ana")

    @criterion("AC-CRM-006-01", "AC-CRM-006-02", "AC-CRM-006-03")
    def test_lost_from_each_active_stage_and_stale_rejection(self):
        for stage in ("NEW", "QUALIFIED", "PROPOSAL"):
            with self.subTest(stage=stage):
                card = self.create(stage)
                if stage != "NEW":
                    card = self.app.move(card.id, "QUALIFIED", card.version, "Ana")
                if stage == "PROPOSAL":
                    card = self.app.move(card.id, "PROPOSAL", card.version, "Ana")
                with self.assertRaises(Conflict):
                    self.app.lost(card.id, "No fit", card.version + 1, "Ana")
                before = self.app.board()[card.stage][0]
                self.assertEqual(before["notes"], [])
                lost = self.app.lost(card.id, "No fit", card.version, "Ana")
                self.assertEqual((lost.stage, lost.version), ("LOST", card.version + 1))
                after = next(c for c in self.app.board()["LOST"] if c["id"] == card.id)
                self.assertEqual(len(after["history"]), len(before["history"]) + 1)
                self.assertEqual(len(after["notes"]), 1)
                with self.assertRaises(Invalid):
                    self.app.lost(card.id, "Again", lost.version, "Ana")


if __name__ == "__main__":
    unittest.main()
