import sys
import unittest.mock
from unittest.mock import call

import pytest

from pysmith import BuildInfo
from tests.util import MockFileInfo, create_patch

sys.modules["sass"] = unittest.mock.Mock()
from pysmith.contrib.web.sass import Sass  # NOQA: E402


@pytest.fixture
def mock_compile(monkeypatch):
    return create_patch(monkeypatch, "sass.compile")


def test_valid_files_no_rename(mock_compile):
    files = {
        "test1.scss": MockFileInfo("contents1"),
    }

    mock_compile.return_value = "parsedContents1"

    sass = Sass(output_extension=".scss")
    sass.build(BuildInfo(files))

    mock_compile.assert_called_once_with(string="contents1")
    assert files == {
        "test1.scss": MockFileInfo(b"parsedContents1"),
    }


def test_valid_files_rename(mock_compile):
    files = {
        "test1.scss": MockFileInfo("contents1"),
        "test2.sass": MockFileInfo("contents2"),
    }

    mock_compile.side_effect = ("parsedContents1", "parsedContents2")

    sass = Sass()
    sass.build(BuildInfo(files))

    mock_compile.assert_has_calls((call(string="contents1"), call(string="contents2")))
    assert files == {
        "test1.css": MockFileInfo(b"parsedContents1"),
        "test2.css": MockFileInfo(b"parsedContents2"),
    }


def test_compile_args(mock_compile):
    files = {
        "test1.scss": MockFileInfo("contents1"),
    }

    mock_compile.return_value = "parsedContents1"

    sass = Sass(compile_args={"extra_arg": "value"})
    sass.build(BuildInfo(files))

    mock_compile.assert_called_once_with(string="contents1", extra_arg="value")
    assert files == {
        "test1.css": MockFileInfo(b"parsedContents1"),
    }
