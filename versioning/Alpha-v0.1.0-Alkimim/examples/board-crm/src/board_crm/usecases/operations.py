"""Six specified cases; all stage and board policy is decided here."""
from dataclasses import asdict
from ..entities import ACTIVE, STAGES, Opportunity, valid_text
from ..errors import Conflict, Invalid
from ..tools.contracts import Clock, IdentifierProvider, Store
from ..authorization import require_actor

def expect_version(card: Opportunity, expected: int) -> None:
    if not isinstance(expected, int) or isinstance(expected, bool) or expected < 1:
        raise Invalid("expected_version must be a positive integer")
    if card.version != expected:
        raise Conflict("card changed; refresh the board")


class CreateOpportunity:
    ucs_id = "UC-CRM-001"

    def __init__(self, store: Store, ids: IdentifierProvider, clock: Clock):
        self.store, self.ids, self.clock = store, ids, clock

    def __call__(self, title: str, company: str, owner: str, *, principal: str | None = None) -> Opportunity:
        require_actor(self.ucs_id, principal)
        title, company, owner = (valid_text(title, "title", 80),
                                 valid_text(company, "company", 80),
                                 valid_text(owner, "owner", 40))
        timestamp = self.clock()
        card = Opportunity(self.ids(), title, company, owner, "NEW", 1, timestamp, timestamp)
        self.store.create(card, owner)
        return card


class MoveOpportunity:
    ucs_id = "UC-CRM-002"

    def __init__(self, store: Store, clock: Clock):
        self.store, self.clock = store, clock

    def __call__(self, card_id: str, destination: str, expected_version: int, actor: str, *, principal: str | None = None) -> Opportunity:
        require_actor(self.ucs_id, principal)
        card = self.store.get(card_id)
        expect_version(card, expected_version)
        if destination not in ACTIVE or card.stage not in ACTIVE:
            raise Invalid("only active cards can move between active stages")
        if abs(ACTIVE.index(destination) - ACTIVE.index(card.stage)) != 1:
            raise Invalid("move to an adjacent active stage")
        return self.store.mutate(card_id, expected_version, self.clock(), actor, stage=destination)


class RecordInteraction:
    ucs_id = "UC-CRM-003"

    def __init__(self, store: Store, ids: IdentifierProvider, clock: Clock):
        self.store, self.ids, self.clock = store, ids, clock

    def __call__(self, card_id: str, body: str, expected_version: int, actor: str, *, principal: str | None = None) -> dict:
        require_actor(self.ucs_id, principal)
        body = valid_text(body, "note", 500)
        card = self.store.get(card_id)
        expect_version(card, expected_version)
        note_id = self.ids()
        updated = self.store.mutate(card_id, expected_version, self.clock(), actor,
                                    note_id=note_id, note_body=body)
        return {"note_id": note_id, "version": updated.version}


class ViewBoard:
    ucs_id = "UC-CRM-004"

    def __init__(self, store: Store):
        self.store = store

    def __call__(self, owner: str | None = None, *, principal: str | None = None) -> dict[str, list[dict]]:
        require_actor(self.ucs_id, principal)
        if owner is not None and not isinstance(owner, str):
            raise Invalid("owner filter must be text")
        records = self.store.list_records()
        ordered = sorted(records, key=lambda record: record[0].id)
        ordered.sort(key=lambda record: record[0].updated_at, reverse=True)
        board: dict[str, list[dict]] = {stage: [] for stage in STAGES}
        for card, notes, events in ordered:
            if owner is not None and card.owner != owner:
                continue
            board[card.stage].append({**asdict(card), "notes": [asdict(note) for note in notes],
                                      "history": [asdict(event) for event in events]})
        return board


class CloseWon:
    ucs_id = "UC-CRM-005"

    def __init__(self, store: Store, ids: IdentifierProvider, clock: Clock):
        self.store, self.ids, self.clock = store, ids, clock

    def __call__(self, card_id: str, reason: str, expected_version: int, actor: str, *, principal: str | None = None) -> Opportunity:
        require_actor(self.ucs_id, principal)
        reason = valid_text(reason, "reason", 200)
        card = self.store.get(card_id)
        expect_version(card, expected_version)
        if card.stage != "PROPOSAL":
            raise Invalid("only a Proposal card can close as Won")
        return self.store.mutate(card_id, expected_version, self.clock(), actor, stage="WON",
                                 note_id=self.ids(), note_body=reason)


class CloseLost:
    ucs_id = "UC-CRM-006"

    def __init__(self, store: Store, ids: IdentifierProvider, clock: Clock):
        self.store, self.ids, self.clock = store, ids, clock

    def __call__(self, card_id: str, reason: str, expected_version: int, actor: str, *, principal: str | None = None) -> Opportunity:
        require_actor(self.ucs_id, principal)
        reason = valid_text(reason, "reason", 200)
        card = self.store.get(card_id)
        expect_version(card, expected_version)
        if card.stage not in ACTIVE:
            raise Invalid("only an active card can close as Lost")
        return self.store.mutate(card_id, expected_version, self.clock(), actor, stage="LOST",
                                 note_id=self.ids(), note_body=reason)


