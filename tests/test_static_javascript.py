from importlib.resources import files


def _javascript() -> str:
    return (
        files("sphinx_needs_datatables_config")
        .joinpath("static/datatables_config.js")
        .read_text(encoding="utf-8")
    )


def test_pdf_column_widths_are_converted_to_customize_callback() -> None:
    javascript = _javascript()

    assert 'hasOwnProperty.call(button, "columnWidths")' in javascript
    assert "delete button.columnWidths" in javascript
    assert "pdfTable.table.widths = columnWidths" in javascript


def test_nested_button_collections_are_processed() -> None:
    javascript = _javascript()

    assert "button.buttons.forEach(prepareButton)" in javascript
