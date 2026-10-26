"""Concrete identifier and clock providers selected by composition."""
from datetime import datetime, timezone
from uuid import uuid4


def new_identifier() -> str:
    return uuid4().hex[:12]


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
