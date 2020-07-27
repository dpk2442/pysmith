Built-in Plugins
================

The following plugins come bundled with Pysmith. To automatically install the dependencies needed for each plugin,
specify the `extra
<https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies>`_
specified in the plugin's documentation.

Core
----

The following plugins are core plugins and generally useful.

- :doc:`Collection <plugins/core/collection>`

  - This plugin creates a collection of files.

- :doc:`Frontmatter <plugins/core/frontmatter>`

  - This plugin parses YAML frontmatter into the file's metadata.

Web
---

The following plugins are designed specifically for building static sites.

- :doc:`Markdown <plugins/web/markdown>`

  - This plugin renders markdown files into HTML.

- :doc:`Minify <plugins/web/minify>`

  - This plugin minifies javascript using jsmin.

- :doc:`Sass <plugins/web/sass>`

  - This plugin compiles sass/scss files into css.

- :doc:`Template <plugins/web/template>`

  - This plugin processes the contents of the file using a template.

.. toctree::
    :maxdepth: 1
    :hidden:
    :titlesonly:

    plugins/core
    plugins/web
