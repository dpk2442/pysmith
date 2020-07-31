"""
    The classes defined in the module make up the core of pysmith. They do not do any file processing, but handle the
    reading of the files, pipeline execution, and finally writing of the files.
"""

import fnmatch
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

        .. attribute:: files
            :type: dict(str, FileInfo)

            The files uses the file path relative to the source folder as the key and :class:`~pysmith.FileInfo` objects
            as the values. Keys can be added or removed by the plugin, and files can be modified. At the end of the
            processing pipeline, files will be written based on the keys relative to the destination directory.
    """

    __slots__ = ("metadata", "files")

    def __init__(self, files=None):
        self.metadata = {}
        self.files = files or {}

    def get_files_by_pattern(self, match_pattern):
        """
            Retrieves files from the :attr:`files` object using the given glob pattern.

            :param str match_pattern: The pattern to pass to :func:`fnmatch.filter`.
        """

        for file_name in fnmatch.filter(self.files.keys(), match_pattern):
            yield file_name, self.files[file_name]

    def get_files_by_regex(self, regex):
        """
            Retrieves files from the :attr:`files` object using the given regex.

            :param regex: The regular expression to use, compiled using :func:`re.compile`.
            :type regex: :class:`re.Pattern`
        """

        for file_name in list(self.files.keys()):
            if regex.search(file_name):
                yield file_name, self.files[file_name]

    def rename_file(self, file_name, new_file_name):
        """
            Renames a file in the :attr:`files` object. If the new file name matches the old, no action is taken.

            :param str file_name: The existing name of the file.
            :param str new_file_name: The new name for the file.
        """

        if file_name not in self.files:
            raise ValueError("The specified file name does not exist")

        if file_name == new_file_name:
            return

        file_info = self.files[file_name]
        del self.files[file_name]
        self.files[new_file_name] = file_info

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

        files = self._load_files()
        build_info = BuildInfo(files)
        for plugin in self._plugins:
            logger.info("Executing {}".format(type(plugin).__name__))
            plugin.build(build_info)

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
