Plugin Interface
================

Contract
--------

Plugins are simply an object that implements the appropriate contract, which is a build method that follows the
following signature:

.. method:: build(self, build_info)

    Executes the plugin in the current build.

    :param build_info: The information for the current build.
    :type build_info: ~pysmith.BuildInfo

Types
-----

The following types are passed to plugins during the build.

.. autoclass:: pysmith.BuildInfo()
    :members:

.. autoclass:: pysmith.FileInfo()


Logging
-------

If plugins wish to log message, they should create a logger using :func:`logging.getLogger`, passing
:code:`pysmith.plugin.<plugin_name>` as the logger name. :meth:`~pysmith.Pysmith.enable_logging` configures logging
under the :code:`pysmith` namespace, so plugins should use this name for logging to be configured correctly.


Utils
-----

The following utilities are also available for plugins to use.

.. automodule:: pysmith.plugin_util
    :members:
