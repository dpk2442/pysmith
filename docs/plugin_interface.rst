Plugin Interface
================

Plugins are simply an object that implements a build method that follows the following signature:

.. method:: build(self, build_info, files)

    Executes the plugin in the current build.

    :param build_info: The information for the current build.
    :type build_info: ~pysmith.BuildInfo
    :param files: The set of files to be processed.
    :type files: dict(str, ~pysmith.FileInfo)

The files uses the file path relative to the source folder as the key and :class:`~pysmith.FileInfo` objects as the
values. Keys can be added or removed by the plugin, and files can be modified. At the end of the processing pipeline,
files will be written based on the keys relative to the destination directory.

.. autoclass:: pysmith.BuildInfo()

.. autoclass:: pysmith.FileInfo()
