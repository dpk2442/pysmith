import os
import shutil

from .util import scantree


class FileInfo(object):

    __slots__ = ("name", "path", "stats", "metadata", "_contents")

    def __init__(self, name, path, stats, contents):
        self.name = name
        self.path = path
        self.stats = stats
        self.metadata = {}
        self._contents = contents

    @staticmethod
    def from_entry(entry):
        with open(entry.path, "rb") as f:
            contents = f.read()

        return FileInfo(entry.name, entry.path, entry.stat(), contents)

    @property
    def contents(self):
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

    def __init__(self, *, src, dest):
        self._src = src
        self._dest = dest
        self._plugins = []

    def use(self, plugin):
        if not callable(plugin.build):
            raise ValueError("The passed in plugin does not define a build method")

        self._plugins.append(plugin)
        return self

    def clean(self):
        shutil.rmtree(self._dest, onerror=self._handle_clean_error)
        return self

    def build(self):
        files = self._load_files()
        for plugin in self._plugins:
            plugin.build(files)

        for file_name, file_info in files.items():
            self._write_file(file_name, file_info.contents)

    def _handle_clean_error(self, fn, path, exception_info):
        if exception_info[0] != FileNotFoundError:
            raise exception_info[1]

    def _load_files(self):
        files = {}
        for file_name, entry in scantree(self._src):
            files[file_name] = FileInfo.from_entry(entry)

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
