"""Shared supporting check for retrieval, listing, and deactivation."""
import pytest
from tiny_catalog.composition import build_application


@pytest.mark.criterion("AC-SHARED-01", "AC-CAT-004-01", "AC-CAT-002-01")
def test_confirmed_deactivation_survives_application_reconstruction(tmp_path):
    path = tmp_path / "retained.sqlite3"
    first_application = build_application(path).for_actor("maintainer")
    first_application.register.execute("A", "Retained name")
    first_application.deactivate.execute("A")
    del first_application
    second_application = build_application(path).for_actor("maintainer")
    retained = second_application.get.execute("A")
    assert (retained.code, retained.name, retained.active) == ("A", "Retained name", False)
    assert second_application.list_available.execute() == []
