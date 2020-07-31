import fnmatch

import markdown2


class Markdown(object):
    """
        Renders markdown into html. The file's :attr:`~pysmith.FileInfo.contents` will be updated and the source file
        will not be renamed.

        :param str match_pattern: The pattern of files to render.
        :param extras: A list of `extras <https://github.com/trentm/python-markdown2/wiki/Extras>`_ to pass to
                       markdown2.
        :type extras: list(str) or None
    """

    def __init__(self, *, match_pattern="*.md", extras=None):
        self._match_pattern = match_pattern
        self._extras = extras

    def build(self, build_info):
        for file_name, f in build_info.get_files_by_pattern(self._match_pattern):
            f.contents = markdown2.markdown(f.contents, extras=self._extras).encode()
