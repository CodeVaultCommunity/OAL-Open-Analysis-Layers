"""The local HTTP adapter invokes the same specified use cases as the UI."""
from __future__ import annotations

from io import BytesIO
import base64
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from board_crm.composition import build_application
from board_crm.transport.demo_auth import PASSWORDS
from board_crm.transport.wsgi import create_wsgi


class LocalBoardScenario(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="oal-crm-http-")
        self.addCleanup(directory.cleanup)
        self.wsgi = create_wsgi(build_application(Path(directory.name) / "crm.sqlite3"),
                                authenticate=lambda environ: "manager")

    def call(self, method: str, path: str, payload: dict | None = None, headers: dict | None = None):
        body = json.dumps(payload).encode() if payload is not None else b""
        status = []
        environ = {"REQUEST_METHOD": method, "PATH_INFO": path,
                   "CONTENT_LENGTH": str(len(body)), "wsgi.input": BytesIO(body),
                   "CONTENT_TYPE": "application/json",
                   "QUERY_STRING": ""}
        environ.update(headers or {})
        result = self.wsgi(environ, lambda code, response_headers: status.append(code))
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

    def test_real_authenticator_accepts_and_refuses_credentials(self):
        directory = tempfile.TemporaryDirectory(prefix="oal-crm-real-auth-")
        self.addCleanup(directory.cleanup)
        self.wsgi = create_wsgi(build_application(Path(directory.name) / "crm.sqlite3"))

        def basic(username, password):
            token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
            return {"HTTP_AUTHORIZATION": "Basic " + token}

        status, board = self.call("GET", "/api/board", headers=basic("manager", PASSWORDS["manager"]))
        self.assertEqual((status, board["columns"]["NEW"]), ("200 OK", []))
        for password in ("wrong-password", "senha-inválida-çãõ"):
            with self.subTest(password=password):
                status, error = self.call("GET", "/api/board", headers=basic("manager", password))
                self.assertEqual((status, error["error"]), ("401 Unauthorized", "authentication_required"))

    def test_json_media_type_and_charset(self):
        payload = {"title": "Renewal", "company": "Horizon", "owner": "Ana"}
        for content_type in ("text/plain", "", "application/json; charset=iso-8859-1"):
            with self.subTest(content_type=content_type):
                status, error = self.call("POST", "/api/opportunities", payload,
                                          {"CONTENT_TYPE": content_type})
                self.assertEqual((status, error["error"]),
                                 ("415 Unsupported Media Type", "unsupported_media_type"))
        _, board = self.call("GET", "/api/board")
        self.assertEqual(sum(map(len, board["columns"].values())), 0)
        status, created = self.call("POST", "/api/opportunities", payload,
                                    {"CONTENT_TYPE": "Application/JSON; charset=UTF-8"})
        self.assertEqual((status, created["title"]), ("201 Created", "Renewal"))

    def test_incomplete_and_unsupported_framing_are_rejected_without_creation(self):
        payload = {"title": "Renewal", "company": "Horizon", "owner": "Ana"}
        actual_length = len(json.dumps(payload).encode())
        for headers in ({"CONTENT_LENGTH": str(actual_length + 50)},
                        {"CONTENT_LENGTH": str(actual_length - 1)},
                        {"HTTP_TRANSFER_ENCODING": "chunked"},
                        {"CONTENT_LENGTH": "65537"}):
            with self.subTest(headers=headers):
                status, error = self.call("POST", "/api/opportunities", payload, headers)
                self.assertEqual((status, error["error"]), ("400 Bad Request", "invalid"))
        _, board = self.call("GET", "/api/board")
        self.assertEqual(sum(map(len, board["columns"].values())), 0)


if __name__ == "__main__":
    unittest.main()
