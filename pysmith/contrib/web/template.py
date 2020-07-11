import fnmatch
import os

import jinja2


class _BaseTemplate(object):

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

    def build(self, files):
        for file_name in list(files.keys()):
            if not fnmatch.fnmatch(file_name, self._match_pattern):
                continue

            output_name = self.process_file(file_name, files[file_name])
            if output_name is not None:
                files[output_name] = files[file_name]
                del files[file_name]

    def process_file(self, file_name, file_info):  # pragma: no cover
        raise NotImplementedError("process_file is not implemented")


class ContentTemplate(_BaseTemplate):

    def process_file(self, file_name, file_info):
        template = self._jinja.from_string(file_info.contents.decode())
        file_info.contents = template.render().encode()


class LayoutTemplate(_BaseTemplate):

    def __init__(self, *, layout_selector="layout", output_extension=".html", **kwargs):
        super().__init__(**kwargs)

        self._output_extension = output_extension

        if (isinstance(layout_selector, str)):
            self._layout_selector = lambda f: f.metadata[layout_selector]
        else:
            self._layout_selector = layout_selector

    def process_file(self, file_name, file_info):
        template = self._jinja.get_template(self._layout_selector(file_info))
        file_info.contents = template.render(contents=file_info.contents.decode(),
                                             page=file_info.metadata).encode()
        file_name_parts = os.path.splitext(file_name)
        if file_name_parts[1] == self._output_extension:
            return None
        else:
            return file_name_parts[0] + self._output_extension
