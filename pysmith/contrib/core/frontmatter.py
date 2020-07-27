import fnmatch

import frontmatter


class Frontmatter(object):
    """
        Parses YAML frontmatter from files. The parsed frontmatter metadata will be added to the file's
        :attr:`~pysmith.FileInfo.metadata` and removed from the :attr:`~pysmith.FileInfo.contents`.

        :param str match_pattern: The pattern of files to parse metadata from.
    """

    def __init__(self, *, match_pattern="*"):
        self._match_pattern = match_pattern

    def build(self, build_info, files):
        for file_name, file_info in files.items():
            if not fnmatch.fnmatch(file_name, self._match_pattern):
                continue

            metadata, contents = frontmatter.parse(file_info.contents)
            file_info.metadata.update(metadata)
            file_info.contents = contents.encode()
