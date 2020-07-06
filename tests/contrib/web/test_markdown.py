import sys
import unittest.mock
from unittest.mock import call

import pytest

from tests.util import MockFileInfo, create_patch

sys.modules["markdown2"] = unittest.mock.Mock()
from pysmith.contrib.web.markdown import Markdown  # NOQA: E402


@pytest.fixture
def mock_markdown2(monkeypatch):
    return create_patch(monkeypatch, "markdown2.markdown")


def test_skips_unmatched_files(mock_markdown2):
    files = {
        "test1.html": None,
        "test2.js": None,
        "test3.css": None,
    }

    markdown = Markdown()
    markdown.build(files)

    mock_markdown2.assert_not_called()


def test_valid_files(mock_markdown2):
    files = {
        "test1.md": MockFileInfo("contents1"),
        "test2.md": MockFileInfo("contents2"),
    }

    mock_markdown2.side_effect = ("parsedContents1", "parsedContents2")

    markdown = Markdown()
    markdown.build(files)

    mock_markdown2.assert_has_calls((call("contents1", extras=None), call("contents2", extras=None)))
    assert files == {
        "test1.md": MockFileInfo(b"parsedContents1"),
        "test2.md": MockFileInfo(b"parsedContents2"),
    }


def test_extras(mock_markdown2):
    files = {
        "test.md": MockFileInfo("contents"),
    }

    mock_markdown2.return_value = "parsedContents"

    markdown = Markdown(extras="test")
    markdown.build(files)

    mock_markdown2.assert_called_once_with("contents", extras="test")
    assert files == {
        "test.md": MockFileInfo(b"parsedContents"),
    }
