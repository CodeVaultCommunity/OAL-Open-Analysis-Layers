"""Three directed regression checks for the release verifiers."""
from pathlib import Path
import json
import subprocess
import tempfile
import unittest

from check_structure import check_origins
from content_inventory import build, check


class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "VERSION").write_bytes(b"Stable-v1.0.0\n")
        (self.root / "payload.txt").write_bytes(b"original\n")
        subprocess.run(["git", "-c", "core.autocrlf=false", "add", "VERSION", "payload.txt"], cwd=self.root, check=True)
        self.inventory = self.root / "CONTENT-SHA256.json"
        self.inventory.write_text(json.dumps(build(self.root)), encoding="utf-8")
        self.assertEqual(check(self.root), [])

    def tearDown(self):
        self.temp.cleanup()

    def test_altered_hash_is_rejected(self):
        data = json.loads(self.inventory.read_text(encoding="utf-8"))
        data["files"][0]["sha256"] = "0" * 64
        self.inventory.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("hash/size" in error for error in check(self.root)))

    def test_omitted_indexed_file_is_rejected(self):
        data = json.loads(self.inventory.read_text(encoding="utf-8"))
        data["files"] = [entry for entry in data["files"] if entry["path"] != "payload.txt"]
        self.inventory.write_text(json.dumps(data), encoding="utf-8")
        self.assertIn("omitted indexed file: payload.txt", check(self.root))

    def test_unadmitted_origin_is_rejected(self):
        self.assertEqual(check_origins([{"id": "O-WB-AVAIL", "origin": "domain"}]), [])
        errors = check_origins([{"id": "O-WB-AVAIL", "origin": "baseline-decision"}])
        self.assertEqual(len(errors), 1)
        self.assertIn("invalid origin for O-WB-AVAIL", errors[0])


if __name__ == "__main__":
    unittest.main()
