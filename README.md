# sphinx-needs-datatables-config

Small Sphinx extension that implements the basic idea proposed in
[Sphinx-Needs issue #408](https://github.com/useblocks/sphinx-needs/issues/408):
named DataTables configurations that can be selected per table.

The extension is intentionally small and isolated so it can be removed once
equivalent functionality is available directly in Sphinx-Needs.

## Installation

```bash
uv add sphinx-needs-datatables-config
```

## Activate the extension

```python
extensions = [
    "sphinx_needs",
    "sphinx_needs_datatables_config",
]
```

The extension also calls `app.setup_extension("sphinx_needs")`, so explicitly
listing `sphinx_needs` first is recommended for clarity but not technically
required.

## Configure DataTables

The configuration deliberately follows the name proposed by Sphinx-Needs
issue #408:

```python
needs_datatable_config = {
    "requirements": {
        "dom": "lBfrtip",
        "colReorder": True,
        "scrollX": True,
        "autoWidth": False,
        "responsive": False,
        "pageLength": 50,
        "buttons": [
            {
                "extend": "colvis",
                "text": "Columns",
            },
            "copy",
            "excel",
            {
                "extend": "collection",
                "text": "PDF",
                "buttons": [
                    {
                        "extend": "pdfHtml5",
                        "text": "Portrait",
                        "orientation": "portrait",
                        "pageSize": "A4",
                    },
                    {
                        "extend": "pdfHtml5",
                        "text": "Landscape",
                        "orientation": "landscape",
                        "pageSize": "A4",
                    },
                ],
            },
        ],
    },
}
```

Configuration values must currently be JSON-serializable. That covers the
normal DataTables configuration objects, but not JavaScript callback functions.

## Common configuration options

Most DataTables options can be passed directly inside a named configuration.
The following options are especially useful for Sphinx-Needs tables.

### General table options

| Option | Example | Description |
| --- | --- | --- |
| `pageLength` | `50` | Number of rows shown per page. |
| `paging` | `True` | Enables or disables pagination. |
| `searching` | `True` | Enables or disables the search field. |
| `ordering` | `True` | Enables or disables column sorting. |
| `scrollX` | `True` | Adds horizontal scrolling for wide HTML tables. |
| `responsive` | `False` | Enables or disables the DataTables responsive layout. |
| `autoWidth` | `False` | Lets DataTables calculate column widths automatically when enabled. |
| `colReorder` | `True` | Allows columns to be reordered interactively. |
| `dom` | `"lBfrtip"` | Controls the placement of length, buttons, filter, table and paging controls. |
| `buttons` | `[...]` | Configures export and utility buttons such as Copy, Excel, PDF and Columns. |

A typical configuration for a requirements table is:

```python
needs_datatable_config = {
    "requirements": {
        "dom": "lBfrtip",
        "colReorder": True,
        "scrollX": True,
        "autoWidth": False,
        "responsive": False,
        "pageLength": 50,
        "buttons": [
            {
                "extend": "colvis",
                "text": "Columns",
            },
            "copy",
            "excel",
        ],
    },
}
```

### Common buttons

Buttons can either be specified by their short name or as a configuration object:

```python
"buttons": [
    "copy",
    "excel",
    {
        "extend": "colvis",
        "text": "Columns",
    },
]
```

Common button types are:

| Button | Description |
| --- | --- |
| `copy` | Copies the exported table data to the clipboard. |
| `excel` | Exports the table as an Excel file. |
| `colvis` | Opens a menu for showing and hiding columns. |
| `pdfHtml5` | Exports the table as a PDF using pdfmake. |
| `collection` | Groups multiple buttons into a drop-down menu. |

### PDF export

The most useful PDF options are:

| Option | Example | Description |
| --- | --- | --- |
| `orientation` | `"landscape"` | PDF orientation: `"portrait"` or `"landscape"`. |
| `pageSize` | `"A4"` | PDF page size, for example `"A4"`, `"A3"` or `"LETTER"`. |
| `text` | `"PDF"` | Text displayed on the export button. |
| `exportOptions` | `{"columns": ":visible"}` | Controls which rows or columns are exported. |
| `columnWidths` | `[...]` | Extension-specific option for defining pdfmake column widths. |

For a single PDF button that always exports in landscape orientation:

```python
{
    "extend": "pdfHtml5",
    "text": "PDF",
    "orientation": "landscape",
    "pageSize": "A4",
    "columnWidths": [
        "10%",
        "10%",
        "10%",
        "10%",
        "60%",
    ],
}
```

To offer both portrait and landscape export, use a button collection:

```python
{
    "extend": "collection",
    "text": "PDF",
    "buttons": [
        {
            "extend": "pdfHtml5",
            "text": "Portrait",
            "orientation": "portrait",
            "pageSize": "A4",
        },
        {
            "extend": "pdfHtml5",
            "text": "Landscape",
            "orientation": "landscape",
            "pageSize": "A4",
        },
    ],
}
```

### PDF column widths

`columnWidths` is provided by this extension. It is converted to the pdfmake
`table.widths` setting during PDF export.

The number of entries should match the number of columns exported to the PDF:

```python
"columnWidths": [
    "10%",
    "10%",
    "15%",
    "15%",
    "50%",
]
```

Supported values include:

| Value | Meaning |
| --- | --- |
| `"20%"` | Percentage of the available table width. |
| `80` | Fixed width in PDF points. |
| `"auto"` | Width is derived from the column content. |
| `"*"` | Uses available remaining width according to pdfmake's layout calculation. |

For tables that must reliably fit inside the PDF page, percentage widths whose
sum is approximately `100%` are recommended. Combinations of `"auto"` and `"*"`
can grow beyond the available page width when the content requires a larger
minimum width.

For example, this is predictable for a five-column landscape report:

```python
"columnWidths": [
    "8%",
    "12%",
    "10%",
    "15%",
    "55%",
]
```

The width definition applies to the columns exported to PDF, not necessarily to
all columns present in the HTML table. If `exportOptions` excludes columns,
`columnWidths` must describe only the remaining exported columns.

## Select a configuration

For a Sphinx-Needs ``needtable``, select a named configuration directly with
``:config:``:

```rst
.. needtable::
   :config: requirements
```

``:config:`` implicitly selects the Sphinx-Needs ``datatables`` style, so
``:style: datatables`` is not required. If another style is explicitly selected,
the build fails. Unknown configuration names are also reported during the Sphinx
build.

Existing classes are preserved:

```rst
.. needtable::
   :config: requirements
   :class: my-project-table
```

The generated table contains the Sphinx-Needs class plus the extension marker
classes:

```text
NEEDS_DATATABLES
sphinx-needs-datatables-config
sphinx-needs-datatables-config--requirements
```

For arbitrary Docutils/Sphinx table nodes, the same marker classes can still be
used directly:

```rst
.. list-table:: Example
   :class: sphinx-needs-datatables-config sphinx-needs-datatables-config--requirements
   :header-rows: 1

   * - ID
     - Status
   * - REQ_001
     - open
```

## Design boundaries

This first version intentionally does not patch or replace
`sphinx_needs/libs/html/datatables_loader.js`.

It relies on the DataTables assets already shipped by Sphinx-Needs and only
reconfigures tables that explicitly opt in.

Once Sphinx-Needs implements issue #408, the intended migration is:

1. remove `sphinx_needs_datatables_config` from `extensions`;
2. remove this package dependency;
3. keep `needs_datatable_config` and the RST `:config:` names where compatible;
