"""The local HTTP adapter invokes the same specified use cases as the UI."""
from __future__ import annotations

from io import BytesIO
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from board_crm.composition import build_application
from board_crm.transport.wsgi import create_wsgi


class LocalBoardScenario(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="oal-crm-http-")
        self.addCleanup(directory.cleanup)
        self.wsgi = create_wsgi(build_application(Path(directory.name) / "crm.sqlite3"),
                                authenticate=lambda environ: "manager")

    def call(self, method: str, path: str, payload: dict | None = None):
        body = json.dumps(payload).encode() if payload is not None else b""
        status = []
        result = self.wsgi({"REQUEST_METHOD": method, "PATH_INFO": path,
                            "CONTENT_LENGTH": str(len(body)), "wsgi.input": BytesIO(body),
                            "QUERY_STRING": ""}, lambda code, headers: status.append(code))
        return status[0], json.loads(b"".join(result))

    def test_create_move_and_refresh_through_http(self):
        status, created = self.call("POST", "/api/opportunities",
                                    {"title": "Renewal", "company": "Horizon", "owner": "Ana"})
        self.assertEqual(status, "201 Created")
        status, moved = self.call("POST", f"/api/opportunities/{created['id']}/move",
                                  {"stage": "QUALIFIED", "expected_version": 1})
        self.assertEqual((status, moved["version"]), ("200 OK", 2))
        status, board = self.call("GET", "/api/board")
        self.assertEqual((status, board["columns"]["QUALIFIED"][0]["id"]),
                         ("200 OK", created["id"]))
        status, error = self.call("POST", f"/api/opportunities/{created['id']}/move",
                                  {"stage": "PROPOSAL", "expected_version": 1})
        self.assertEqual((status, error["error"]), ("409 Conflict", "conflict"))

    def test_http_authentication_and_case_permission(self):
        directory = tempfile.TemporaryDirectory(prefix="oal-crm-auth-")
        self.addCleanup(directory.cleanup)
        app = build_application(Path(directory.name) / "crm.sqlite3")
        self.wsgi = create_wsgi(app, authenticate=lambda environ: None)
        status, error = self.call("GET", "/api/board")
        self.assertEqual((status, error["error"]), ("401 Unauthorized", "authentication_required"))
        self.wsgi = create_wsgi(app, authenticate=lambda environ: "viewer")
        status, error = self.call("POST", "/api/opportunities",
                                  {"title": "A", "company": "B", "owner": "C"})
        self.assertEqual((status, error["error"]), ("403 Forbidden", "access_denied"))
        status, board = self.call("GET", "/api/board")
        self.assertEqual((status, sum(map(len, board["columns"].values()))), ("200 OK", 0))


if __name__ == "__main__":
    unittest.main()
