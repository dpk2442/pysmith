from pysmith import BuildInfo
from pysmith.plugin_util import lambda_or_metadata_selector


class Permalink(object):
    """
        Creates permalinks for pages. The permalink will be pulled from the :class:`~pysmith.FileInfo` object as
        specified by the `permalink_selector`, and the file will be moved under the correct key for the new path. If the
        permalink cannot be found in the :class:`~pysmith.FileInfo`, the file will not be renamed. Leading slashes are
        ignored in the permalink. If the path ends with a slash, the file will be moved to `index.html` in the specified
        folder. Otherwise the permalink will be treated as a literal path for the file.

        :param str match_pattern: The pattern of files to rename.
        :param permalink_selector: The permalink selector. If this is a string, it will be used as the key to look up
                                   the permalink in the file metadata. If this is a function, it will be executed to
                                   find the permalink.
        :type permalink_selector: str or func(:class:`~pysmith.FileInfo`)
    """

    def __init__(self, match_pattern="*.html", permalink_selector="permalink"):
        self._match_pattern = match_pattern
        self._permalink_selector = lambda_or_metadata_selector(permalink_selector)

    def build(self, build_info: BuildInfo):
        for file_name, file_info in build_info.get_files_by_pattern(self._match_pattern):
            try:
                permalink = self._permalink_selector(file_info)
            except Exception:
                continue

            if permalink.startswith("/"):
                permalink = permalink[1:]

            if permalink.endswith("/") or permalink == "":
                permalink += "index.html"

            build_info.rename_file(file_name, permalink)
