"""Optional HTTP transport for the local demo; not part of the UCS.

The adapter authenticates, parses representation, dispatches to use cases, and
maps outcomes. Case permissions are enforced by the cases themselves.
"""
from collections.abc import Callable, Iterable
from http import HTTPStatus
import json
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from tiny_catalog.composition import CatalogApplication
from tiny_catalog.transport.demo_auth import authenticate as demo_authenticate
from tiny_catalog.entities.item import Item
from tiny_catalog.errors import (
    AccessDenied, AuthenticationRequired, DuplicateItem, InvalidData,
    ItemNotFound, PersistenceUnavailable,
)

MAX_BODY_BYTES = 16_384
STATIC = Path(__file__).resolve().parent / "static"
STATIC_ROUTES = {"/": ("index.html", "text/html"),
                 "/app.css": ("app.css", "text/css"),
                 "/app.js": ("app.js", "text/javascript")}


def _item_data(item: Item) -> dict[str, object]:
    """Project entity fields into the transport representation."""
    return {"code": item.code, "name": item.name, "active": item.active}


class CatalogWSGI:
    """A small WSGI adapter with injected application and technical error sink."""

    def __init__(
        self,
        application: CatalogApplication,
        report_error: Callable[[str, Exception], None],
        authenticate: Callable[[dict[str, Any]], str | None] = demo_authenticate,
    ) -> None:
        self._application = application
        self._report_error = report_error
        self._authenticate = authenticate

    def __call__(self, environ: dict[str, Any], start_response: Callable) -> Iterable[bytes]:
        """Handle one request; implementation failures never leak tracebacks to clients."""
        path = environ.get("PATH_INFO", "/")
        if environ.get("REQUEST_METHOD", "GET") == "GET" and path in STATIC_ROUTES:
            name, kind = STATIC_ROUTES[path]
            body = (STATIC / name).read_bytes()
            start_response("200 OK", [("Content-Type", f"{kind}; charset=utf-8"),
                                      ("Content-Length", str(len(body))),
                                      ("Cache-Control", "no-store")])
            return [body]
        try:
            actor = self._authenticate(environ)
            if actor is None:
                raise AuthenticationRequired("valid demo credentials are required")
            status, payload = self._dispatch(environ, actor)
        except AuthenticationRequired as error:
            status, payload = 401, {"error": "authentication_required", "message": str(error)}
        except AccessDenied as error:
            status, payload = 403, {"error": "access_denied", "message": str(error)}
        except InvalidData as error:
            status, payload = 422, {"error": "invalid_data", "field": error.field, "message": str(error)}
        except DuplicateItem as error:
            status, payload = 409, {"error": "duplicate_item", "message": str(error)}
        except ItemNotFound as error:
            status, payload = 404, {"error": "item_not_found", "message": str(error)}
        except PersistenceUnavailable as error:
            self._report_error("persistence_unavailable", error)
            status, payload = 503, {"error": "persistence_unavailable", "message": str(error)}
        except (UnicodeDecodeError, json.JSONDecodeError, _RequestError) as error:
            status, payload = 400, {"error": "invalid_request", "message": str(error)}
        except Exception as error:
            self._report_error("unexpected_failure", error)
            status, payload = 500, {"error": "internal_error"}
        body = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
        headers = [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("Cache-Control", "no-store"),
        ]
        if status == 401:
            headers.append(("WWW-Authenticate", 'Basic realm="OAL Tiny Catalog"'))
        start_response(
            f"{status} {HTTPStatus(status).phrase}",
            headers,
        )
        return [body]

    def _dispatch(self, environ: dict[str, Any], actor: str) -> tuple[int, object]:
        method = environ.get("REQUEST_METHOD", "GET")
        path = unquote(environ.get("PATH_INFO", "/"))
        cases = self._application.for_actor(actor)
        if path == "/items":
            if method == "GET":
                return 200, {"items": [_item_data(x) for x in cases.list_available.execute()]}
            if method == "POST":
                data = self._body(environ)
                if set(data) != {"code", "name"}:
                    raise _RequestError("expected exactly code and name")
                return 201, _item_data(cases.register.execute(data["code"], data["name"]))
            return 405, {"error": "method_not_allowed"}
        parts = path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "items":
            if method != "GET":
                return 405, {"error": "method_not_allowed"}
            return 200, _item_data(cases.get.execute(parts[1]))
        if len(parts) == 3 and parts[0] == "items" and parts[2] == "deactivate":
            if method != "POST":
                return 405, {"error": "method_not_allowed"}
            if environ.get("CONTENT_LENGTH") not in (None, "", "0"):
                raise _RequestError("deactivation does not accept a request body")
            return 200, _item_data(cases.deactivate.execute(parts[1]))
        return 404, {"error": "route_not_found"}

    @staticmethod
    def _body(environ: dict[str, Any]) -> dict[str, Any]:
        if environ.get("HTTP_TRANSFER_ENCODING"):
            raise _RequestError("transfer encoding is not supported by this demo")
        if environ.get("CONTENT_TYPE", "").split(";", 1)[0].strip().lower() != "application/json":
            raise _RequestError("Content-Type must be application/json")
        try:
            length = int(environ.get("CONTENT_LENGTH") or "0")
        except (TypeError, ValueError) as error:
            raise _RequestError("invalid Content-Length") from error
        if not 0 < length <= MAX_BODY_BYTES:
            raise _RequestError(f"body must contain 1 to {MAX_BODY_BYTES} bytes")
        raw = environ["wsgi.input"].read(length)
        if len(raw) != length:
            raise _RequestError("incomplete request body")
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise _RequestError("JSON body must be an object")
        return data


class _RequestError(Exception):
    """Transport-only rejection, not a catalog rule."""
