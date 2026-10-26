"""Behavioral scenarios for UC-CAT-004."""
from unittest.mock import Mock
import pytest
from tiny_catalog.composition import compose
from tiny_catalog.entities.item import Item
from tiny_catalog.errors import InvalidData, ItemNotFound, PersistenceUnavailable, StoreMissing, StoreUnavailable
from tiny_catalog.tools.contracts import ItemStore


@pytest.mark.criterion("AC-CAT-004-01")
def test_deactivation_changes_only_availability_and_retains_record(application):
    application.register.execute("A", "Original")
    result = application.deactivate.execute("A")
    assert (result.code, result.name, result.active) == ("A", "Original", False)
    assert application.list_available.execute() == []
    assert application.get.execute("A").name == "Original"


@pytest.mark.criterion("AC-CAT-004-02")
def test_repeated_deactivation_succeeds_without_altering_retained_data(application):
    application.register.execute("A", "Original")
    first = application.deactivate.execute("A")
    second = application.deactivate.execute("A")
    assert (first.code, first.name, first.active) == (second.code, second.name, second.active)


@pytest.mark.criterion("AC-CAT-004-03")
def test_missing_item_is_rejected(application):
    with pytest.raises(ItemNotFound):
        application.deactivate.execute("MISSING")


@pytest.mark.criterion("AC-CAT-004-04")
def test_invalid_code_is_rejected(application):
    with pytest.raises(InvalidData):
        application.deactivate.execute("bad")


@pytest.mark.criterion("AC-CAT-004-05")
@pytest.mark.parametrize("stage", ["lookup", "write"])
def test_unavailable_dependency_prevents_false_confirmation(stage):
    store = Mock(spec=ItemStore)
    store.get.return_value = Item("A", "Name", True)
    if stage == "lookup":
        store.get.side_effect = StoreUnavailable("lookup failed")
    else:
        store.replace.side_effect = StoreUnavailable("write outcome unknown")
    with pytest.raises(PersistenceUnavailable):
        compose(store).for_actor("maintainer").deactivate.execute("A")


@pytest.mark.criterion("AC-CAT-004-03")
def test_disappeared_record_is_not_recreated():
    # Defensive contract outcome; deletion is not a public use case in this scope.
    store = Mock(spec=ItemStore)
    store.get.return_value = Item("A", "Name", True)
    store.replace.side_effect = StoreMissing("record disappeared")
    with pytest.raises(ItemNotFound):
        compose(store).for_actor("maintainer").deactivate.execute("A")
