"""HTTP Basic credentials for a loopback-only teaching example."""
import base64
import binascii
import hmac
import os

PASSWORDS = {
    "maintainer": os.environ.get("OAL_CATALOG_MAINTAINER_PASSWORD", "maintainer-demo"),
    "reader": os.environ.get("OAL_CATALOG_READER_PASSWORD", "reader-demo"),
}


def authenticate(environ: dict) -> str | None:
    header = environ.get("HTTP_AUTHORIZATION", "")
    if not header.startswith("Basic "):
        return None
    try:
        decoded = base64.b64decode(header[6:], validate=True).decode("utf-8")
        username, password = decoded.split(":", 1)
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return None
    expected = PASSWORDS.get(username)
    if expected is None or not hmac.compare_digest(password, expected):
        return None
    return username
