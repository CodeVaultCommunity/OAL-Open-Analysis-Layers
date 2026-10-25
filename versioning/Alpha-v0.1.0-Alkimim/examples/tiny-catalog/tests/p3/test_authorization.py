"""ADVS permission scenarios for all four catalog cases."""
import pytest

from tiny_catalog.composition import build_application
from tiny_catalog.errors import AccessDenied, AuthenticationRequired


@pytest.mark.criterion(
    "AC-CAT-001-06", "AC-CAT-002-06", "AC-CAT-003-04", "AC-CAT-004-06"
)
def test_missing_and_unpermitted_actors_have_no_effect(tmp_path):
    app = build_application(tmp_path / "permissions.sqlite3")
    with pytest.raises(AuthenticationRequired):
        app.register.execute("A", "Book")
    with pytest.raises(AuthenticationRequired):
        app.get.execute("A")
    with pytest.raises(AuthenticationRequired):
        app.list_available.execute()
    with pytest.raises(AuthenticationRequired):
        app.deactivate.execute("A")

    reader = app.for_actor("reader")
    with pytest.raises(AccessDenied):
        reader.register.execute("A", "Book")
    with pytest.raises(AccessDenied):
        reader.deactivate.execute("A")
    assert reader.list_available.execute() == []
    with pytest.raises(AccessDenied):
        app.for_actor("unknown").list_available.execute()


@pytest.mark.criterion("AC-CAT-002-06", "AC-CAT-003-04")
def test_reader_may_retrieve_and_list(tmp_path):
    app = build_application(tmp_path / "reader.sqlite3")
    app.for_actor("maintainer").register.execute("A", "Book")
    reader = app.for_actor("reader")
    assert reader.get.execute("A").name == "Book"
    assert [item.code for item in reader.list_available.execute()] == ["A"]

