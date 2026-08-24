import pytest
from docutils import nodes

from sphinx_needs_datatables_config import (
    CONFIG_CLASS,
    CONFIG_CLASS_PREFIX,
    mark_datatable,
)


def test_mark_datatable_adds_classes() -> None:
    table = nodes.table(classes=["NEEDS_DATATABLES"])

    mark_datatable(table, "wide")

    assert "NEEDS_DATATABLES" in table["classes"]
    assert CONFIG_CLASS in table["classes"]
    assert f"{CONFIG_CLASS_PREFIX}wide" in table["classes"]


def test_mark_datatable_without_config_is_noop() -> None:
    table = nodes.table(classes=["NEEDS_DATATABLES"])

    mark_datatable(table, None)

    assert table["classes"] == ["NEEDS_DATATABLES"]


def test_mark_datatable_rejects_invalid_name() -> None:
    table = nodes.table()

    with pytest.raises(ValueError):
        mark_datatable(table, "wide report")
