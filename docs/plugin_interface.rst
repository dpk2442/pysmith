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
