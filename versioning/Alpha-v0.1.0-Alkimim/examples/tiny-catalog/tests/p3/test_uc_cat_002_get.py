"""Behavioral scenarios for UC-CAT-002."""
from unittest.mock import Mock
import pytest
from tiny_catalog.composition import compose
from tiny_catalog.errors import InvalidData, ItemNotFound, PersistenceUnavailable, StoreUnavailable
from tiny_catalog.tools.contracts import ItemStore


@pytest.mark.criterion("AC-CAT-002-01")
@pytest.mark.parametrize("deactivated", [False, True])
def test_lookup_retains_all_fields_independently_of_availability(application, deactivated):
    application.register.execute("A", "Name")
    if deactivated:
        application.deactivate.execute("A")
    found = application.get.execute("A")
    assert (found.code, found.name, found.active) == ("A", "Name", not deactivated)


@pytest.mark.criterion("AC-CAT-002-02")
def test_absent_valid_code_has_a_distinct_result(application):
    with pytest.raises(ItemNotFound):
        application.get.execute("MISSING")


@pytest.mark.criterion("AC-CAT-002-03")
def test_invalid_lookup_code_is_rejected(application):
    with pytest.raises(InvalidData):
        application.get.execute("not valid")


@pytest.mark.criterion("AC-CAT-002-04")
def test_unavailable_lookup_is_not_confused_with_absence():
    store = Mock(spec=ItemStore)
    store.get.side_effect = StoreUnavailable("simulated unavailable resource")
    with pytest.raises(PersistenceUnavailable):
        compose(store).for_actor("maintainer").get.execute("A")


@pytest.mark.criterion("AC-CAT-002-05")
def test_changing_returned_entity_is_not_an_implicit_persistence_operation(application):
    application.register.execute("A", "Original")
    received = application.get.execute("A")
    received.name = "Local change"
    received.active = False
    unchanged = application.get.execute("A")
    assert (unchanged.name, unchanged.active) == ("Original", True)
