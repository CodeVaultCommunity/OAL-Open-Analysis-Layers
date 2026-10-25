"""Shared execution support for the centralized behavioral scenarios."""
import pytest
from tiny_catalog.composition import build_application, compose
from tiny_catalog.entities.item import Item
from tests.support.memory_store import MemoryItemStore


@pytest.fixture(params=["controlled", "sqlite"])
def application(request, tmp_path):
    """Both configurations execute the very same use-case implementations."""
    request.node.user_properties.append(("execution_profile", request.param))
    if request.param == "controlled":
        return compose(MemoryItemStore(Item)).for_actor("maintainer")
    return build_application(tmp_path / "behavior.sqlite3").for_actor("maintainer")
