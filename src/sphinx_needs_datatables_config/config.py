from __future__ import annotations

import json
from typing import Any


class DataTableConfigError(ValueError):
    """Raised when the Sphinx configuration cannot be exported to JavaScript."""


def validate_configs(value: object) -> dict[str, dict[str, Any]]:
    if not isinstance(value, dict):
        raise DataTableConfigError("needs_datatable_config must be a dictionary")

    result: dict[str, dict[str, Any]] = {}

    for name, config in value.items():
        if not isinstance(name, str) or not name:
            raise DataTableConfigError("DataTables config names must be non-empty strings")
        if not isinstance(config, dict):
            raise DataTableConfigError(
                f"DataTables config {name!r} must be a dictionary, got {type(config).__name__}"
            )
        result[name] = config

    try:
        json.dumps(result)
    except (TypeError, ValueError) as exc:
        raise DataTableConfigError(
            "needs_datatable_config must contain JSON-serializable values"
        ) from exc

    return result


def serialize_configs(value: object) -> str:
    """Serialize configuration safely for embedding in an inline script."""
    configs = validate_configs(value)

    # '<' is escaped so a value containing '</script>' cannot terminate the
    # surrounding inline script element.
    return json.dumps(configs, ensure_ascii=False, separators=(",", ":")).replace("<", r"\u003c")
