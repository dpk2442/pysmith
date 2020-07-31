import os
import re
import unittest.mock
from unittest.mock import call

import pytest

from pysmith import BuildInfo, FileInfo, Pysmith
from .util import MockFileInfo, create_patch


@pytest.fixture
def mock_rmtree(monkeypatch):
    return create_patch(monkeypatch, "shutil.rmtree")


@pytest.fixture
def mock_scantree(monkeypatch):
    return create_patch(monkeypatch, "pysmith.scantree")


@pytest.fixture
def mock_file_info_from_entry(monkeypatch):
    return create_patch(monkeypatch, "pysmith.FileInfo._from_entry")


@pytest.fixture
def mock_exists(monkeypatch):
    return create_patch(monkeypatch, "os.path.exists")


@pytest.fixture
def mock_makedirs(monkeypatch):
    return create_patch(monkeypatch, "os.makedirs")


@pytest.fixture
def mock_isdir(monkeypatch):
    return create_patch(monkeypatch, "os.path.isdir")


@pytest.fixture
def mock_open(monkeypatch):
    mock = unittest.mock.mock_open()
    monkeypatch.patch("__builtin__.open", mock)
    return mock


class TestBuildInfo(object):

    def test_constructor(self):
        build_info = BuildInfo()
        assert build_info.metadata == {}

    def test_get_files_by_pattern(self):
        build_info = BuildInfo(files={
            "file1.html": "file1",
            "file2.css": "file2",
        })

        assert list(build_info.get_files_by_pattern("*.css")) == [
            ("file2.css", "file2"),
        ]

    def test_get_files_by_regex(self):
        build_info = BuildInfo(files={
            "file1.html": "file1",
            "file2.css": "file2",
            "file3.js": "file3",
        })

        regex = re.compile(r".*\.(html|js)")
        assert list(build_info.get_files_by_regex(regex)) == [
            ("file1.html", "file1"),
            ("file3.js", "file3"),
        ]

    def test_rename_file_invalid_name(self):
        build_info = BuildInfo(files={
            "file1.txt": "contents",
        })

        with pytest.raises(ValueError):
            build_info.rename_file("bad_name", "new_name")

    def test_rename_file_same_name(self):
        mock_files = unittest.mock.MagicMock()
        mock_files.__contains__.return_value = True

        build_info = BuildInfo(files=mock_files)

        build_info.rename_file("name", "name")

        mock_files.__getitem__.assert_not_called()
        mock_files.__delitem__.assert_not_called()
        mock_files.__setitem__.assert_not_called()

    def test_rename_file_success(self):
        build_info = BuildInfo(files={
            "file1.txt": "contents",
        })

        build_info.rename_file("file1.txt", "file2.txt")

        assert build_info.files == {
            "file2.txt": "contents",
        }


class TestFileInfo(object):

    def test_from_entry(self):
        mock_open = unittest.mock.mock_open()
        mock_open.return_value.read.return_value = b"contents"
        entry = unittest.mock.Mock()
        entry.name = "name"
        entry.path = "path"
        entry.stat.return_value = "stats"

        with unittest.mock.patch("pysmith.open", mock_open):
            info = FileInfo._from_entry(entry)

        assert info.name == "name"
        assert info.path == "path"
        assert info.stats == "stats"
        assert info.metadata == {}
        assert info._contents == b"contents"

    def test_contents_setter_non_bytes_passed(self):
        info = FileInfo("name", "path", "stats", b"contents")

        with pytest.raises(ValueError):
            info.contents = "string contents"

    def test_contents_setter_bytes_passed(self):
        info = FileInfo("name", "path", "stats", b"contents")
        info.contents = b"bytes contents"
        assert info.contents == b"bytes contents"


class TestPysmith(object):

    def test_constructor(self):
        pysmith = Pysmith(src="src", dest="dest")
        assert pysmith._src == "src"
        assert pysmith._dest == "dest"
        assert pysmith._plugins == []

    def test_use(self):
        pysmith = Pysmith(src="src", dest="dest")
        mock_plugin = unittest.mock.Mock()

        pysmith.use(mock_plugin)

        assert pysmith._plugins == [mock_plugin]

    def test_use_build_not_callable(self):
        pysmith = Pysmith(src="src", dest="dest")
        mock_plugin = unittest.mock.Mock()
        mock_plugin.build = "str"

        with pytest.raises(ValueError):
            pysmith.use(mock_plugin)

    def test_clean(self, mock_rmtree):
        pysmith = Pysmith(src="src", dest="dest")

        pysmith.clean()

        mock_rmtree.assert_called_once_with(pysmith._dest, onerror=pysmith._handle_clean_error)

    def test_build(self, monkeypatch):
        mock_plugin1 = unittest.mock.Mock()
        mock_plugin2 = unittest.mock.Mock()
        mock_build_info_constructor = create_patch(monkeypatch, "pysmith.BuildInfo")
        mock_build_info = mock_build_info_constructor.return_value
        mock_files = {
            "f1": MockFileInfo("value1"),
            "f2": MockFileInfo("value2"),
        }

        pysmith = Pysmith(src="src", dest="dest")
        pysmith.use(mock_plugin1).use(mock_plugin2)
        pysmith._load_files = unittest.mock.Mock()
        pysmith._load_files.return_value = mock_files
        pysmith._write_file = unittest.mock.Mock()

        pysmith.build()

        pysmith._load_files.assert_called_once_with()
        mock_build_info_constructor.assert_called_once_with(pysmith._load_files.return_value)
        mock_plugin1.build.assert_called_once_with(mock_build_info)
        mock_plugin2.build.assert_called_once_with(mock_build_info)
        pysmith._write_file.assert_has_calls((
            call("f1", "value1"),
            call("f2", "value2"),
        ))

    def test_handle_errors_consumes_filenotfound(self):
        pysmith = Pysmith(src="src", dest="dest")
        pysmith._handle_clean_error(None, None, (FileNotFoundError, FileNotFoundError("error")))

    def test_handle_errors_raises_other_exceptions(self):
        pysmith = Pysmith(src="src", dest="dest")
        with pytest.raises(ValueError):
            pysmith._handle_clean_error(None, None, (ValueError, ValueError("error")))

    def test_load_files(self, mock_scantree, mock_file_info_from_entry):
        mock_scantree.return_value = [
            ("f1", "value1"),
            ("f2", "value2"),
        ]
        mock_file_info_from_entry.side_effect = ["fileInfo1", "fileInfo2"]

        pysmith = Pysmith(src="src", dest="dest")
        files = pysmith._load_files()

        assert files == {
            "f1": "fileInfo1",
            "f2": "fileInfo2",
        }
        mock_scantree.assert_called_once_with("src")
        mock_file_info_from_entry.assert_has_calls((call("value1"), call("value2")))

    def test_write_file_directory_exists(self, mock_exists, mock_isdir):
        mock_open = unittest.mock.mock_open()
        mock_exists.return_value = True
        mock_isdir.return_value = True

        pysmith = Pysmith(src="src", dest="dest")
        with unittest.mock.patch("pysmith.open", mock_open):
            pysmith._write_file("file_name", b"contents")

        path = os.path.join("dest", "file_name")
        dirname = os.path.dirname(path)
        mock_exists.assert_called_once_with(dirname)
        mock_isdir.assert_called_once_with(dirname)
        mock_open.assert_called_once_with(path, "wb")
        mock_open.return_value.write.assert_called_once_with(b"contents")

    def test_write_file_directory_does_not_exist(self, mock_exists, mock_makedirs, mock_isdir):
        mock_open = unittest.mock.mock_open()
        mock_exists.return_value = False

        pysmith = Pysmith(src="src", dest="dest")
        with unittest.mock.patch("pysmith.open", mock_open):
            pysmith._write_file("file_name", b"contents")

        path = os.path.join("dest", "file_name")
        dirname = os.path.dirname(path)
        mock_exists.assert_called_once_with(dirname)
        mock_makedirs.assert_called_once_with(dirname)
        mock_isdir.assert_not_called()
        mock_open.assert_called_once_with(path, "wb")
        mock_open.return_value.write.assert_called_once_with(b"contents")

    def test_write_file_path_is_not_directory(self, mock_exists, mock_isdir):
        mock_exists.return_value = True
        mock_isdir.return_value = False

        pysmith = Pysmith(src="src", dest="dest")
        with pytest.raises(NotADirectoryError):
            pysmith._write_file("file_name", b"contents")
