from __future__ import annotations

from importlib.metadata import version
from importlib.resources import files
from typing import Any

from sphinx.application import Sphinx

from .config import serialize_configs
from .needtable import ConfigurableNeedtableDirective


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

    # Sphinx-Needs installs its DataTables assets with the normal extension
    # priority. We deliberately run afterwards.
    app.add_js_file(None, priority=890, body=config_script)
    app.add_js_file(None, priority=900, body=javascript)


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

    return {
        "version": version("sphinx-needs-datatables-config"),
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
