"""Behavioral scenarios for UC-CAT-001, including controlled failures."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import Mock
import pytest

from tiny_catalog.composition import build_application, compose
from tiny_catalog.errors import DuplicateItem, InvalidData, PersistenceUnavailable, StoreUnavailable
from tiny_catalog.tools.contracts import ItemStore


@pytest.mark.criterion("AC-CAT-001-01")
def test_valid_registration_is_active_and_retrievable(application):
    created = application.register.execute("BOOK-1", "Notebook")
    assert (created.code, created.name, created.active) == ("BOOK-1", "Notebook", True)
    assert application.get.execute("BOOK-1").active is True


@pytest.mark.criterion("AC-CAT-001-02")
@pytest.mark.parametrize("code,name", [("bad", "Valid"), ("A", ""), ("A", " " * 3), (None, "Valid")])
def test_invalid_registration_has_no_record_effect(application, code, name):
    with pytest.raises(InvalidData):
        application.register.execute(code, name)
    assert application.list_available.execute() == []


@pytest.mark.criterion("AC-CAT-001-03")
@pytest.mark.parametrize("deactivated", [False, True])
def test_allocated_code_is_not_reused_even_for_inactive_item(application, deactivated):
    application.register.execute("A", "Original")
    if deactivated:
        application.deactivate.execute("A")
    with pytest.raises(DuplicateItem):
        application.register.execute("A", "Replacement")
    existing = application.get.execute("A")
    assert existing.name == "Original"
    assert existing.active is (not deactivated)


@pytest.mark.criterion("AC-CAT-001-04")
def test_concurrent_registration_has_exactly_one_success(tmp_path):
    application = build_application(tmp_path / "race.sqlite3").for_actor("maintainer")
    barrier = Barrier(2)

    def register(name):
        barrier.wait(timeout=5)
        try:
            application.register.execute("A", name)
            return "registered"
        except DuplicateItem:
            return "duplicate"

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(register, ("One", "Two"))) == ["duplicate", "registered"]
    assert len(application.list_available.execute()) == 1


@pytest.mark.criterion("AC-CAT-001-05")
def test_unavailable_registration_is_not_reported_as_success():
    store = Mock(spec=ItemStore)
    store.insert.side_effect = StoreUnavailable("simulated unavailable resource")
    application = compose(store).for_actor("maintainer")
    with pytest.raises(PersistenceUnavailable):
        application.register.execute("A", "Valid")
    # We intentionally make no assertion that the failed write had no effect.
