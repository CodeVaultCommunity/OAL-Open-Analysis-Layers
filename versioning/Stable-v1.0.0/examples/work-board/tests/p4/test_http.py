"""HTTP checks for the P4 adapter, separate from the callable cases."""
import base64
from io import BytesIO
import json
import sqlite3

from work_board.composition import build_application
from work_board.transport.wsgi import create_wsgi


def request(handler, method, path, *, actor=None, password=None, payload=None, query=""):
    raw = json.dumps(payload).encode() if payload is not None else b""
    environ = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": query,
               "CONTENT_LENGTH": str(len(raw)), "CONTENT_TYPE": "application/json",
               "wsgi.input": BytesIO(raw)}
    if actor:
        password = password or f"{actor}-demo"
        token = base64.b64encode(f"{actor}:{password}".encode()).decode()
        environ["HTTP_AUTHORIZATION"] = "Basic " + token
    result = {}

    def start_response(status, headers):
        result["status"], result["headers"] = status, dict(headers)

    data = b"".join(handler(environ, start_response))
    return int(result["status"].split()[0]), data, result["headers"]


def test_static_and_authentication(tmp_path):
    handler = create_wsgi(build_application(tmp_path / "work.sqlite3"))
    status, body, _ = request(handler, "GET", "/")
    assert status == 200 and b"Work Board" in body
    status, body, headers = request(handler, "GET", "/api/items")
    assert status == 401 and "WWW-Authenticate" in headers


def test_real_authenticator_refuses_non_ascii_password_without_failing(tmp_path):
    handler = create_wsgi(build_application(tmp_path / "work.sqlite3"))
    for password in ("wrong-password", "senha-inválida-çãõ"):
        status, body, headers = request(handler, "GET", "/api/items", actor="manager", password=password)
        assert status == 401 and json.loads(body)["error"] == "authentication_required"
        assert "WWW-Authenticate" in headers


def test_create_assign_transition_comment_and_read(tmp_path):
    handler = create_wsgi(build_application(tmp_path / "work.sqlite3"))
    status, body, _ = request(handler, "POST", "/api/items", actor="manager",
                              payload={"project": "Site", "title": "Fix login"})
    item = json.loads(body)
    assert status == 201 and item["status"] == "backlog"
    item_id = item["id"]
    status, _, _ = request(handler, "POST", f"/api/items/{item_id}/assign",
                           actor="contributor", payload={"assignee": "Ana", "expected_version": 1})
    assert status == 403
    status, body, _ = request(handler, "POST", f"/api/items/{item_id}/assign",
                              actor="manager", payload={"assignee": "Ana", "expected_version": 1})
    assert status == 200 and json.loads(body)["version"] == 2
    status, body, _ = request(handler, "POST", f"/api/items/{item_id}/transition",
                              actor="contributor", payload={"status": "in_progress", "expected_version": 2})
    assert status == 200 and json.loads(body)["status"] == "in_progress"
    status, _, _ = request(handler, "POST", f"/api/items/{item_id}/comments",
                           actor="contributor", payload={"body": "Checked"})
    assert status == 201
    status, body, _ = request(handler, "GET", f"/api/items/{item_id}/comments", actor="viewer")
    assert status == 200 and json.loads(body)["comments"][0]["body"] == "Checked"
    status, body, _ = request(handler, "GET", "/api/items", actor="viewer", query="project=Site")
    assert status == 200 and len(json.loads(body)["items"]) == 1


def test_bad_input_and_conflict(tmp_path):
    handler = create_wsgi(build_application(tmp_path / "work.sqlite3"))
    status, body, _ = request(handler, "POST", "/api/items", actor="manager",
                              payload={"project": "Site", "title": "Fix login"})
    item_id = json.loads(body)["id"]
    assert status == 201
    status, _, _ = request(handler, "POST", f"/api/items/{item_id}/transition",
                           actor="manager", payload={"status": "done", "expected_version": 1})
    assert status == 400
    status, _, _ = request(handler, "POST", f"/api/items/{item_id}/assign",
                           actor="manager", payload={"assignee": "Ana", "expected_version": 1})
    assert status == 200
    status, _, _ = request(handler, "POST", f"/api/items/{item_id}/assign",
                           actor="manager", payload={"assignee": "Bruno", "expected_version": 1})
    assert status == 409



def test_large_expected_version_returns_conflict_or_missing(tmp_path):
    app = build_application(tmp_path / "work.sqlite3")
    item = app.create.execute("Site", "Fix", principal="manager")
    handler = create_wsgi(app)
    for action, field, value in (("assign", "assignee", "Ana"),
                                  ("transition", "status", "in_progress")):
        for item_id, expected in ((item.id, 409), ("absent", 404)):
            status, body, _ = request(handler, "POST", f"/api/items/{item_id}/{action}",
                                      actor="manager", payload={field: value, "expected_version": 2**63})
            assert status == expected
            assert json.loads(body)["error"] == ("conflict" if expected == 409 else "not_found")
    assert app.view.execute(principal="viewer") == [item]


def test_storage_failure_returns_503_and_known_write_outcome(tmp_path):
    path = tmp_path / "work.sqlite3"
    app = build_application(path)
    item = app.create.execute("Site", "Fix", principal="manager")
    handler = create_wsgi(app)
    with sqlite3.connect(path) as db:
        db.execute("ALTER TABLE items RENAME TO temporarily_unavailable_items")
    for method, payload in (("GET", None), ("POST", {"project": "Site", "title": "Second"})):
        status, body, _ = request(handler, method, "/api/items", actor="manager", payload=payload)
        result = json.loads(body)
        assert status == 503
        assert result["error"] == "unavailable" and result["write_outcome"] == "not_applied"
        assert "sqlite" not in result["message"].lower()
    with sqlite3.connect(path) as db:
        db.execute("ALTER TABLE temporarily_unavailable_items RENAME TO items")
    assert app.view.execute(principal="viewer") == [item]


def test_unconfirmed_commit_is_reported_as_unknown_over_http(tmp_path, monkeypatch):
    app = build_application(tmp_path / "work.sqlite3")
    item = app.create.execute("Site", "Fix", principal="manager")
    handler = create_wsgi(app)
    connect = sqlite3.connect

    class LostAcknowledgement(sqlite3.Connection):
        def commit(self):
            super().commit()
            raise sqlite3.OperationalError("injected lost acknowledgement")

    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", lambda *args, **kwargs:
                      connect(*args, **kwargs, factory=LostAcknowledgement))
        status, body, _ = request(handler, "POST", f"/api/items/{item.id}/assign",
                                  actor="manager", payload={"assignee": "Ana", "expected_version": 1})
    assert status == 503
    assert json.loads(body)["write_outcome"] == "unknown"
    observed = app.view.execute(principal="viewer")[0]
    assert (observed.assignee, observed.version) == ("Ana", 2)
