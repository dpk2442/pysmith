import unittest.mock

import pytest

from pysmith.plugin_util import lambda_or_metadata_selector


@pytest.mark.parametrize("selector", (
    "key",
    lambda f: f.metadata["key"],
), ids=("str", "lambda"))
def test_lambda_or_metadata_selector(selector):
    selector = lambda_or_metadata_selector(selector)

    mock_file_info = unittest.mock.MagicMock()
    mock_file_info.metadata.__getitem__.return_value = "value"

    assert callable(selector)
    assert selector(mock_file_info) == "value"
    mock_file_info.metadata.__getitem__.assert_called_once_with("key")


def test_lambda_or_metadata_selector_invalid_input_type():
    with pytest.raises(ValueError):
        lambda_or_metadata_selector(None)
