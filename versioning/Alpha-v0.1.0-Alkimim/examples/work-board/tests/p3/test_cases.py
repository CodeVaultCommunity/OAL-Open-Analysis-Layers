"""Checks supporting the six ADVS behavioral-test identities."""
import pytest

from work_board.composition import build_application
from work_board.errors import AccessDenied, Conflict, Invalid, Missing


@pytest.fixture
def app(tmp_path):
    return build_application(tmp_path / "work.sqlite3")


def test_create_item(app):
    # AC-WB-001-01, AC-WB-001-02
    item = app.create.execute("Site", "Fix login", "Browser flow", "high", principal="contributor")
    assert (item.project, item.status, item.version) == ("Site", "backlog", 1)
    with pytest.raises(AccessDenied):
        app.create.execute("Site", "No", principal="viewer")
    with pytest.raises(Invalid):
        app.create.execute("", "No", principal="manager")


def test_assign_item(app):
    # AC-WB-002-01, AC-WB-002-02
    item = app.create.execute("Site", "Fix login", principal="manager")
    with pytest.raises(AccessDenied):
        app.assign.execute(item.id, "Ana", 1, principal="contributor")
    assigned = app.assign.execute(item.id, "Ana", 1, principal="manager")
    assert (assigned.assignee, assigned.version) == ("Ana", 2)
    with pytest.raises(Conflict):
        app.assign.execute(item.id, "Bruno", 1, principal="manager")


def test_transition_item(app):
    # AC-WB-003-01, AC-WB-003-02
    item = app.create.execute("Site", "Fix login", principal="manager")
    with pytest.raises(Invalid):
        app.transition.execute(item.id, "done", 1, principal="contributor")
    progress = app.transition.execute(item.id, "in_progress", 1, principal="contributor")
    with pytest.raises(Conflict):
        app.transition.execute(item.id, "done", 1, principal="manager")
    done = app.transition.execute(item.id, "done", progress.version, principal="manager")
    assert done.status == "done"
    with pytest.raises(Conflict):
        app.assign.execute(item.id, "Ana", 1, principal="manager")


def test_add_comment(app):
    # AC-WB-004-01, AC-WB-004-02
    item = app.create.execute("Site", "Fix login", principal="manager")
    comment = app.comment.execute(item.id, "Please check", principal="contributor")
    assert (comment.author, comment.body) == ("contributor", "Please check")
    with pytest.raises(AccessDenied):
        app.comment.execute(item.id, "Not allowed", principal="viewer")
    with pytest.raises(Invalid):
        app.comment.execute(item.id, "  ", principal="manager")
    with pytest.raises(Missing):
        app.comment.execute("absent", "Text", principal="manager")


def test_view_board(app):
    # AC-WB-005-01, AC-WB-005-02
    site = app.create.execute("Site", "Fix login", principal="manager")
    app.create.execute("Mobile", "Fix view", principal="manager")
    assert [item.id for item in app.view.execute("Site", principal="viewer")] == [site.id]
    assert len(app.view.execute(principal="viewer")) == 2
    assert [item.id for item in app.view.execute(status="backlog", principal="viewer")] == [
        item.id for item in app.view.execute(principal="viewer")]
    with pytest.raises(Invalid):
        app.view.execute(status="unknown", principal="viewer")


def test_view_comments(app):
    # AC-WB-006-01, AC-WB-006-02
    item = app.create.execute("Site", "Fix login", principal="manager")
    assert app.view_comments.execute(item.id, principal="viewer") == []
    app.comment.execute(item.id, "First", principal="manager")
    assert [comment.body for comment in app.view_comments.execute(item.id, principal="viewer")] == ["First"]
    with pytest.raises(Missing):
        app.view_comments.execute("absent", principal="viewer")
