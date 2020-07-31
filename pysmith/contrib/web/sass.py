import os
import re

import sass


class Sass(object):
    """
        Compiles sass/scss into css. The file's :attr:`~pysmith.FileInfo.contents` will be updated and the file will be
        renamed if necessary based on the output extension.

        :param str match_pattern: A regex pattern to specify which files to compile.
        :param str output_extension: The extension the file should have after compilation.
        :param compile_args: Extra arguments to be passed to :func:`sass.compile` in addition to the
                             file contents.
        :type compile_args: dict(str, object)
    """

    def __init__(self, *, match_pattern=r".*\.(sass|scss)", output_extension=".css", compile_args={}):
        self._match_pattern = re.compile(match_pattern)
        self._output_extension = output_extension
        self._compile_args = compile_args

    def build(self, build_info):
        for file_name, f in build_info.get_files_by_regex(self._match_pattern):
            f.contents = sass.compile(string=f.contents, **self._compile_args).encode()

            file_name_parts = os.path.splitext(file_name)
            if file_name_parts[1] != self._output_extension:
                del build_info.files[file_name]
                build_info.files[file_name_parts[0] + self._output_extension] = f
