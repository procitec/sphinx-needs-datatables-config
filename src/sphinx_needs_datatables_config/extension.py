from __future__ import annotations

from importlib.metadata import version
from importlib.resources import files
from typing import Any

from docutils import nodes
from sphinx.application import Sphinx

from .config import serialize_configs
from .needtable import ConfigurableNeedtableDirective
from .table import CONFIG_CLASS


def _install_javascript(app: Sphinx) -> None:
    if app.builder.format != "html":
        return

    serialized = serialize_configs(app.config.needs_datatable_config)
    config_script = f"window.SPHINX_NEEDS_DATATABLE_CONFIG = {serialized};"

    javascript = (
        files("sphinx_needs_datatables_config")
        .joinpath("static/datatables_config.js")
        .read_text(encoding="utf-8")
    )

    # Sphinx-Needs provides DataTables and its default loader. Our JavaScript
    # runs afterwards, but configured tables are removed from the default
    # Sphinx-Needs selector during ``doctree-resolved`` below.
    app.add_js_file(None, priority=890, body=config_script)
    app.add_js_file(None, priority=900, body=javascript)


def _prepare_configured_tables(
    app: Sphinx,
    doctree: nodes.document,
    docname: str,
) -> None:
    """Keep configured tables out of the Sphinx-Needs default DataTables loader."""
    if app.builder.format != "html":
        return

    for table in doctree.findall(nodes.table):
        classes = table.get("classes", [])
        if CONFIG_CLASS in classes and "NEEDS_DATATABLES" in classes:
            classes.remove("NEEDS_DATATABLES")


def setup(app: Sphinx) -> dict[str, Any]:
    # The extension intentionally relies on the DataTables bundle delivered by
    # Sphinx-Needs instead of shipping a second copy.
    app.setup_extension("sphinx_needs")

    app.add_directive("needtable", ConfigurableNeedtableDirective, override=True)

    app.add_config_value(
        "needs_datatable_config",
        {},
        "html",
        types=[dict],
        description="Named DataTables configuration objects.",
    )
    app.connect("builder-inited", _install_javascript)
    # Sphinx-Needs turns Needtable nodes into normal table nodes during
    # ``doctree-resolved``. Run afterwards and remove its loader marker only
    # from tables that are explicitly managed by this extension.
    app.connect("doctree-resolved", _prepare_configured_tables, priority=900)

    return {
        "version": version("sphinx-needs-datatables-config"),
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
