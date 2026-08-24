from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx_needs.directives.needtable import NeedtableDirective

from .table import CONFIG_CLASS, CONFIG_CLASS_PREFIX, validate_config_name


def prepare_needtable_options(
    options: dict[str, Any], configs: Mapping[str, object]
) -> None:
    """Apply ``:config:`` semantics to Sphinx-Needs needtable options."""
    config_name = options.get("config")
    if not config_name:
        return

    config_name = str(config_name).strip()
    try:
        config_name = validate_config_name(config_name)
    except ValueError as exc:
        raise ValueError(str(exc)) from exc

    configured_style = str(options.get("style", "")).strip().lower()
    if configured_style and configured_style != "datatables":
        raise ValueError(":config: can only be used with the 'datatables' style.")

    if config_name not in configs:
        available = ", ".join(sorted(configs)) or "<none>"
        raise ValueError(
            f"Unknown DataTables config {config_name!r}. Available configs: {available}."
        )

    # A selected DataTables configuration implicitly enables the DataTables
    # table style, independent of the global ``needs_table_style`` value.
    options["style"] = "datatables"

    config_classes = [
        CONFIG_CLASS,
        f"{CONFIG_CLASS_PREFIX}{config_name}",
    ]
    existing_classes = str(options.get("class", "")).strip()
    options["class"] = ";".join(
        value for value in [existing_classes, *config_classes] if value
    )


class ConfigurableNeedtableDirective(NeedtableDirective):
    """Extend Sphinx-Needs' ``needtable`` directive with ``:config:``."""

    option_spec = {
        **NeedtableDirective.option_spec,
        "config": directives.unchanged_required,
    }

    def run(self) -> Sequence[nodes.Node]:
        try:
            prepare_needtable_options(
                self.options,
                self.env.config.needs_datatable_config,
            )
        except ValueError as exc:
            raise self.error(str(exc)) from exc

        return super().run()
