import unittest.mock


class MockFileInfo(object):

    def __init__(self, contents, metadata=None):
        self.contents = contents
        self.metadata = metadata or {}

    def __eq__(self, other):
        return self.contents == other.contents and self.metadata == other.metadata

    def __repr__(self):
        return "MockFileInfo(contents={}, metadata={}".format(self.contents, self.metadata)


def create_patch(monkeypatch, target):
    mock = unittest.mock.Mock()
    monkeypatch.setattr(target, mock)
    return mock
