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

        const tableConfig = window.jQuery.extend(true, {}, config);
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
