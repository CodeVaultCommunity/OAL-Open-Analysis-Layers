"""HTTP checks for the P4 adapter, separate from the callable cases."""
import base64
from io import BytesIO
import json

from work_board.composition import build_application
from work_board.transport.wsgi import create_wsgi


def request(handler, method, path, *, actor=None, payload=None, query=""):
    raw = json.dumps(payload).encode() if payload is not None else b""
    environ = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": query,
               "CONTENT_LENGTH": str(len(raw)), "CONTENT_TYPE": "application/json",
               "wsgi.input": BytesIO(raw)}
    if actor:
        password = f"{actor}-demo"
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

