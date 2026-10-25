"""Case permissions; every unlisted actor is denied."""
from .errors import AccessDenied, AuthenticationRequired

PERMISSIONS = {
    "UC-CRM-001": frozenset({"operator", "manager"}),
    "UC-CRM-002": frozenset({"operator", "manager"}),
    "UC-CRM-003": frozenset({"operator", "manager"}),
    "UC-CRM-004": frozenset({"viewer", "operator", "manager"}),
    "UC-CRM-005": frozenset({"manager"}),
    "UC-CRM-006": frozenset({"manager"}),
}


def require_actor(case_id: str, actor: str | None) -> None:
    if actor is None:
        raise AuthenticationRequired("an authenticated actor is required")
    if actor not in PERMISSIONS[case_id]:
        raise AccessDenied(f"{actor} cannot execute {case_id}")
