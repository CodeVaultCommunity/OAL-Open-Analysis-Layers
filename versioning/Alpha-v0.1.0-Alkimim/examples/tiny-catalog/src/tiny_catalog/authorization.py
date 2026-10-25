"""Case permissions for the local example. Missing actors are denied."""
from tiny_catalog.errors import AccessDenied, AuthenticationRequired

PERMISSIONS = {
    "UC-CAT-001": frozenset({"maintainer"}),
    "UC-CAT-002": frozenset({"maintainer", "reader"}),
    "UC-CAT-003": frozenset({"maintainer", "reader"}),
    "UC-CAT-004": frozenset({"maintainer"}),
}


def require_actor(case_id: str, actor: str | None) -> None:
    if actor is None:
        raise AuthenticationRequired("an authenticated actor is required")
    if actor not in PERMISSIONS[case_id]:
        raise AccessDenied(f"{actor} cannot execute {case_id}")
