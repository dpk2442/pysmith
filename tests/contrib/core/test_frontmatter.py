import sys
import unittest.mock
from unittest.mock import call

import pytest

from pysmith import BuildInfo
from tests.util import MockFileInfo, create_patch

sys.modules["frontmatter"] = unittest.mock.Mock()
from pysmith.contrib.core.frontmatter import Frontmatter  # NOQA: E402


@pytest.fixture
def mock_parse(monkeypatch):
    return create_patch(monkeypatch, "frontmatter.parse")


def test_valid_files(mock_parse):
    files = {
        "file1": MockFileInfo("contents1"),
        "file2": MockFileInfo("contents2"),
        "file3": MockFileInfo("contents3"),
    }

    mock_parse.side_effect = (
        ({"key1": "value1"}, "newContents1"),
        ({"key2": "value2"}, "newContents2"),
        ({"key3": "value3"}, "newContents3"),
    )

    frontmatter = Frontmatter()
    frontmatter.build(BuildInfo(files))

    mock_parse.assert_has_calls((call("contents1"), call("contents2"), call("contents3")))
    assert files == {
        "file1": MockFileInfo(b"newContents1", {"key1": "value1"}),
        "file2": MockFileInfo(b"newContents2", {"key2": "value2"}),
        "file3": MockFileInfo(b"newContents3", {"key3": "value3"}),
    }


def test_existing_metadata(mock_parse):
    files = {
        "file1": MockFileInfo("contents", {
            "existingKey1": "value1",
            "existingKey2": "value2",
        })
    }

    mock_parse.return_value = ({"existingKey1": "newValue", "newKey": "value"}, "newContents")

    frontmatter = Frontmatter()
    frontmatter.build(BuildInfo(files))

    assert files == {
        "file1": MockFileInfo(b"newContents", {
            "existingKey1": "newValue",
            "existingKey2": "value2",
            "newKey": "value",
        })
    }


def test_parse_raises_exception(mock_parse):
    build_info = BuildInfo(files={
        "file1": MockFileInfo("contents"),
    })

    mock_parse.side_effect = Exception("error")

    frontmatter = Frontmatter()
    frontmatter.build(build_info)

    assert build_info.files == {
        "file1": MockFileInfo("contents"),
    }
