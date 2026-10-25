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
    """Resolve HTTP Basic credentials to a demo role.

    Any invalid credential — including non-ASCII passwords — is a normal
    refusal (None), never an exception: the comparison uses UTF-8 bytes
    because hmac.compare_digest rejects non-ASCII str operands.
    """
    header = environ.get("HTTP_AUTHORIZATION", "")
    if not header.startswith("Basic "):
        return None
    try:
        decoded = base64.b64decode(header[6:], validate=True).decode("utf-8")
        username, password = decoded.split(":", 1)
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return None
    expected = PASSWORDS.get(username)
    if expected is None:
        return None
    if not hmac.compare_digest(password.encode("utf-8"), expected.encode("utf-8")):
        return None
    return username
