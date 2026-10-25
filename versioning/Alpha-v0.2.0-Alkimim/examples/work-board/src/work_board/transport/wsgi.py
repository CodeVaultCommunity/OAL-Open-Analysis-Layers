"""Local browser and JSON boundary; no workflow or case permission rules."""
from dataclasses import asdict
from http import HTTPStatus
import json
from pathlib import Path
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from ..composition import Application, build_application
from ..errors import Unavailable, WorkBoardError
from .demo_auth import authenticate as default_authenticate


STATIC = Path(__file__).parent / "static"
STATIC_FILES = {"/": ("index.html", "text/html"),
                "/app.js": ("app.js", "text/javascript"),
                "/app.css": ("app.css", "text/css")}
ERROR_STATUS = {"authentication_required": 401, "access_denied": 403, "invalid": 400,
                "not_found": 404, "conflict": 409, "unavailable": 503}


def create_wsgi(app: Application, authenticate=default_authenticate):
    def reply(start_response, status: int, value, *, content_type="application/json; charset=utf-8"):
        body = (json.dumps(value, ensure_ascii=False).encode("utf-8")
                if content_type.startswith("application/json") else value)
        headers = [("Content-Type", content_type), ("Content-Length", str(len(body))),
                   ("Cache-Control", "no-store")]
        if status == 401:
            headers.append(("WWW-Authenticate", 'Basic realm="OAL Work Board"'))
        start_response(f"{status} {HTTPStatus(status).phrase}", headers)
        return [body]

    def body(environ):
        try:
            length = int(environ.get("CONTENT_LENGTH", ""))
        except ValueError as error:
            raise ValueError("Content-Length is required") from error
        if not 1 <= length <= 65536 or environ.get("HTTP_TRANSFER_ENCODING"):
            raise ValueError("request body must have 1–65536 bytes")
        if environ.get("CONTENT_TYPE", "").split(";", 1)[0].lower() != "application/json":
            raise ValueError("Content-Type must be application/json")
        raw = environ["wsgi.input"].read(length)
        if len(raw) != length:
            raise ValueError("incomplete request body")
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("request body must be a JSON object")
        return data

    def handler(environ, start_response):
        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET").upper()
        if method == "GET" and path in STATIC_FILES:
            name, mime = STATIC_FILES[path]
            return reply(start_response, 200, (STATIC / name).read_bytes(),
                         content_type=f"{mime}; charset=utf-8")
        if not path.startswith("/api/"):
            return reply(start_response, 404, {"error": "route_not_found"})
        actor = authenticate(environ)
        if actor is None:
            return reply(start_response, 401, {"error": "authentication_required"})
        try:
            if path == "/api/items" and method == "GET":
                query = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=True)
                project = query.get("project", [None])[0]
                status = query.get("status", [None])[0]
                return reply(start_response, 200, {"items": [asdict(item) for item in
                             app.view.execute(project, status, principal=actor)]})
            if path == "/api/items" and method == "POST":
                data = body(environ)
                item = app.create.execute(data.get("project"), data.get("title"),
                                          data.get("description", ""), data.get("priority", "normal"),
                                          principal=actor)
                return reply(start_response, 201, asdict(item))
            parts = path.strip("/").split("/")
            if len(parts) == 4 and parts[:2] == ["api", "items"] and method == "POST":
                item_id, action = parts[2:]
                data = body(environ)
                if action == "assign":
                    item = app.assign.execute(item_id, data.get("assignee"),
                                              data.get("expected_version"), principal=actor)
                    return reply(start_response, 200, asdict(item))
                if action == "transition":
                    item = app.transition.execute(item_id, data.get("status"),
                                                  data.get("expected_version"), principal=actor)
                    return reply(start_response, 200, asdict(item))
                if action == "comments":
                    comment = app.comment.execute(item_id, data.get("body"), principal=actor)
                    return reply(start_response, 201, asdict(comment))
            if len(parts) == 4 and parts[:2] == ["api", "items"] and parts[3] == "comments" and method == "GET":
                return reply(start_response, 200, {"comments": [asdict(comment) for comment in
                             app.view_comments.execute(parts[2], principal=actor)]})
            return reply(start_response, 404, {"error": "route_not_found"})
        except WorkBoardError as error:
            result = {"error": error.code, "message": str(error)}
            if isinstance(error, Unavailable):
                result["write_outcome"] = error.write_outcome
            return reply(start_response, ERROR_STATUS[error.code], result)
        except (ValueError, KeyError, TypeError, UnicodeError, json.JSONDecodeError) as error:
            return reply(start_response, 400, {"error": "invalid_request", "message": str(error)})

    return handler


def serve(database: Path, port: int = 8002) -> None:
    with make_server("127.0.0.1", port, create_wsgi(build_application(database))) as server:
        print(f"work-board: http://127.0.0.1:{port}/\nPress Ctrl+C to stop.", flush=True)
        server.serve_forever()
