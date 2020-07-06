import fnmatch

import markdown2


class Markdown(object):

    def __init__(self, *, match_pattern="*.md", extras=None):
        self._match_pattern = match_pattern
        self._extras = extras

    def build(self, files):
        for file_name, f in files.items():
            if not fnmatch.fnmatch(file_name, self._match_pattern):
                continue

            f.contents = markdown2.markdown(f.contents, extras=self._extras).encode()
