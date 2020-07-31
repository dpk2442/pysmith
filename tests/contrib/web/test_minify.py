import sys
import unittest.mock
from unittest.mock import call

import pytest

from pysmith import BuildInfo
from tests.util import MockFileInfo, create_patch

sys.modules["rjsmin"] = unittest.mock.Mock()
from pysmith.contrib.web.minify import Minify  # NOQA: E402


@pytest.fixture
def mock_jsmin(monkeypatch):
    return create_patch(monkeypatch, "rjsmin.jsmin")


def test_valid_files(mock_jsmin):
    files = {
        "test1.js": MockFileInfo(b"contents1"),
        "test2.js": MockFileInfo(b"contents2"),
    }

    mock_jsmin.side_effect = (b"parsedContents1", b"parsedContents2")

    minify = Minify()
    minify.build(BuildInfo(files))

    mock_jsmin.assert_has_calls((call(b"contents1"), call(b"contents2")))
    assert files == {
        "test1.js": MockFileInfo(b"parsedContents1"),
        "test2.js": MockFileInfo(b"parsedContents2"),
    }
