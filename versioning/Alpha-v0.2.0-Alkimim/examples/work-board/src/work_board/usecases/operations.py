"""Work-item decisions and permissions live here, outside the HTTP adapter."""
from collections.abc import Callable

from ..authorization import require_actor
from ..entities import (
    ASSIGNEE_LIMIT, COMMENT_LIMIT, DEFAULT_PRIORITY, DESCRIPTION_LIMIT, PRIORITIES,
    PROJECT_LIMIT, STATUSES, TITLE_LIMIT, Comment, WorkItem, required_text,
)
from ..errors import Conflict, Invalid
from ..tools.contracts import WorkStore


class CreateItem:
    ucs_id = "UC-WB-001"

    def __init__(self, store: WorkStore, make_id: Callable[[], str]):
        self.store, self.make_id = store, make_id

    def execute(self, project: str, title: str, description: str = "",
                priority: str = DEFAULT_PRIORITY, *, principal: str | None = None) -> WorkItem:
        require_actor(self.ucs_id, principal)
        project = required_text(project, "project", PROJECT_LIMIT)
        title = required_text(title, "title", TITLE_LIMIT)
        if not isinstance(description, str):
            raise Invalid(f"description must be text of at most {DESCRIPTION_LIMIT} characters")
        description = description.strip()
        if len(description) > DESCRIPTION_LIMIT:
            raise Invalid(f"description must be text of at most {DESCRIPTION_LIMIT} characters")
        if priority not in PRIORITIES:
            raise Invalid("unknown priority")
        item = WorkItem(self.make_id(), project, title, description, priority,
                        "backlog", None, 1)
        return self.store.create(item)


class AssignItem:
    ucs_id = "UC-WB-002"

    def __init__(self, store: WorkStore):
        self.store = store

    def execute(self, item_id: str, assignee: str, expected_version: int,
                *, principal: str | None = None) -> WorkItem:
        require_actor(self.ucs_id, principal)
        assignee = required_text(assignee, "assignee", ASSIGNEE_LIMIT)
        if type(expected_version) is not int or expected_version < 1:
            raise Invalid("expected_version must be a positive integer")
        return self.store.assign(item_id, assignee, expected_version)


class TransitionItem:
    ucs_id = "UC-WB-003"
    next_status = {"backlog": "in_progress", "in_progress": "done"}

    def __init__(self, store: WorkStore):
        self.store = store

    def execute(self, item_id: str, target_status: str, expected_version: int,
                *, principal: str | None = None) -> WorkItem:
        require_actor(self.ucs_id, principal)
        if type(expected_version) is not int or expected_version < 1:
            raise Invalid("expected_version must be a positive integer")
        if target_status not in STATUSES:
            raise Invalid("unknown status")
        current = self.store.get(item_id)
        if current.version != expected_version:
            raise Conflict("work item changed; reload before retrying")
        if self.next_status.get(current.status) != target_status:
            raise Invalid("only the next workflow state is allowed")
        return self.store.transition(item_id, target_status, expected_version)


class AddComment:
    ucs_id = "UC-WB-004"

    def __init__(self, store: WorkStore, make_id: Callable[[], str],
                 now: Callable[[], str]):
        self.store, self.make_id, self.now = store, make_id, now

    def execute(self, item_id: str, body: str, *, principal: str | None = None) -> Comment:
        author = require_actor(self.ucs_id, principal)
        body = required_text(body, "body", COMMENT_LIMIT)
        self.store.get(item_id)
        return self.store.add_comment(Comment(self.make_id(), item_id, author, body, self.now()))


class ViewBoard:
    ucs_id = "UC-WB-005"

    def __init__(self, store: WorkStore):
        self.store = store

    def execute(self, project: str | None = None, status: str | None = None,
                *, principal: str | None = None) -> list[WorkItem]:
        require_actor(self.ucs_id, principal)
        if project is not None:
            project = required_text(project, "project", PROJECT_LIMIT)
        if status is not None and status not in STATUSES:
            raise Invalid("unknown status")
        return self.store.list_items(project, status)


class ViewComments:
    ucs_id = "UC-WB-006"

    def __init__(self, store: WorkStore):
        self.store = store

    def execute(self, item_id: str, *, principal: str | None = None) -> list[Comment]:
        require_actor(self.ucs_id, principal)
        return self.store.comments(item_id)
