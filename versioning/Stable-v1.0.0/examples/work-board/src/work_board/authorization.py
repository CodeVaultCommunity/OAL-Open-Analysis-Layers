"""Case permissions, independent of HTTP authentication."""
from .errors import AccessDenied, AuthenticationRequired


ALLOWED = {
    "UC-WB-001": {"manager", "contributor"},
    "UC-WB-002": {"manager"},
    "UC-WB-003": {"manager", "contributor"},
    "UC-WB-004": {"manager", "contributor"},
    "UC-WB-005": {"manager", "contributor", "viewer"},
    "UC-WB-006": {"manager", "contributor", "viewer"},
}


def require_actor(case_id: str, actor: str | None) -> str:
    if actor is None:
        raise AuthenticationRequired("an actor is required")
    if actor not in ALLOWED[case_id]:
        raise AccessDenied(f"{actor} cannot execute {case_id}")
    return actor
