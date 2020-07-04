import unittest.mock


def create_patch(monkeypatch, target):
    mock = unittest.mock.Mock()
    monkeypatch.setattr(target, mock)
    return mock
