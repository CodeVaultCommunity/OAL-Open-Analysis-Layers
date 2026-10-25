"""Select tools and inject one application-scoped instance of each case."""
from pathlib import Path
from types import SimpleNamespace

from .tools.contracts import Clock, IdentifierProvider, Store
from .tools.providers import new_identifier, utc_timestamp
from .tools.sqlite_store import SQLiteStore
from .usecases.operations import (CreateOpportunity, MoveOpportunity, RecordInteraction,
                                 ViewBoard, CloseWon, CloseLost)

class Application:
    def __init__(self, store: Store, ids: IdentifierProvider, clock: Clock):
        self.create = CreateOpportunity(store, ids, clock)
        self.move = MoveOpportunity(store, clock)
        self.note = RecordInteraction(store, ids, clock)
        self.board = ViewBoard(store)
        self.won = CloseWon(store, ids, clock)
        self.lost = CloseLost(store, ids, clock)
        self.use_cases = {case.ucs_id: case for case in
                          (self.create, self.move, self.note, self.board, self.won, self.lost)}

    def for_actor(self, actor: str):
        """Bind an authenticated actor to calls while retaining the case registry."""
        class BoundCase:
            def __init__(self, case):
                self.case = case

            def __call__(self, *args, **kwargs):
                return self.case(*args, principal=actor, **kwargs)

        return SimpleNamespace(**{
            name: BoundCase(getattr(self, name))
            for name in ("create", "move", "note", "board", "won", "lost")
        })


def build_application(path: Path) -> Application:
    return Application(SQLiteStore(path), new_identifier, utc_timestamp)
