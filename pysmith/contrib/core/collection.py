import pysmith.plugin_util


COLLECTIONS_KEY = "collections"


class Collection(object):
    """
        Creates ordered collections of files. Collections are sorted lists of :class:`~pysmith.FileInfo` objects that
        are stored in a dictionary (using the provided name as a key) in the build info
        :attr:`~pysmith.BuildInfo.metadata` under the key `collections`.

        :param str collection_name: The name of the collection.
        :param str match_pattern: The pattern of files to build the collection from.
        :param order_by: The function to use when sorting the collection. If this is a string, it will be used as the
                         key to look up the value to order by in the file's :attr:`~pysmith.FileInfo.metadata`. If this
                         is a function, it will be executed to find the value to order by.
        :type order_by: str or func(:class:`~pysmith.FileInfo`)
        :param bool reverse: If this parameter is true, the collection will be sorted in reverse order.
    """

    def __init__(self, *, collection_name, match_pattern, order_by, reverse=False):
        self._collection_name = collection_name
        self._match_pattern = match_pattern
        self._order_by = pysmith.plugin_util.lambda_or_metadata_selector(order_by)
        self._reverse = reverse

    def build(self, build_info):
        if COLLECTIONS_KEY not in build_info.metadata:
            build_info.metadata[COLLECTIONS_KEY] = {}

        if self._collection_name in build_info.metadata[COLLECTIONS_KEY]:
            raise ValueError("Collection \"{}\" already defined".format(self._collection_name))

        filtered_files = [f for file_name, f in build_info.get_files_by_pattern(self._match_pattern)]
        filtered_files.sort(key=self._order_by, reverse=self._reverse)
        build_info.metadata[COLLECTIONS_KEY][self._collection_name] = filtered_files
