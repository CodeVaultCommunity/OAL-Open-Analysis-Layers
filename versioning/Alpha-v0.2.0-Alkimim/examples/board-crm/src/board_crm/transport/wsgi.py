"""Loopback WSGI adapter for the Board CRM use cases."""
from __future__ import annotations

from dataclasses import asdict
from email.message import Message
import json
from pathlib import Path
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from ..composition import Application, build_application
from ..errors import CrmError, Invalid
from .demo_auth import authenticate as demo_authenticate

STATIC = Path(__file__).parent / "static"
STATUS = {"invalid": "400 Bad Request", "not_found": "404 Not Found",
          "conflict": "409 Conflict", "unavailable": "503 Service Unavailable",
          "authentication_required": "401 Unauthorized", "access_denied": "403 Forbidden"}


def create_wsgi(app: Application, authenticate=demo_authenticate):
    def respond(start_response, status: str, body: bytes, content_type: str):
        start_response(status, [("Content-Type", content_type),
                                ("Content-Length", str(len(body))),
                                ("Cache-Control", "no-store")])
        return [body]

    def json_reply(start_response, status: str, value: object):
        return respond(start_response, status,
                       json.dumps(value, ensure_ascii=False).encode("utf-8"),
                       "application/json; charset=utf-8")

    def unauthorized(start_response):
        body = b'{"error":"authentication_required"}'
        start_response("401 Unauthorized", [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("Cache-Control", "no-store"),
            ("WWW-Authenticate", 'Basic realm="OAL Board CRM"'),
        ])
        return [body]

    def handler(environ, start_response):
        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET")
        if method == "GET" and path in {"/", "/app.js", "/app.css"}:
            name = {"/": "index.html", "/app.js": "app.js", "/app.css": "app.css"}[path]
            kind = {"index.html": "text/html", "app.js": "text/javascript", "app.css": "text/css"}[name]
            return respond(start_response, "200 OK", (STATIC / name).read_bytes(),
                           kind + "; charset=utf-8")
        try:
            actor = authenticate(environ)
            if actor is None:
                return unauthorized(start_response)
            cases = app.for_actor(actor)
            if method == "GET" and path == "/api/board":
                owner = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=True).get("owner", [None])[0]
                return json_reply(start_response, "200 OK", {"columns": cases.board(owner)})
            if method == "POST":
                media_type = Message()
                media_type["Content-Type"] = environ.get("CONTENT_TYPE", "")
                if (media_type.get_content_type() != "application/json"
                        or media_type.get_content_charset("utf-8") not in {"utf-8", "utf8"}):
                    return json_reply(start_response, "415 Unsupported Media Type",
                                      {"error": "unsupported_media_type",
                                       "message": "Content-Type must be application/json with UTF-8 encoding"})
                try:
                    length = int(environ.get("CONTENT_LENGTH", "0"))
                except ValueError as error:
                    raise Invalid("invalid request length") from error
                if length < 1 or length > 65536 or environ.get("HTTP_TRANSFER_ENCODING"):
                    raise Invalid("request body must be 1–65536 bytes")
                raw = environ["wsgi.input"].read(length)
                if len(raw) != length:
                    raise Invalid("incomplete request body")
                try:
                    payload = json.loads(raw.decode("utf-8"))
                except (ValueError, UnicodeError) as error:
                    raise Invalid("invalid JSON body") from error
                if not isinstance(payload, dict):
                    raise Invalid("JSON body must be an object")
                if path == "/api/opportunities":
                    card = cases.create(payload.get("title"), payload.get("company"), payload.get("owner"))
                    return json_reply(start_response, "201 Created", asdict(card))
                parts = path.strip("/").split("/")
                if len(parts) == 4 and parts[:2] == ["api", "opportunities"]:
                    card_id, action = parts[2], parts[3]
                    version = payload.get("expected_version")
                    if action == "move":
                        result = cases.move(card_id, payload.get("stage"), version, actor)
                    elif action == "notes":
                        result = cases.note(card_id, payload.get("body"), version, actor)
                    elif action == "close-won":
                        result = cases.won(card_id, payload.get("reason"), version, actor)
                    elif action == "close-lost":
                        result = cases.lost(card_id, payload.get("reason"), version, actor)
                    else:
                        return json_reply(start_response, "404 Not Found", {"error": "route not found"})
                    return json_reply(start_response, "200 OK", asdict(result) if not isinstance(result, dict) else result)
            return json_reply(start_response, "404 Not Found", {"error": "route not found"})
        except CrmError as error:
            return json_reply(start_response, STATUS[error.code], {"error": error.code, "message": str(error)})
    return handler


def serve(database: Path, port: int) -> None:
    app = build_application(database)
    with make_server("127.0.0.1", port, create_wsgi(app)) as server:
        print(f"Board CRM: http://127.0.0.1:{port}", flush=True)
        server.serve_forever()
