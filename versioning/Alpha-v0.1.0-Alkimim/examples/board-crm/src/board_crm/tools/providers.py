"""Local implementations of the identifier and clock tool contracts."""
from datetime import datetime, timezone
from uuid import uuid4


def new_identifier() -> str:
    return str(uuid4())


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")
