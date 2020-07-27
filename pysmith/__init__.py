"""
    The classes defined in the module make up the core of pysmith. They do not do any file processing, but handle the
    reading of the files, pipeline execution, and finally writing of the files.
"""

import logging
import os
import shutil
import time

from .util import scantree


logger = logging.getLogger("pysmith")


class BuildInfo(object):
    """
        Contains information for the current build.

        .. attribute:: metadata
            :type: dict(str, object)

            The global metadata for the build.
    """

    __slots__ = ("metadata",)

    def __init__(self):
        self.metadata = {}

    def __repr__(self):  # pragma: no cover
        self_type = type(self)
        attrs = ", ".join("{}={!r}".format(k, getattr(self, k)) for k in self.__slots__)
        return "{}.{}({})".format(self_type.__module__, self_type.__name__, attrs)


class FileInfo(object):
    """
        Contains the data for a file to be processed.

        .. attribute:: name
            :type: str

            The file name.

        .. attribute:: path
            :type: str

            The full path of the file.

        .. attribute:: stats
            :type: os.stat_result

            The stats of the file, as returned by :func:`os.stat`.

        .. attribute:: metadata
            :type: dict(str, object)

            The metadata of the file. This is a generic dictionary that can be modified by plugins.

        .. attribute:: contents
            :type: bytes

            The raw binary contents of the file.
    """

    __slots__ = ("name", "path", "stats", "metadata", "_contents")

    def __init__(self, name, path, stats, contents):
        self.name = name
        self.path = path
        self.stats = stats
        self.metadata = {}
        self._contents = contents

    @staticmethod
    def _from_entry(entry):
        with open(entry.path, "rb") as f:
            contents = f.read()

        return FileInfo(entry.name, entry.path, entry.stat(), contents)

    @property
    def contents(self) -> bytes:
        """
            Get the contents of the file.

            :returns: The file contents
        """

        return self._contents

    @contents.setter
    def contents(self, value):
        if not isinstance(value, bytes):
            raise ValueError("contents field must be a bytes object")

        self._contents = value

    def __repr__(self):  # pragma: no cover
        self_type = type(self)
        attrs = ", ".join("{}={!r}".format(k, getattr(self, k)) for k in self.__slots__)
        return "{}.{}({})".format(self_type.__module__, self_type.__name__, attrs)


class Pysmith(object):
    """
        The main pipeline processing object. To minimize potential issues, it is recommended that all paths are passed
        as absolute paths.

        :param str src: The path to the source directory.
        :param str dest: The path to the destination directory.
    """

    def __init__(self, *, src, dest):
        self._src = src
        self._dest = dest
        self._plugins = []

    def enable_logging(self):  # pragma: no cover
        """
            Enables basic logging while the build is running.

            :returns: self
        """

        formatter = logging.Formatter("{asctime} - {levelname:>8} - {name} - {message}", style="{")

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(ch)

        return self

    def use(self, plugin):
        """
            Add a new plugin instance to the pipeline.

            :param plugin: A plugin that implements the :meth:`build` method.
            :returns: self
        """

        if not callable(plugin.build):
            raise ValueError("The passed in plugin does not define a build method")

        self._plugins.append(plugin)
        return self

    def clean(self):
        """
            Recursively deletes the destination directory.

            :returns: self
        """

        shutil.rmtree(self._dest, onerror=self._handle_clean_error)
        return self

    def build(self):
        """
            Executes the plugins in the pipeline to run the build.
        """

        start_time = time.time()
        logger.info("Starting the build...")

        build_info = BuildInfo()
        files = self._load_files()
        for plugin in self._plugins:
            logger.info("Executing {}".format(type(plugin).__name__))
            plugin.build(build_info, files)

        logger.info("Writing the output files to disk...")
        for file_name, file_info in files.items():
            self._write_file(file_name, file_info.contents)

        logger.info("Build completed in {:.2}ms".format(time.time() - start_time))

    def _handle_clean_error(self, fn, path, exception_info):
        if exception_info[0] != FileNotFoundError:
            raise exception_info[1]

    def _load_files(self):
        files = {}
        for file_name, entry in scantree(self._src):
            files[file_name] = FileInfo._from_entry(entry)

        return files

    def _write_file(self, file_name, contents):
        path = os.path.join(self._dest, file_name)
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        elif not os.path.isdir(dirname):
            raise NotADirectoryError("\"{}\" is not a directory".format(dirname))

        with open(path, "wb") as f:
            f.write(contents)
