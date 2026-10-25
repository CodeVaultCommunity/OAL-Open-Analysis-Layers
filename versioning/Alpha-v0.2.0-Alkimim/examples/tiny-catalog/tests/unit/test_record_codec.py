"""The concrete codec has no external service and consumes no other tool."""
import pytest
from tiny_catalog.entities.item import Item
from tiny_catalog.tools.record_codec import ItemRecordCodec


@pytest.mark.parametrize("active", [True, False])
def test_codec_round_trip_is_detached(active):
    codec = ItemRecordCodec(Item)
    original = Item("A", "Pencil", active)
    record = codec.encode(original)
    assert record == ("A", "Pencil", int(active))
    restored = codec.decode(record)
    assert (restored.code, restored.name, restored.active) == ("A", "Pencil", active)
    restored.name = "Changed"
    assert original.name == "Pencil"


@pytest.mark.parametrize("record", [
    ("A", "Pencil"), ("A", "Pencil", 2), ("A", "Pencil", True),
    ("A", "Pencil", "1"), (1, "Pencil", 1), ("A", None, 1),
])
def test_corrupt_storage_representation_is_rejected(record):
    with pytest.raises(ValueError):
        ItemRecordCodec(Item).decode(record)
