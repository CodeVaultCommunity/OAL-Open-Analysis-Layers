"""Behavioral scenarios for UC-CAT-003."""
from unittest.mock import Mock
import pytest
from tiny_catalog.composition import compose
from tiny_catalog.errors import PersistenceUnavailable, StoreUnavailable
from tiny_catalog.tools.contracts import ItemStore


@pytest.mark.criterion("AC-CAT-003-01")
def test_only_available_items_are_returned_in_code_order(application):
    for code in ["C", "A", "B"]:
        application.register.execute(code, f"Item {code}")
    application.deactivate.execute("B")
    assert [item.code for item in application.list_available.execute()] == ["A", "C"]


@pytest.mark.criterion("AC-CAT-003-02")
def test_empty_or_fully_inactive_catalog_returns_an_empty_collection(application):
    assert application.list_available.execute() == []
    application.register.execute("A", "Name")
    application.deactivate.execute("A")
    assert application.list_available.execute() == []


@pytest.mark.criterion("AC-CAT-003-03")
def test_unavailable_listing_is_not_confused_with_an_empty_catalog():
    store = Mock(spec=ItemStore)
    store.list_all.side_effect = StoreUnavailable("simulated unavailable resource")
    with pytest.raises(PersistenceUnavailable):
        compose(store).for_actor("maintainer").list_available.execute()
