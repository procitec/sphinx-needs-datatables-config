extensions = [
    "sphinx_needs",
    "sphinx_needs_datatables_config",
]

project = "sphinx-needs-datatables-config demo"
html_theme = "alabaster"

needs_datatable_config = {
    "requirements": {
        "dom": "lBfrtip",
        "colReorder": True,
        "scrollX": True,
        "autoWidth": False,
        "responsive": False,
        "pageLength": 25,
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
                        "columnWidths": ["25%", "75%"],
                    },
                    {
                        "extend": "pdfHtml5",
                        "text": "Landscape",
                        "orientation": "landscape",
                        "pageSize": "A4",
                        "columnWidths": ["25%", "75%"],
                    },
                ],
            },
        ],
    },
}
