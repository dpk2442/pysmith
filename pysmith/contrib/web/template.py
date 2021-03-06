import logging
import os

import jinja2

import pysmith.plugin_util


logger = logging.getLogger("pysmith.plugin.template")


class _BaseTemplate(object):
    """
        This class is not intended to be instantiated directly, but instead just serves to hold common logic for both
        template plugins.

        :param str match_pattern: The pattern of files to process.
        :param globals: Global values to insert into the underlying :class:`~jinja2.Environment`.
        :type globals: dict(str, object)
        :param str global_include: The name of a template (to be retrieved using
                                   :meth:`~jinja2.Environment.get_template`) containing macros that will be included
                                   in the globals list of the :class:`~jinja2.Environment`. The macros will be
                                   available in all templates, but will not have access to the rendering context.
        :param environment_args: A dictionary of options to pass to the :class:`~jinja2.Environment` constructor.
        :type environment_args: dict(str, object)
    """

    def __init__(self, *, match_pattern="*", globals=None, global_include=None, environment_args={}):
        self._match_pattern = match_pattern
        self._jinja = jinja2.Environment(**environment_args)

        if globals:
            self._jinja.globals.update(globals)

        if global_include:
            template = self._jinja.get_template(global_include)
            for key, val in template.module.__dict__.items():
                if isinstance(val, jinja2.runtime.Macro):
                    self._jinja.globals[key] = val

    def build(self, build_info):
        for file_name, file_info in build_info.get_files_by_pattern(self._match_pattern):
            output_name = self.process_file(build_info, file_name, file_info)
            if output_name is not None:
                build_info.rename_file(file_name, output_name)

    def process_file(self, build_info, file_name, file_info):  # pragma: no cover
        raise NotImplementedError("process_file is not implemented")


class ContentTemplate(_BaseTemplate):
    """
        Treats the contents of the files as a template and renders it. This can be used to do pre-processing on the
        source files. All parameters specified in :class:`_BaseTemplate` are valid for this class as well. When the
        template is rendered, the build info :attr:`~pysmith.BuildInfo.metadata` will be available as :code:`site`.
    """

    def process_file(self, build_info, file_name, file_info):
        template = self._jinja.from_string(file_info.contents.decode())
        file_info.contents = template.render(site=build_info.metadata).encode()


class LayoutTemplate(_BaseTemplate):
    """
        Treats the contents of the files as a variable to pass into a template. The layout to use is selected by the
        :code:`layout_selector` parameter. When the template is rendered, the file :attr:`~pysmith.FileInfo.contents`
        will be available in the rendering context as :code:`contents`, the file :attr:`~pysmith.FileInfo.metadata`
        will be available as :code:`page`, and the build info :attr:`~pysmith.BuildInfo.metadata` will be available as
        :code:`site`. In addition to the parameters specified below, all parameters specified in :class:`_BaseTemplate`
        are valid for this class as well.

        :param layout_selector: The layout selector. If this is a string, it will be used as the key to look up the
                                template in the file metadata. If this is a function, it will be executed to find the
                                name of the template to use.
        :type layout_selector: str or func(:class:`~pysmith.FileInfo`)
        :param str output_extension: The extension to use for the output file. The file info will be moved to a new key
                                     in the files dictionary if the file needs to be renamed to have the correct
                                     extension.
    """

    def __init__(self, *, layout_selector="layout", output_extension=".html", **kwargs):
        super().__init__(**kwargs)

        self._output_extension = output_extension
        self._layout_selector = pysmith.plugin_util.lambda_or_metadata_selector(layout_selector)

    def process_file(self, build_info, file_name, file_info):
        try:
            template_name = self._layout_selector(file_info)
        except Exception:
            logger.error("Could not find layout for {}".format(file_name))
            return None

        template = self._jinja.get_template(template_name)
        file_info.contents = template.render(contents=file_info.contents.decode(),
                                             page=file_info.metadata,
                                             site=build_info.metadata).encode()
        file_name_parts = os.path.splitext(file_name)
        if file_name_parts[1] == self._output_extension:
            return None
        else:
            return file_name_parts[0] + self._output_extension
