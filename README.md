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

During local development:

```bash
uv sync --dev
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

## Integration into req_tools

Keep the existing `:style: datatables` behavior and add a `:config:` option to
the custom report directives.

For example:

```rst
.. acc_requirement_report::
   :style: datatables
   :config: requirements
```

When creating the table node, call the helper:

```python
from sphinx_needs_datatables_config import mark_datatable

mark_datatable(table_node, self.options.get("config"))
```

`mark_datatable()` adds the configuration classes. It deliberately leaves an
existing `NEEDS_DATATABLES` class untouched.

This means Sphinx-Needs may initialize the table first. The extension detects
that state, destroys that DataTable instance and initializes it again with the
selected named configuration. Tables without a config marker are not touched.

If you later prefer to avoid this short-lived double initialization, req_tools
can omit `NEEDS_DATATABLES` for configured tables. The extension supports both
variants.

A minimal directive option looks like:

```python
from docutils.parsers.rst import directives

option_spec = {
    # ...
    "style": directives.unchanged,
    "config": directives.unchanged_required,
}
```

## Commands

```bash
just test
just lint
just build
just demo
```

Without `just`:

```bash
uv run pytest
uv run ruff check .
uv build
uv run sphinx-build -W -b html docs docs/_build/html
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
4. adapt only the small req_tools table-marking integration if required.
