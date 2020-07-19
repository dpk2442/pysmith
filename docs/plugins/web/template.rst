Template
========

The template plugin is actually two plugins. The first treats the content of the file itself as the template, whereas
the second inserts the content into a layout template. This plugin uses `jinja2
<https://jinja.palletsprojects.com/en/2.11.x/>`_ to do all templating. The dependencies necessary for this plugin can be
installed using the :code:`template` extra.

.. module:: pysmith.contrib.web.template
.. autoclass:: _BaseTemplate
.. autoclass:: ContentTemplate(*, **kwargs)
.. autoclass:: LayoutTemplate
