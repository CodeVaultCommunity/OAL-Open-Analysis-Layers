"""Storage contract checks for the work store; no use case under test."""
import sqlite3

import pytest

from work_board.entities import Comment, WorkItem
from work_board.errors import Conflict, Missing, Unavailable
from work_board.tools.sqlite_store import SQLiteStore


@pytest.fixture
def store(tmp_path):
    return SQLiteStore(tmp_path / "work.sqlite3")


def make_item(store, item_id="i1"):
    return store.create(WorkItem(item_id, "Site", "Fix", "", "normal", "backlog", None, 1))


def test_versioned_update_is_atomic_and_preserves_state_on_conflict(store):
    make_item(store)
    updated = store.assign("i1", "Ana", 1)
    assert (updated.assignee, updated.version) == ("Ana", 2)
    with pytest.raises(Conflict):
        store.assign("i1", "Bruno", 1)
    current = store.get("i1")
    assert (current.assignee, current.version) == ("Ana", 2)


def test_absent_item_is_missing(store):
    with pytest.raises(Missing):
        store.get("absent")
    with pytest.raises(Missing):
        store.add_comment(Comment("c1", "absent", "manager", "Text", "2026-01-01T00:00:00+00:00"))


def test_duplicate_comment_id_is_a_conflict_and_rolls_back(store):
    make_item(store)
    store.add_comment(Comment("c1", "i1", "manager", "First", "2026-01-01T00:00:00+00:00"))
    with pytest.raises(Conflict):
        store.add_comment(Comment("c1", "i1", "manager", "Again", "2026-01-01T00:00:01+00:00"))
    assert [comment.body for comment in store.comments("i1")] == ["First"]


def test_comments_are_returned_in_chronological_order(store):
    make_item(store)
    store.add_comment(Comment("c2", "i1", "manager", "Second", "2026-01-01T00:00:02+00:00"))
    store.add_comment(Comment("c1", "i1", "manager", "First", "2026-01-01T00:00:01+00:00"))
    assert [comment.body for comment in store.comments("i1")] == ["First", "Second"]


@pytest.mark.parametrize("version", [2**63 - 1, 2**63, 10**100])
@pytest.mark.parametrize("operation,value", [("assign", "Ana"), ("transition", "in_progress")])
def test_large_expected_version_is_conflict_or_missing_without_effects(store, version, operation, value):
    before = make_item(store)
    update = getattr(store, operation)
    with pytest.raises(Conflict):
        update("i1", value, version)
    with pytest.raises(Missing):
        update("absent", value, version)
    assert store.get("i1") == before


def test_exhausted_storage_counter_is_unavailable_without_numeric_promotion(store):
    before = store.create(WorkItem("i1", "Site", "Fix", "", "normal", "backlog", None, 2**63 - 1))
    with pytest.raises(Unavailable) as failure:
        store.assign("i1", "Ana", before.version)
    assert failure.value.write_outcome == "not_applied"
    assert store.get("i1") == before
    with sqlite3.connect(store.path) as db:
        assert db.execute("SELECT typeof(version) FROM items WHERE id='i1'").fetchone()[0] == "integer"


def test_connection_failure_has_stable_unavailable_result(store, monkeypatch):
    def cannot_connect(*args, **kwargs):
        raise sqlite3.OperationalError("injected connection failure")
    monkeypatch.setattr(sqlite3, "connect", cannot_connect)
    with pytest.raises(Unavailable) as failure:
        store.get("i1")
    assert failure.value.write_outcome == "not_applied"
    assert isinstance(failure.value.__cause__, sqlite3.OperationalError)


def test_statement_failure_rolls_back_the_update(store):
    before = make_item(store)
    with sqlite3.connect(store.path) as db:
        db.execute("CREATE TRIGGER fail_update AFTER UPDATE ON items "
                   "BEGIN SELECT missing_storage_function(); END")
    with pytest.raises(Unavailable) as failure:
        store.assign("i1", "Ana", before.version)
    assert failure.value.write_outcome == "not_applied"
    assert store.get("i1") == before


@pytest.mark.parametrize("commit_applied", [False, True])
def test_unconfirmed_commit_is_unknown_even_when_rollback_returns(store, monkeypatch, commit_applied):
    before = make_item(store)
    connect = sqlite3.connect

    class FailingCommit(sqlite3.Connection):
        def commit(self):
            if commit_applied:
                super().commit()
            raise sqlite3.OperationalError("injected commit acknowledgement failure")

    def connection(*args, **kwargs):
        return connect(*args, **kwargs, factory=FailingCommit)

    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", connection)
        with pytest.raises(Unavailable) as failure:
            store.assign("i1", "Ana", before.version)
        assert failure.value.write_outcome == "unknown"
    observed = store.get("i1")
    if commit_applied:
        assert (observed.assignee, observed.version) == ("Ana", before.version + 1)
    else:
        assert observed == before
