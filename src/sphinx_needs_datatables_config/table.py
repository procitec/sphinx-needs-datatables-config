from __future__ import annotations

import re

from docutils import nodes

CONFIG_CLASS = "sphinx-needs-datatables-config"
CONFIG_CLASS_PREFIX = "sphinx-needs-datatables-config--"

_CONFIG_NAME_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def validate_config_name(config_name: str) -> str:
    """Validate a config name so it can safely be encoded as a CSS class."""
    if not _CONFIG_NAME_RE.fullmatch(config_name):
        raise ValueError(
            "DataTables config names may only contain letters, digits, '_' and '-': "
            f"{config_name!r}"
        )
    return config_name


def mark_datatable(table_node: nodes.Element, config_name: str | None) -> None:
    """Mark a Docutils table node for initialization by this extension.

    Existing ``NEEDS_DATATABLES`` is intentionally kept. If Sphinx-Needs has
    already initialized the table, the browser-side extension destroys that
    instance before applying the selected configuration.
    """
    if not config_name:
        return

    config_name = validate_config_name(config_name)
    classes = table_node.setdefault("classes", [])

    if CONFIG_CLASS not in classes:
        classes.append(CONFIG_CLASS)

    config_class = f"{CONFIG_CLASS_PREFIX}{config_name}"
    if config_class not in classes:
        classes.append(config_class)
