import os
import unittest.mock
from unittest.mock import call

from pysmith.util import scantree


def create_dir_entry(name, path, is_dir):
    entry = unittest.mock.Mock()
    entry.name = name
    entry.path = path
    entry.is_dir.return_value = is_dir
    return entry


def test_scantree(monkeypatch):
    mock_scandir = unittest.mock.MagicMock()
    monkeypatch.setattr("os.scandir", mock_scandir)

    file1_entry = create_dir_entry("file1", "root/file1", False)
    file2_entry = create_dir_entry("file2", "root/file2", False)
    file3_entry = create_dir_entry("file3", "root/dir/file3", False)
    file4_entry = create_dir_entry("file4", "root/dir/file4", False)
    mock_scandir.return_value.__enter__.side_effect = (
        (
            file1_entry,
            create_dir_entry("dir", "root/dir", True),
            file2_entry,
        ),
        (
            file3_entry,
            file4_entry,
        ),
    )

    entries = list(scantree("root"))
    assert entries == [
        ("file1", file1_entry),
        ("dir/file3", file3_entry),
        ("dir/file4", file4_entry),
        ("file2", file2_entry),
    ]

    mock_scandir.assert_has_calls((
        call("root"),
        call(os.path.join("root", "dir")),
    ), any_order=True)
