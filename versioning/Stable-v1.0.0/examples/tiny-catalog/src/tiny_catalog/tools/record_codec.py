"""A concrete tool with no service access and no consumption of other tools."""
from collections.abc import Callable

from tiny_catalog.entities.item import Item


class ItemRecordCodec:
    """Representation conversion only; does not choose catalog behavior."""

    def __init__(self, item_factory: Callable[[str, str, bool], Item]) -> None:
        self._item_factory = item_factory

    def encode(self, item: Item) -> tuple[str, str, int]:
        """Serialize the field representation without mutating the entity."""
        return item.code, item.name, int(item.active)

    def decode(self, record: tuple[object, ...]) -> Item:
        """Validate representation, rejecting corrupt flags rather than coercing them."""
        if len(record) != 3:
            raise ValueError("an item record must have three fields")
        code, name, flag = record
        if not isinstance(code, str) or not isinstance(name, str):
            raise ValueError("stored code and name must be text")
        if type(flag) is not int or flag not in (0, 1):
            raise ValueError("stored active flag must be integer 0 or 1")
        return self._item_factory(code, name, flag == 1)
