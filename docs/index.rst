Pysmith
=======

Welcome to the documentation site for Pysmith. Pysmith is a file processing pipeline heavily inspired by `Metalsmith
<https://metalsmith.io/>`_. It is primarily designed for static site generation, but is not limited to that. To use
simply construct a :class:`~pysmith.Pysmith` object, add the relevant plugins using :meth:`~pysmith.Pysmith.use`, and
execute the pipeline by calling :meth:`~pysmith.Pysmith.build`.

The project's source can be found on Github here: https://github.com/dpk2442/pysmith.

.. toctree::
   :maxdepth: 1
   :caption: Contents
   :titlesonly:

   pysmith
   plugin_interface
   plugins


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
