import pytest

from sphinx_needs_datatables_config.config import (
    DataTableConfigError,
    serialize_configs,
    validate_configs,
)


def test_validate_configs() -> None:
    configs = {
        "wide": {
            "scrollX": True,
            "pageLength": 50,
        }
    }

    assert validate_configs(configs) == configs


def test_validate_configs_rejects_non_dict_config() -> None:
    with pytest.raises(DataTableConfigError):
        validate_configs({"wide": "invalid"})


def test_serialize_escapes_script_end() -> None:
    serialized = serialize_configs({"x": {"text": "</script>"}})

    assert "</script>" not in serialized
    assert r"\u003c/script>" in serialized
