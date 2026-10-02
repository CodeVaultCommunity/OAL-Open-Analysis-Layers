"""Run a complete observable flow against the local demo; no third-party packages."""
import argparse
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import uuid4


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    base = f"http://127.0.0.1:{args.port}"
    code = "DEMO-" + uuid4().hex[:12].upper()

    def request(method, path, payload=None):
        data = None if payload is None else json.dumps(payload).encode()
        headers = {} if payload is None else {"Content-Type": "application/json"}
        req = Request(base + path, data=data, headers=headers, method=method)
        try:
            response = urlopen(req, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            result = json.loads(response.read())
            print(method, path, response.status)
            print(json.dumps(result, indent=2, ensure_ascii=False))

    try:
        request("POST", "/items", {"code": code, "name": "Example notebook"})
        request("GET", "/items")
        request("POST", f"/items/{code}/deactivate")
        request("GET", f"/items/{code}")
    except (URLError, TimeoutError, OSError) as error:
        parser.exit(1, f"Cannot contact the local demo: {error}\n")


if __name__ == "__main__":
    main()
