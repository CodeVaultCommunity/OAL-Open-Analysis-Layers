"""HTTP Basic identity for a loopback-only demonstration."""
import base64
import binascii
import hmac
import os


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
        username, password = base64.b64decode(header[6:], validate=True).decode("utf-8").split(":", 1)
    except (ValueError, UnicodeError, binascii.Error):
        return None
    defaults = {"manager": "manager-demo", "contributor": "contributor-demo",
                "viewer": "viewer-demo"}
    expected = os.getenv(f"OAL_WORK_BOARD_{username.upper()}_PASSWORD", defaults.get(username, ""))
    if username not in defaults:
        return None
    if not hmac.compare_digest(password.encode("utf-8"), expected.encode("utf-8")):
        return None
    return username

