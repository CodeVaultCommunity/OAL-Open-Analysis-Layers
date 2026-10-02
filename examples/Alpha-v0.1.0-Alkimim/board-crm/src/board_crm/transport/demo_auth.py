"""HTTP Basic credentials for the loopback CRM demonstration."""
import base64
import binascii
import hmac
import os

PASSWORDS = {
    name: os.environ.get(f"OAL_CRM_{name.upper()}_PASSWORD", f"{name}-demo")
    for name in ("viewer", "operator", "manager")
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
