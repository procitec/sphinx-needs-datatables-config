from __future__ import annotations

from html.parser import HTMLParser
from io import StringIO
from pathlib import Path

import pytest
from sphinx.application import Sphinx

from sphinx_needs_datatables_config.needtable import prepare_needtable_options


class _TableClassParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tables: list[set[str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "table":
            return

        attributes = dict(attrs)
        self.tables.append(set((attributes.get("class") or "").split()))


def _table_classes(html: str) -> list[set[str]]:
    parser = _TableClassParser()
    parser.feed(html)
    return parser.tables


def _build_html(tmp_path: Path, index: str, config: str) -> str:
    srcdir = tmp_path / "src"
    outdir = tmp_path / "html"
    doctreedir = tmp_path / "doctrees"
    srcdir.mkdir()

    (srcdir / "conf.py").write_text(
        "\n".join(
            [
                'extensions = ["sphinx_needs", "sphinx_needs_datatables_config"]',
                'project = "test"',
                config,
            ]
        ),
        encoding="utf-8",
    )
    (srcdir / "index.rst").write_text(index, encoding="utf-8")

    app = Sphinx(
        srcdir=str(srcdir),
        confdir=str(srcdir),
        outdir=str(outdir),
        doctreedir=str(doctreedir),
        buildername="html",
        status=StringIO(),
        warning=StringIO(),
        freshenv=True,
        warningiserror=True,
    )
    app.build()

    return (outdir / "index.html").read_text(encoding="utf-8")


def test_prepare_needtable_options() -> None:
    options = {"config": "wide", "class": "custom-table"}

    prepare_needtable_options(options, {"wide": {}})

    assert options["style"] == "datatables"
    assert options["class"] == (
        "custom-table;sphinx-needs-datatables-config;sphinx-needs-datatables-config--wide"
    )


def test_prepare_needtable_options_rejects_unknown_config() -> None:
    with pytest.raises(ValueError, match="Unknown DataTables config 'missing'"):
        prepare_needtable_options({"config": "missing"}, {"wide": {}})


def test_prepare_needtable_options_rejects_non_datatables_style() -> None:
    with pytest.raises(ValueError, match="config.*datatables"):
        prepare_needtable_options(
            {"config": "wide", "style": "table"},
            {"wide": {}},
        )


def test_needtable_config_adds_classes_and_enables_datatables(tmp_path: Path) -> None:
    html = _build_html(
        tmp_path,
        """
Demo
====

.. req:: Requirement
   :id: REQ_001

.. needtable::
   :config: wide
   :class: custom-table
""",
        'needs_datatable_config = {"wide": {"pageLength": 25}}',
    )

    tables = _table_classes(html)
    assert any(
        {
            "NEEDS_DATATABLES",
            "custom-table",
            "sphinx-needs-datatables-config",
            "sphinx-needs-datatables-config--wide",
        }.issubset(classes)
        for classes in tables
    )


def test_needtable_without_config_remains_unmarked(tmp_path: Path) -> None:
    html = _build_html(
        tmp_path,
        """
Demo
====

.. req:: Requirement
   :id: REQ_001

.. needtable::
""",
        'needs_datatable_config = {"wide": {"pageLength": 25}}',
    )

    tables = _table_classes(html)
    assert tables
    assert all("sphinx-needs-datatables-config" not in classes for classes in tables)
