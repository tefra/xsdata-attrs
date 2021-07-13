Code Generation
===============

All the xsdata :ref:`cli <xsdata:Command Line>` features are available. You only need
to specify **attrs** as the output format


Example from Schema
-------------------

.. code:: console

    $ xsdata tests/fixtures/schemas/po.xsd --output attrs --package tests.fixtures.po.models --structure-style single-package
    Parsing schema po.xsd
    Compiling schema po.xsd
    Builder: 6 main and 1 inner classes
    Analyzer input: 6 main and 1 inner classes
    Analyzer output: 5 main and 1 inner classes
    Generating package: init
    Generating package: tests.fixtures.po.models



Generated Models
----------------

.. literalinclude:: /../tests/fixtures/po/models.py
   :language: python
