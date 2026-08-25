(function () {
    "use strict";

    const TABLE_CLASS = "sphinx-needs-datatables-config";
    const CONFIG_CLASS_PREFIX = TABLE_CLASS + "--";

    function getConfigName(table) {
        if (table.dataset && table.dataset.needsDatatableConfig) {
            return table.dataset.needsDatatableConfig;
        }

        for (const className of table.classList) {
            if (className.startsWith(CONFIG_CLASS_PREFIX)) {
                return className.substring(CONFIG_CLASS_PREFIX.length);
            }
        }

        return null;
    }

    function findPdfTable(doc) {
        if (!doc || !Array.isArray(doc.content)) {
            return null;
        }

        for (const item of doc.content) {
            if (item && item.table && Array.isArray(item.table.body)) {
                return item;
            }
        }

        return null;
    }

    function prepareButton(button) {
        if (!button || typeof button !== "object" || Array.isArray(button)) {
            return;
        }

        if (Object.prototype.hasOwnProperty.call(button, "columnWidths")) {
            const columnWidths = button.columnWidths;
            delete button.columnWidths;

            if (!Array.isArray(columnWidths)) {
                console.warn(
                    "sphinx-needs-datatables-config: columnWidths must be an array",
                    button
                );
            } else if (button.extend !== "pdf" && button.extend !== "pdfHtml5") {
                console.warn(
                    "sphinx-needs-datatables-config: columnWidths is only supported " +
                        "for pdf/pdfHtml5 buttons",
                    button
                );
            } else {
                button.customize = function (doc) {
                    const pdfTable = findPdfTable(doc);

                    if (!pdfTable) {
                        console.warn(
                            "sphinx-needs-datatables-config: no table found in PDF document"
                        );
                        return;
                    }

                    pdfTable.table.widths = columnWidths;
                };
            }
        }

        if (Array.isArray(button.buttons)) {
            button.buttons.forEach(prepareButton);
        }
    }

    function prepareTableConfig(config) {
        const tableConfig = window.jQuery.extend(true, {}, config);

        if (Array.isArray(tableConfig.buttons)) {
            tableConfig.buttons.forEach(prepareButton);
        }

        return tableConfig;
    }

    function initializeTable(table, configs) {
        const configName = getConfigName(table);

        if (!configName) {
            console.warn(
                "sphinx-needs-datatables-config: table has no configuration name",
                table
            );
            return;
        }

        const config = configs[configName];
        if (!config) {
            console.warn(
                "sphinx-needs-datatables-config: unknown configuration '" +
                    configName +
                    "'",
                table
            );
            return;
        }

        if (
            typeof window.jQuery === "undefined" ||
            typeof window.jQuery.fn.DataTable === "undefined"
        ) {
            console.error(
                "sphinx-needs-datatables-config: DataTables is not available"
            );
            return;
        }

        if (window.jQuery.fn.dataTable.isDataTable(table)) {
            console.warn(
                "sphinx-needs-datatables-config: table was already initialized",
                table
            );
            return;
        }

        const tableConfig = prepareTableConfig(config);
        window.jQuery(table).DataTable(tableConfig);
    }

    window.jQuery(document).ready(function () {
        const configs = window.SPHINX_NEEDS_DATATABLE_CONFIG || {};

        document
            .querySelectorAll("table." + TABLE_CLASS)
            .forEach(function (table) {
                initializeTable(table, configs);
            });
    });
})();
