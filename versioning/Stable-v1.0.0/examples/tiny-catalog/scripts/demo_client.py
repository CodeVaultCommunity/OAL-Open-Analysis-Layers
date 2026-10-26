"""Run a complete observable flow against the local demo; no third-party packages.

Every route is protected, so the client sends HTTP Basic credentials and checks
the expected status of each step. Credentials are never printed; any unexpected
status stops the flow with a clear failure.
"""
import argparse
import base64
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import uuid4

STEPS = [
    ("POST", "/items", 201),
    ("GET", "/items", 200),
    ("POST", "/items/{code}/deactivate", 200),
    ("GET", "/items/{code}", 200),
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--username", default=os.environ.get("OAL_CATALOG_DEMO_USER", "maintainer"))
    parser.add_argument(
        "--password",
        default=os.environ.get("OAL_CATALOG_MAINTAINER_PASSWORD", "maintainer-demo"),
        help="demo credential; prefer the environment variable over the command line",
    )
    args = parser.parse_args()
    base = f"http://127.0.0.1:{args.port}"
    code = "DEMO-" + uuid4().hex[:12].upper()
    token = base64.b64encode(f"{args.username}:{args.password}".encode("utf-8")).decode("ascii")

    def request(method, path, payload, expected):
        data = None if payload is None else json.dumps(payload).encode()
        headers = {"Authorization": "Basic " + token}
        if payload is not None:
            headers["Content-Type"] = "application/json"
        req = Request(base + path, data=data, headers=headers, method=method)
        try:
            response = urlopen(req, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            body = response.read()
            result = json.loads(body) if body else {}
            print(method, path, response.status)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            if response.status != expected:
                raise SystemExit(
                    f"Flow stopped: {method} {path} returned {response.status}, expected {expected}."
                )
            return result

    try:
        registered = request("POST", "/items", {"code": code, "name": "Example notebook"}, 201)
        if registered.get("code") != code or registered.get("active") is not True:
            raise SystemExit("Flow stopped: registration did not return the requested active item.")
        request("GET", "/items", None, 200)
        request("POST", f"/items/{code}/deactivate", None, 200)
        final = request("GET", f"/items/{code}", None, 200)
        if final.get("active") is not False:
            raise SystemExit("Flow stopped: the retained item should be inactive.")
    except (URLError, TimeoutError, OSError) as error:
        print(f"Cannot contact the local demo: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print("Flow completed: all steps returned their expected status.")


if __name__ == "__main__":
    main()
