import fnmatch

import rjsmin


class Minify(object):
    """
        Minifies javascript using :func:`rjsmin.jsmin`. The file's :attr:`~pysmith.FileInfo.contents` will be updated
        and the source file will not be renamed.

        :param str js_match_pattern: The pattern of javascript files to minify.
    """

    def __init__(self, js_match_pattern="*.js"):
        self._js_match_pattern = js_match_pattern

    def build(self, build_info, files):
        for file_name, f in files.items():
            if not fnmatch.fnmatch(file_name, self._js_match_pattern):
                continue

            f.contents = rjsmin.jsmin(f.contents)
