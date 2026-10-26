"""Only representation assignment is tested here; no use case is executed."""
import pytest
from tiny_catalog.entities.item import Item, ItemKey
from tiny_catalog.errors import InvalidData


def test_valid_entity_fields_are_readable_and_assignable():
    item = Item("ITEM_1", "Notebook", True)
    assert (item.code, item.name, item.active) == ("ITEM_1", "Notebook", True)
    item.code = "ITEM-2"
    item.name = "New name"
    item.active = False
    assert (item.code, item.name, item.active) == ("ITEM-2", "New name", False)


@pytest.mark.parametrize("code", ["", "a", "AB C", "Á", "A" * 25, None, 1, True])
def test_invalid_code_is_rejected_on_assignment(code):
    key = ItemKey("A")
    with pytest.raises(InvalidData) as error:
        key.code = code
    assert error.value.field == "code"
    assert key.code == "A"


@pytest.mark.parametrize("name", ["", "   ", "\n\t", "x" * 81, None, 7])
def test_invalid_name_preserves_previous_value(name):
    item = Item("A", "Original", True)
    with pytest.raises(InvalidData) as error:
        item.name = name
    assert error.value.field == "name"
    assert item.name == "Original"


@pytest.mark.parametrize("flag", [0, 1, "true", None, [], 0.0])
def test_active_requires_an_actual_boolean(flag):
    item = Item("A", "Original", True)
    with pytest.raises(InvalidData):
        item.active = flag
    assert item.active is True


def test_boundary_lengths_and_unicode_names_are_supported():
    item = Item("A" * 24, "á" * 80, False)
    assert len(item.code) == 24
    assert len(item.name) == 80
