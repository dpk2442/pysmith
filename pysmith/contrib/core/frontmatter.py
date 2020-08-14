import logging

import frontmatter


logger = logging.getLogger("pysmith.plugin.frontmatter")


class Frontmatter(object):
    """
        Parses YAML frontmatter from files. The parsed frontmatter metadata will be added to the file's
        :attr:`~pysmith.FileInfo.metadata` and removed from the :attr:`~pysmith.FileInfo.contents`.

        :param str match_pattern: The pattern of files to parse metadata from.
    """

    def __init__(self, *, match_pattern="*"):
        self._match_pattern = match_pattern

    def build(self, build_info):
        for file_name, file_info in build_info.get_files_by_pattern(self._match_pattern):
            try:
                metadata, contents = frontmatter.parse(file_info.contents)
                file_info.metadata.update(metadata)
                file_info.contents = contents.encode()
            except Exception:
                logger.error("Error parsing frontmatter for {}".format(file_name))
