"""Checks supporting the six ADVS behavioral-test identities."""
import sqlite3

import pytest

from work_board.composition import build_application
from work_board.errors import AccessDenied, AuthenticationRequired, Conflict, Invalid, Missing, Unavailable


@pytest.fixture
def app(tmp_path):
    return build_application(tmp_path / "work.sqlite3")


def stored(app, item_id):
    return next(item for item in app.view.execute(principal="viewer") if item.id == item_id)


def snapshot(app):
    """Observe the whole item collection and each item's comments deterministically."""
    items = sorted(app.view.execute(principal="viewer"), key=lambda item: item.id)
    return [
        (
            item.id, item.project, item.title, item.description, item.priority,
            item.status, item.assignee, item.version,
            tuple(
                (comment.id, comment.author, comment.body, comment.created_at)
                for comment in app.view_comments.execute(item.id, principal="viewer")
            ),
        )
        for item in items
    ]


def test_create_item(app):
    # AC-WB-001-01, AC-WB-001-02
    item = app.create.execute("Site", "Fix login", "Browser flow", "high", principal="contributor")
    assert item.id
    assert (item.project, item.title, item.description, item.priority, item.status,
            item.assignee, item.version) == ("Site", "Fix login", "Browser flow", "high",
                                             "backlog", None, 1)
    default = app.create.execute("Site", "Defaults", principal="manager")
    assert (default.priority, default.description) == ("normal", "")
    trimmed = app.create.execute("  Site  ", "  Trimmed  ", "  text  ", "low", principal="manager")
    assert (trimmed.project, trimmed.title, trimmed.description) == ("Site", "Trimmed", "text")
    with pytest.raises(AccessDenied):
        app.create.execute("Site", "No", principal="viewer")
    with pytest.raises(Invalid):
        app.create.execute("", "No", principal="manager")
    with pytest.raises(Invalid):
        app.create.execute("Site", "x" * 121, principal="manager")
    with pytest.raises(Invalid):
        app.create.execute("Site", "Bad priority", priority="urgent", principal="manager")
    assert len(app.view.execute(principal="viewer")) == 3


def test_assign_item(app):
    # AC-WB-002-01, AC-WB-002-02
    item = app.create.execute("Site", "Fix login", principal="manager")
    with pytest.raises(AccessDenied):
        app.assign.execute(item.id, "Ana", 1, principal="contributor")
    assigned = app.assign.execute(item.id, "Ana", 1, principal="manager")
    assert (assigned.assignee, assigned.version) == ("Ana", 2)
    with pytest.raises(Conflict):
        app.assign.execute(item.id, "Bruno", 1, principal="manager")
    current = stored(app, item.id)
    assert (current.assignee, current.version) == ("Ana", 2)


def test_transition_item(app):
    # AC-WB-003-01, AC-WB-003-02
    item = app.create.execute("Site", "Fix login", principal="manager")
    with pytest.raises(Invalid):
        app.transition.execute(item.id, "done", 1, principal="contributor")
    assert (stored(app, item.id).status, stored(app, item.id).version) == ("backlog", 1)
    progress = app.transition.execute(item.id, "in_progress", 1, principal="contributor")
    with pytest.raises(Conflict):
        app.transition.execute(item.id, "done", 1, principal="manager")
    assert (stored(app, item.id).status, stored(app, item.id).version) == ("in_progress", 2)
    done = app.transition.execute(item.id, "done", progress.version, principal="manager")
    assert done.status == "done"
    with pytest.raises(Conflict):
        app.assign.execute(item.id, "Ana", 1, principal="manager")
    assert (stored(app, item.id).assignee, stored(app, item.id).version) == (None, 3)


def test_add_comment(app):
    # AC-WB-004-01, AC-WB-004-02
    item = app.create.execute("Site", "Fix login", principal="manager")
    comment = app.comment.execute(item.id, "  Please check  ", principal="contributor")
    assert (comment.author, comment.body) == ("contributor", "Please check")
    assert comment.created_at
    assert stored(app, item.id).version == 1
    with pytest.raises(AccessDenied):
        app.comment.execute(item.id, "Not allowed", principal="viewer")
    with pytest.raises(Invalid):
        app.comment.execute(item.id, "  ", principal="manager")
    with pytest.raises(Invalid):
        app.comment.execute(item.id, "x" * 1001, principal="manager")
    with pytest.raises(Missing):
        app.comment.execute("absent", "Text", principal="manager")
    assert [item.body for item in app.view_comments.execute(item.id, principal="viewer")] == [
        "Please check"]


def test_authorization_matrix_denies_without_effects(app):
    # AC-WB-001-02, AC-WB-002-01, AC-WB-004-02
    item = app.create.execute("Site", "Fix login", principal="manager")
    before_denials = snapshot(app)
    calls = {
        "UC-WB-001": lambda actor: app.create.execute("Site", "New", principal=actor),
        "UC-WB-002": lambda actor: app.assign.execute(item.id, "Ana", 1, principal=actor),
        "UC-WB-003": lambda actor: app.transition.execute(item.id, "in_progress", 1, principal=actor),
        "UC-WB-004": lambda actor: app.comment.execute(item.id, "Text", principal=actor),
        "UC-WB-005": lambda actor: app.view.execute(principal=actor),
        "UC-WB-006": lambda actor: app.view_comments.execute(item.id, principal=actor),
    }
    known = {"manager", "contributor", "viewer"}
    permitted = {
        "UC-WB-001": {"manager", "contributor"},
        "UC-WB-002": {"manager"},
        "UC-WB-003": {"manager", "contributor"},
        "UC-WB-004": {"manager", "contributor"},
        "UC-WB-005": {"manager", "contributor", "viewer"},
        "UC-WB-006": {"manager", "contributor", "viewer"},
    }
    for case_id, call in calls.items():
        for identity, error in ((None, AuthenticationRequired), ("unknown", AccessDenied)):
            before_call = snapshot(app)
            with pytest.raises(error):
                call(identity)
            assert snapshot(app) == before_call, (
                f"{case_id} changed observable state for identity {identity!r}"
            )
        for role in sorted(known - permitted[case_id]):
            before_call = snapshot(app)
            with pytest.raises(AccessDenied):
                call(role)
            assert snapshot(app) == before_call, (
                f"{case_id} changed observable state for forbidden role {role!r}"
            )
    assert snapshot(app) == before_denials

    assert app.view.execute(principal="viewer")[0].id == item.id
    assert app.view_comments.execute(item.id, principal="viewer") == []
    created = app.create.execute("Site", "Second", principal="contributor")
    assigned = app.assign.execute(created.id, "Ana", created.version, principal="manager")
    advanced = app.transition.execute(created.id, "in_progress", assigned.version, principal="contributor")
    app.comment.execute(created.id, "Text", principal="contributor")
    assert advanced.status == "in_progress"
    assert [comment.body for comment in app.view_comments.execute(created.id, principal="viewer")] == ["Text"]


def test_view_board(app):
    # AC-WB-005-01, AC-WB-005-02
    site = app.create.execute("Site", "Fix login", principal="manager")
    app.create.execute("Mobile", "Fix view", principal="manager")
    before = [(item.id, item.version, item.status, item.assignee)
              for item in app.view.execute(principal="viewer")]
    assert [item.id for item in app.view.execute("Site", principal="viewer")] == [site.id]
    assert len(app.view.execute(principal="viewer")) == 2
    assert [item.id for item in app.view.execute(status="backlog", principal="viewer")] == [
        item.id for item in app.view.execute(principal="viewer")]
    with pytest.raises(Invalid):
        app.view.execute(status="unknown", principal="viewer")
    after = [(item.id, item.version, item.status, item.assignee)
             for item in app.view.execute(principal="viewer")]
    assert after == before


def test_view_comments(app):
    # AC-WB-006-01, AC-WB-006-02
    item = app.create.execute("Site", "Fix login", principal="manager")
    before = stored(app, item.id)
    assert app.view_comments.execute(item.id, principal="viewer") == []
    app.comment.execute(item.id, "First", principal="manager")
    assert [comment.body for comment in app.view_comments.execute(item.id, principal="viewer")] == ["First"]
    with pytest.raises(Missing):
        app.view_comments.execute("absent", principal="viewer")
    assert stored(app, item.id) == before


@pytest.mark.parametrize("version", [2**63, 10**100])
def test_large_expected_versions_preserve_contract_and_state(app, version):
    item = app.create.execute("Site", "Fix login", principal="manager")
    for case, value in ((app.assign, "Ana"), (app.transition, "in_progress")):
        with pytest.raises(Conflict):
            case.execute(item.id, value, version, principal="manager")
        with pytest.raises(Missing):
            case.execute("absent", value, version, principal="manager")
        assert stored(app, item.id) == item


def test_storage_failure_is_exposed_by_each_case_without_false_success(app):
    item = app.create.execute("Site", "Fix login", principal="manager")
    path = app.create.store.path
    with sqlite3.connect(path) as db:
        db.execute("ALTER TABLE items RENAME TO temporarily_unavailable_items")
    calls = [
        lambda: app.create.execute("Site", "Second", principal="manager"),
        lambda: app.assign.execute(item.id, "Ana", 1, principal="manager"),
        lambda: app.transition.execute(item.id, "in_progress", 1, principal="manager"),
        lambda: app.comment.execute(item.id, "Text", principal="manager"),
        lambda: app.view.execute(principal="viewer"),
        lambda: app.view_comments.execute(item.id, principal="viewer"),
    ]
    for call in calls:
        with pytest.raises(Unavailable) as failure:
            call()
        assert failure.value.write_outcome == "not_applied"
    with sqlite3.connect(path) as db:
        db.execute("ALTER TABLE temporarily_unavailable_items RENAME TO items")
    assert app.view.execute(principal="viewer") == [item]
    assert app.view_comments.execute(item.id, principal="viewer") == []
