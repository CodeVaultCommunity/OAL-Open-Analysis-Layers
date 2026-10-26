"""Check the real demonstration authenticator at the local HTTP boundary.

The lambda substitutes in other channel tests do not cover the Basic credential
mechanism itself; these checks exercise tiny_catalog.transport.demo_auth through
CatalogWSGI, including a non-ASCII password, which must be a normal 401 refusal.
"""
import base64
from io import BytesIO
import json
import pytest

from tiny_catalog.composition import build_application
from tiny_catalog.transport.demo_auth import PASSWORDS, authenticate
from tiny_catalog.transport.wsgi import CatalogWSGI


def _basic(username: str, password: str) -> str:
    token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return "Basic " + token


def _call(handler, environ_extra):
    observed = []
    environ = {"REQUEST_METHOD": "GET", "PATH_INFO": "/items",
               "CONTENT_LENGTH": "0", "CONTENT_TYPE": "application/json",
               "wsgi.input": BytesIO(b"")}
    environ.update(environ_extra)
    response = handler(environ, lambda status, headers: observed.append((status, dict(headers))))
    return observed[0], json.loads(b"".join(response))


def test_real_authenticator_accepts_demo_credentials(tmp_path):
    app = build_application(tmp_path / "real-auth.sqlite3")
    handler = CatalogWSGI(app, lambda kind, error: None)
    (status, _), payload = _call(handler, {"HTTP_AUTHORIZATION": _basic("maintainer", PASSWORDS["maintainer"])})
    assert status.startswith("200") and payload == {"items": []}


@pytest.mark.criterion("AC-CAT-001-06")
def test_real_authenticator_refuses_wrong_and_non_ascii_passwords(tmp_path):
    app = build_application(tmp_path / "real-auth.sqlite3")
    handler = CatalogWSGI(app, lambda kind, error: None)
    for password in ("wrong-password", "senha-inválida-çãõ"):
        (status, headers), payload = _call(handler, {"HTTP_AUTHORIZATION": _basic("maintainer", password)})
        assert status.startswith("401"), f"password {password!r} must be refused as unauthenticated"
        assert payload["error"] == "authentication_required"
        assert "WWW-Authenticate" in headers


def test_authenticate_never_raises_for_malformed_or_non_ascii_credentials():
    cases = [
        {},
        {"HTTP_AUTHORIZATION": "Bearer abc"},
        {"HTTP_AUTHORIZATION": "Basic !!!not-base64!!!"},
        {"HTTP_AUTHORIZATION": "Basic " + base64.b64encode(b"not-utf8-\xff\xfe").decode("ascii")},
        {"HTTP_AUTHORIZATION": _basic("unknown-user", "whatever")},
        {"HTTP_AUTHORIZATION": _basic("maintainer", "senha-inválida-çãõ")},
        {"HTTP_AUTHORIZATION": _basic("maintainer", PASSWORDS["maintainer"] + "x")},
    ]
    for environ in cases:
        assert authenticate(environ) is None, f"expected refusal for {sorted(environ)}"
    assert authenticate({"HTTP_AUTHORIZATION": _basic("reader", PASSWORDS["reader"])}) == "reader"
