"""ADVS permission scenarios for all four catalog cases.

The matrix covers, for every case: a valid permitted call, an absent identity,
an unknown identity, and a known role without permission when one exists.
Denials are observed through the persisted state, not only through the raised
error.
"""
import pytest

from tiny_catalog.composition import build_application
from tiny_catalog.errors import AccessDenied, AuthenticationRequired

KNOWN = {"maintainer", "reader"}
PERMITTED = {
    "UC-CAT-001": {"maintainer"},
    "UC-CAT-002": {"maintainer", "reader"},
    "UC-CAT-003": {"maintainer", "reader"},
    "UC-CAT-004": {"maintainer"},
}


def forbidden_roles(case_id):
    return KNOWN - PERMITTED[case_id]


def invoke(app, case_id, actor):
    if case_id == "UC-CAT-001":
        return app.for_actor(actor).register.execute("A", "Book")
    if case_id == "UC-CAT-002":
        return app.for_actor(actor).get.execute("A")
    if case_id == "UC-CAT-003":
        return app.for_actor(actor).list_available.execute()
    return app.for_actor(actor).deactivate.execute("A")


def invoke_without_identity(app, case_id):
    if case_id == "UC-CAT-001":
        return app.register.execute("A", "Book")
    if case_id == "UC-CAT-002":
        return app.get.execute("A")
    if case_id == "UC-CAT-003":
        return app.list_available.execute()
    return app.deactivate.execute("A")


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
    assert app.for_actor("maintainer").list_available.execute() == []

    reader = app.for_actor("reader")
    with pytest.raises(AccessDenied):
        reader.register.execute("A", "Book")
    with pytest.raises(AccessDenied):
        reader.deactivate.execute("A")
    assert reader.list_available.execute() == []
    with pytest.raises(AccessDenied):
        app.for_actor("unknown").list_available.execute()
    assert app.for_actor("maintainer").list_available.execute() == []


@pytest.mark.criterion("AC-CAT-002-06", "AC-CAT-003-04")
def test_reader_may_retrieve_and_list(tmp_path):
    app = build_application(tmp_path / "reader.sqlite3")
    app.for_actor("maintainer").register.execute("A", "Book")
    reader = app.for_actor("reader")
    assert reader.get.execute("A").name == "Book"
    assert [item.code for item in reader.list_available.execute()] == ["A"]


@pytest.mark.criterion(
    "AC-CAT-001-06", "AC-CAT-002-06", "AC-CAT-003-04", "AC-CAT-004-06"
)
def test_authorization_matrix_per_case(tmp_path):
    app = build_application(tmp_path / "matrix.sqlite3")
    maintainer = app.for_actor("maintainer")
    maintainer.register.execute("A", "Book")

    for case_id in ("UC-CAT-001", "UC-CAT-002", "UC-CAT-003", "UC-CAT-004"):
        with pytest.raises(AuthenticationRequired):
            invoke_without_identity(app, case_id)
        with pytest.raises(AccessDenied):
            invoke(app, case_id, "unknown")
        for actor in sorted(forbidden_roles(case_id)):
            with pytest.raises(AccessDenied):
                invoke(app, case_id, actor)
        assert app.for_actor("reader").list_available.execute()[0].active is True
        assert app.for_actor("reader").get.execute("A").active is True
        assert len(app.for_actor("reader").list_available.execute()) == 1
    assert maintainer.get.execute("A").code == "A"
    assert maintainer.list_available.execute()[0].code == "A"
    deactivated = maintainer.deactivate.execute("A")
    assert deactivated.active is False
    assert maintainer.list_available.execute() == []
