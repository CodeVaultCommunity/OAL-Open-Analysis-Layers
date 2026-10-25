"""Data-only entities: getters, setters, and validation during assignment.

Construction only assigns fields through their setters. There is deliberately
no deactivate(), save(), authorize(), or other behavior on either entity.
"""

from tiny_catalog.errors import InvalidData


class ItemKey:
    """A catalog code represented by 1–24 ASCII uppercase letters/digits/_/- ."""

    __slots__ = ("_code",)

    def __init__(self, code: str) -> None:
        self.code = code

    @property
    def code(self) -> str:
        """Read the validated code."""
        return self._code

    @code.setter
    def code(self, value: str) -> None:
        """Validate before assignment, leaving the old value intact on failure."""
        allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
        if not isinstance(value, str) or not 1 <= len(value) <= 24:
            raise InvalidData("code", "code must contain 1 to 24 characters")
        if any(character not in allowed for character in value):
            raise InvalidData("code", "code allows only A-Z, 0-9, underscore, and hyphen")
        self._code = value


class Item(ItemKey):
    """An item record; the active flag is data, not an entity-level transition."""

    __slots__ = ("_name", "_active")

    def __init__(self, code: str, name: str, active: bool) -> None:
        super().__init__(code)
        self.name = name
        self.active = active

    @property
    def name(self) -> str:
        """Read the display name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Require 1–80 characters and at least one non-whitespace character."""
        if not isinstance(value, str) or not 1 <= len(value) <= 80 or not value.strip():
            raise InvalidData("name", "name must contain 1 to 80 characters and not be blank")
        self._name = value

    @property
    def active(self) -> bool:
        """Read the availability flag."""
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        """Accept actual booleans only; authorization and transitions live elsewhere."""
        if type(value) is not bool:
            raise InvalidData("active", "active must be a boolean")
        self._active = value
