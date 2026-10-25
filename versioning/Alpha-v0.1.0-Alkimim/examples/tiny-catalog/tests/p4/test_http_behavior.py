"""The same case obligations exercised through the example's optional transport.

A live loopback server is used to check the optional interaction channel around
the use cases.
"""
from http import HTTPStatus
import json
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from wsgiref.simple_server import WSGIRequestHandler, make_server
import pytest

from tiny_catalog.composition import build_application
from tiny_catalog.transport.wsgi import CatalogWSGI


@pytest.mark.criterion("AC-CAT-001-01", "AC-CAT-001-03", "AC-CAT-004-01", "AC-CAT-002-01", "AC-CAT-003-02")
def test_registration_and_deactivation_are_observable_over_http(tmp_path):
    app = build_application(tmp_path / "http.sqlite3")
    observed_errors = []
    handler = CatalogWSGI(app, lambda kind, error: observed_errors.append(kind),
                          authenticate=lambda environ: "maintainer")

    class QuietHandler(WSGIRequestHandler):
        def log_message(self, format, *args):
            pass

    with make_server("127.0.0.1", 0, handler, handler_class=QuietHandler) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"

        def request(method, path, payload=None):
            data = None if payload is None else json.dumps(payload).encode()
            headers = {} if payload is None else {"Content-Type": "application/json"}
            req = Request(base + path, data=data, headers=headers, method=method)
            try:
                response = urlopen(req, timeout=5)
            except HTTPError as error:
                response = error
            with response:
                return response.status, json.loads(response.read())

        try:
            status, record = request("POST", "/items", {"code": "A", "name": "Original"})
            assert status == HTTPStatus.CREATED and record["active"] is True
            assert request("POST", "/items", {"code": "A", "name": "Other"})[0] == 409
            assert request("POST", "/items/A/deactivate")[1]["active"] is False
            assert request("GET", "/items")[1] == {"items": []}
            assert request("GET", "/items/A")[1] == {"code": "A", "name": "Original", "active": False}
            assert observed_errors == []
        finally:
            server.shutdown()
            thread.join(timeout=5)
