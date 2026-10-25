"""Record the responsibility exercised by each example check."""
from pathlib import Path
import pytest


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Classify checks by subject rather than by test double or storage choice."""
    root = Path(__file__).parent
    groups = {"unit": "unit", "integration": "integration", "p3": "behavior", "p4": "interaction"}
    for item in items:
        group = Path(str(item.path)).relative_to(root).parts[0]
        expected = groups[group]
        item.add_marker(getattr(pytest.mark, expected))
        criteria = sorted({str(value) for mark in item.iter_markers("criterion") for value in mark.args})
        item.user_properties.append(("oal_category", expected))
        if expected == "behavior" and not criteria:
            raise pytest.UsageError(f"P3 case check lacks UCS criterion references: {item.nodeid}")
        if criteria:
            item.user_properties.append(("ucs_criteria", ",".join(criteria)))
