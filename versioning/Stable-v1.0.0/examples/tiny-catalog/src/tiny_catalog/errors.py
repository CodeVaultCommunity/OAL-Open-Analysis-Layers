"""Stable errors shared by contracts; error definitions contain no decisions."""

class CatalogError(Exception):
    """Base for observable application outcomes."""


class AuthenticationRequired(CatalogError):
    """The caller has no authenticated identity."""


class AccessDenied(CatalogError):
    """The actor cannot execute the requested case."""


class InvalidData(CatalogError):
    """A field fails its representation constraints."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(message)


class DuplicateItem(CatalogError):
    """Registration was rejected because the code is already in use."""


class ItemNotFound(CatalogError):
    """No item exists under a valid requested code."""


class PersistenceUnavailable(CatalogError):
    """Persistence could not confirm the operation; a write outcome may be unknown."""


class StoreError(Exception):
    """Base for errors defined by the storage-tool contract."""


class StoreConflict(StoreError):
    """An atomic insertion would violate the contracted key uniqueness."""


class StoreMissing(StoreError):
    """Replacement requested a record that does not exist."""


class StoreUnavailable(StoreError):
    """The storage mechanism cannot confirm a trustworthy result."""
