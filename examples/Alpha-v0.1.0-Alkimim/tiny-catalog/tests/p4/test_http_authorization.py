"""Check identity handling at the local HTTP boundary."""
from io import BytesIO
import json
import pytest

from tiny_catalog.composition import build_application
from tiny_catalog.transport.wsgi import CatalogWSGI


@pytest.mark.criterion("AC-CAT-001-06", "AC-CAT-003-04")
def test_http_boundary_challenges_identity_and_denies_reader_write(tmp_path):
    app = build_application(tmp_path / "http-auth.sqlite3")

    def call(handler, method, path, body=b""):
        observed = []
        response = handler({"REQUEST_METHOD": method, "PATH_INFO": path,
                            "CONTENT_LENGTH": str(len(body)), "CONTENT_TYPE": "application/json",
                            "wsgi.input": BytesIO(body)},
                           lambda status, headers: observed.append((status, dict(headers))))
        return observed[0], json.loads(b"".join(response))

    missing = CatalogWSGI(app, lambda kind, error: None, authenticate=lambda env: None)
    (status, headers), payload = call(missing, "GET", "/items")
    assert status.startswith("401") and "WWW-Authenticate" in headers
    assert payload["error"] == "authentication_required"

    reader = CatalogWSGI(app, lambda kind, error: None, authenticate=lambda env: "reader")
    (status, _), payload = call(reader, "POST", "/items", b'{"code":"A","name":"Book"}')
    assert status.startswith("403") and payload["error"] == "access_denied"
    assert app.for_actor("reader").list_available.execute() == []
