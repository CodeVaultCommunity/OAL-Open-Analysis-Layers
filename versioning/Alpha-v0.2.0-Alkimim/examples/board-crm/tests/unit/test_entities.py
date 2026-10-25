"""Data validity, without use cases or persistence."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from board_crm.entities import InteractionNote, Opportunity, StageEvent
from board_crm.errors import Invalid


class EntityTests(unittest.TestCase):
    def test_opportunity_fields_and_stage(self):
        card = Opportunity("id", "Title", "Company", "Owner", "NEW", 1, "time", "time")
        self.assertEqual(card.stage, "NEW")
        with self.assertRaises(Invalid):
            Opportunity("id", " ", "Company", "Owner", "NEW", 1, "time", "time")
        with self.assertRaises(Invalid):
            Opportunity("id", "Title", "Company", "Owner", "UNKNOWN", 1, "time", "time")

    def test_note_and_event_fields(self):
        note = InteractionNote("note", "id", "Text", "time")
        event = StageEvent(None, "NEW", "Owner", "time", 1)
        self.assertEqual((note.body, event.destination_stage), ("Text", "NEW"))
        with self.assertRaises(Invalid):
            InteractionNote("note", "id", " ", "time")
        with self.assertRaises(Invalid):
            StageEvent("NEW", "NEW", "Owner", "time", 2)

    def test_versions_must_be_positive_integers(self):
        for value in (True, False, 1.5, "1", None, 0, -1):
            with self.subTest(value=value):
                with self.assertRaises(Invalid):
                    Opportunity("id", "Title", "Company", "Owner", "NEW", value, "time", "time")
                with self.assertRaises(Invalid):
                    StageEvent(None, "NEW", "Owner", "time", value)

    def test_entities_normalize_text_canonically(self):
        card = Opportunity("id", "  Title  ", " Company ", " Owner ", "NEW", 1, "time", "time")
        self.assertEqual((card.title, card.company, card.owner), ("Title", "Company", "Owner"))
        note = InteractionNote("note", "id", "  Text  ", "time")
        event = StageEvent(None, "NEW", "  Owner  ", "time", 1)
        self.assertEqual((note.body, event.actor), ("Text", "Owner"))


if __name__ == "__main__":
    unittest.main()
