import sys
import unittest.mock
from unittest.mock import call

import pytest

from tests.util import MockFileInfo, create_patch

sys.modules["jinja2"] = unittest.mock.Mock()
from pysmith.contrib.web.template import _BaseTemplate, ContentTemplate, LayoutTemplate  # NOQA: E402


class MockMacro(object):
    pass


sys.modules["jinja2"].runtime.Macro = MockMacro


@pytest.fixture
def mock_environment_constructor(monkeypatch):
    mock = create_patch(monkeypatch, "jinja2.Environment")
    mock.return_value.globals = {}
    return mock


class TestBaseTemplate(object):

    def test_init_no_globals(self, mock_environment_constructor):
        template = _BaseTemplate(match_pattern="*.md", environment_args={"key": "value"})

        mock_environment_constructor.assert_called_once_with(key="value")
        assert template._match_pattern == "*.md"
        assert template._jinja == mock_environment_constructor.return_value
        assert template._jinja.globals == {}

    def test_init_with_globals(self, mock_environment_constructor):
        template = _BaseTemplate(match_pattern="*.md",
                                 globals={"global": "globalValue"}, environment_args={"key": "value"})

        mock_environment_constructor.assert_called_once_with(key="value")
        assert template._jinja.globals == {
            "global": "globalValue",
        }

    def test_init_with_global_include(self, mock_environment_constructor):
        mock_template = mock_environment_constructor.return_value.get_template.return_value
        macro1 = MockMacro()
        macro2 = MockMacro()
        mock_template.module.__dict__ = {
            "global1": macro1,
            "global2": macro2,
            "global3": "nonMacroValue",
        }

        template = _BaseTemplate(match_pattern="*.md", global_include="globalInclude",
                                 environment_args={"key": "value"})

        mock_environment_constructor.assert_called_once_with(key="value")
        mock_environment_constructor.return_value.get_template.assert_called_once_with("globalInclude")
        assert template._jinja.globals == {
            "global1": macro1,
            "global2": macro2,
        }

    def test_build_no_matching_files(self, mock_environment_constructor):
        mock_process_file = unittest.mock.Mock()
        files = {
            "test1.html": None,
            "test2.js": None,
            "test3.css": None,
        }

        template = _BaseTemplate(match_pattern="*.md")
        template.process_file = mock_process_file
        template.build(files)

        mock_environment_constructor.assert_called_once_with()
        mock_process_file.assert_not_called()

    def test_build_with_some_renames(self, mock_environment_constructor):
        mock_process_file = unittest.mock.Mock()
        mock_process_file.side_effect = [None, "renamed.md"]
        mock_file_1 = MockFileInfo("contents1")
        mock_file_2 = MockFileInfo("contents2")
        files = {
            "test1.md": mock_file_1,
            "test2.md": mock_file_2,
        }

        template = _BaseTemplate(match_pattern="*.md")
        template.process_file = mock_process_file
        template.build(files)

        mock_environment_constructor.assert_called_once_with()
        mock_process_file.assert_has_calls((
            call("test1.md", mock_file_1),
            call("test2.md", mock_file_2),
        ))
        assert files == {
            "test1.md": MockFileInfo("contents1"),
            "renamed.md": MockFileInfo("contents2"),
        }


class TestContentTemplate(object):

    def test_process_file(self, mock_environment_constructor):
        mock_from_string = mock_environment_constructor.return_value.from_string
        mock_template = mock_from_string.return_value
        mock_template.render.return_value = "rendered"

        file_info = MockFileInfo(b"original")
        template = ContentTemplate()
        template.process_file("name", file_info)

        mock_from_string.assert_called_once_with("original")
        mock_template.render.assert_called_once_with()
        assert file_info == MockFileInfo(b"rendered")


class TestLayoutTemplate(object):

    def test_init_str_layout_selector(self, mock_environment_constructor):
        file_info = MockFileInfo("contents", metadata={"layout": "test"})

        template = LayoutTemplate(layout_selector="layout")

        assert callable(template._layout_selector)
        assert template._layout_selector(file_info) == "test"

    def test_init_lambda(self, mock_environment_constructor):
        file_info = MockFileInfo("contents", metadata={"randomPropName": "value"})

        template = LayoutTemplate(layout_selector=lambda f: f.contents + f.metadata["randomPropName"])

        assert callable(template._layout_selector)
        assert template._layout_selector(file_info) == "contentsvalue"

    @pytest.fixture(ids=(
        "no_rename",
        "with_rename",
    ), params=(
        (".md", "test.md", None),
        (".html", "test.md", "test.html"),
    ))
    def process_file_variants(self, request):
        return request.param

    def test_process_file(self, mock_environment_constructor, process_file_variants):
        output_extension, input_name, expected_output_name = process_file_variants

        file_info = MockFileInfo(b"contents", metadata={"layout": "test"})
        mock_get_template = mock_environment_constructor.return_value.get_template
        mock_template = mock_get_template.return_value
        mock_template.render.return_value = "rendered"

        template = LayoutTemplate(output_extension=output_extension)
        output_name = template.process_file(input_name, file_info)

        mock_get_template.assert_called_once_with("test")
        mock_template.render.assert_called_once_with(contents="contents", page={"layout": "test"})
        assert output_name == expected_output_name
        assert file_info == MockFileInfo(b"rendered", metadata={"layout": "test"})
