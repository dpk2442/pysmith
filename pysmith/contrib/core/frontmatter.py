import fnmatch

import frontmatter


class Frontmatter(object):

    def __init__(self, *, match_pattern="*"):
        self._match_pattern = match_pattern

    def build(self, files):
        for file_name, file_info in files.items():
            if not fnmatch.fnmatch(file_name, self._match_pattern):
                continue

            metadata, contents = frontmatter.parse(file_info.contents)
            file_info.metadata.update(metadata)
            file_info.contents = contents.encode()
