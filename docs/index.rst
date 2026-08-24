sphinx-needs-datatables-config
==============================

Native Sphinx-Needs ``needtable`` configuration:

.. req:: Demo requirement
   :id: REQ_DEMO

.. needtable::
   :config: requirements
   :columns: id;title

The same configuration can also be selected for an arbitrary table by using
the marker classes directly:

.. list-table:: Example
   :class: sphinx-needs-datatables-config sphinx-needs-datatables-config--requirements
   :header-rows: 1

   * - ID
     - Title
     - Status
   * - REQ_001
     - First requirement
     - open
   * - REQ_002
     - Second requirement
     - implemented
