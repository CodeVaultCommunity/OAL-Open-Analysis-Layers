"""Select implementations and inject tools into exactly six cases."""
from pathlib import Path

from .tools.sqlite_store import SQLiteStore
from .tools.providers import new_identifier, utc_timestamp
from .usecases.operations import (AddComment, AssignItem, CreateItem, TransitionItem,
                                  ViewBoard, ViewComments)


class Application:
    def __init__(self, store: SQLiteStore):
        self.create = CreateItem(store, new_identifier)
        self.assign = AssignItem(store)
        self.transition = TransitionItem(store)
        self.comment = AddComment(store, new_identifier, utc_timestamp)
        self.view = ViewBoard(store)
        self.view_comments = ViewComments(store)
        self.use_cases = {case.ucs_id: case for case in
                          (self.create, self.assign, self.transition, self.comment,
                           self.view, self.view_comments)}


def build_application(path: Path) -> Application:
    return Application(SQLiteStore(path))
