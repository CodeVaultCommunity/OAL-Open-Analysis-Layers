"""Data entities: field validity only; transitions belong to use cases."""
from dataclasses import dataclass
from .errors import Invalid

STAGES = ("NEW", "QUALIFIED", "PROPOSAL", "WON", "LOST")
ACTIVE = STAGES[:3]
TITLE_LIMIT = 80
COMPANY_LIMIT = 80
OWNER_LIMIT = 40
NOTE_LIMIT = 500
REASON_LIMIT = 200
ACTOR_LIMIT = 40


def valid_text(value: str, label: str, limit: int) -> str:
    """Return normalized text, or reject a non-text, empty, or overlong value."""
    if not isinstance(value, str):
        raise Invalid(f"{label} must be text")
    result = value.strip()
    if not result or len(result) > limit:
        raise Invalid(f"{label} must contain 1–{limit} characters")
    return result


def positive_int(value: object) -> bool:
    """Accept an int of at least 1; booleans and other numerics are not versions."""
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


@dataclass(frozen=True)
class Opportunity:
    id: str
    title: str
    company: str
    owner: str
    stage: str
    version: int
    created_at: str
    updated_at: str

    def __post_init__(self) -> None:
        if not self.id or not self.created_at or not self.updated_at:
            raise Invalid("invalid opportunity identity or timestamp")
        object.__setattr__(self, "title", valid_text(self.title, "title", TITLE_LIMIT))
        object.__setattr__(self, "company", valid_text(self.company, "company", COMPANY_LIMIT))
        object.__setattr__(self, "owner", valid_text(self.owner, "owner", OWNER_LIMIT))
        if self.stage not in STAGES or not positive_int(self.version):
            raise Invalid("invalid stage or version")


@dataclass(frozen=True)
class InteractionNote:
    id: str
    opportunity_id: str
    body: str
    created_at: str

    def __post_init__(self) -> None:
        if not self.id or not self.opportunity_id or not self.created_at:
            raise Invalid("invalid note identity or timestamp")
        object.__setattr__(self, "body", valid_text(self.body, "note", NOTE_LIMIT))


@dataclass(frozen=True)
class StageEvent:
    source_stage: str | None
    destination_stage: str
    actor: str
    created_at: str
    resulting_version: int

    def __post_init__(self) -> None:
        if self.source_stage is not None and self.source_stage not in STAGES:
            raise Invalid("invalid source stage")
        if self.destination_stage not in STAGES or self.source_stage == self.destination_stage:
            raise Invalid("invalid destination stage")
        if not self.created_at or not positive_int(self.resulting_version):
            raise Invalid("invalid event fields")
        object.__setattr__(self, "actor", valid_text(self.actor, "actor", ACTOR_LIMIT))
