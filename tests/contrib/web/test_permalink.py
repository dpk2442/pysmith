import unittest.mock
from unittest.mock import call

from pysmith import BuildInfo
from pysmith.contrib.web.permalink import Permalink
from tests.util import MockFileInfo


def test_build(monkeypatch):
    build_info = BuildInfo(files={
        "file1.html": MockFileInfo("file1"),
        "file2.txt": MockFileInfo("file2"),
        "file3.html": MockFileInfo("file3", metadata={"permalink": "file3"}),
        "file4.html": MockFileInfo("file4", metadata={"permalink": "/file4"}),
        "file5.html": MockFileInfo("file5", metadata={"permalink": "/file5/"}),
        "file6.html": MockFileInfo("file6", metadata={"permalink": "/"}),
        "file7.html": MockFileInfo("file6", metadata={"permalink": ""}),
    })

    mock_rename_file = unittest.mock.Mock()
    with unittest.mock.patch("pysmith.BuildInfo.rename_file", mock_rename_file):
        permalink = Permalink()
        permalink.build(build_info)

    mock_rename_file.assert_has_calls((
        call("file3.html", "file3"),
        call("file4.html", "file4"),
        call("file5.html", "file5/index.html"),
        call("file6.html", "index.html"),
        call("file7.html", "index.html"),
    ))
