"""Data entities: field validity only; transitions belong to use cases."""
from dataclasses import dataclass
from .errors import Invalid

STAGES = ("NEW", "QUALIFIED", "PROPOSAL", "WON", "LOST")
ACTIVE = STAGES[:3]

def valid_text(value: str, label: str, limit: int) -> str:
    if not isinstance(value, str):
        raise Invalid(f"{label} must be text")
    result = value.strip()
    if not result or len(result) > limit:
        raise Invalid(f"{label} must contain 1–{limit} characters")
    return result


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
        valid_text(self.title, "title", 80)
        valid_text(self.company, "company", 80)
        valid_text(self.owner, "owner", 40)
        if self.stage not in STAGES or self.version < 1:
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
        valid_text(self.body, "note", 500)


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
        if not self.actor or not self.created_at or self.resulting_version < 1:
            raise Invalid("invalid event fields")
