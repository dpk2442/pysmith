import pytest

from pysmith import BuildInfo
from pysmith.contrib.core.collection import COLLECTIONS_KEY, Collection
from tests.util import MockFileInfo


def test_collections_key_defined():
    build_info = BuildInfo()
    build_info.metadata[COLLECTIONS_KEY] = {}

    collection = Collection(collection_name="test", match_pattern="*.md", order_by="order")
    collection.build(build_info)

    assert COLLECTIONS_KEY in build_info.metadata
    assert "test" in build_info.metadata[COLLECTIONS_KEY]
    assert build_info.metadata[COLLECTIONS_KEY]["test"] == []


def test_duplicate_collection_name():
    build_info = BuildInfo()
    build_info.metadata[COLLECTIONS_KEY] = {
        "test": [],
    }

    collection = Collection(collection_name="test", match_pattern="*.md", order_by="order")

    with pytest.raises(ValueError):
        collection.build(build_info)


@pytest.mark.parametrize("reverse", (
    True,
    False,
))
def test_build(reverse):
    ordered_file_1 = MockFileInfo("contents1", metadata={"order": 1})
    ordered_file_2 = MockFileInfo("contents2", metadata={"order": 2})
    ordered_file_3 = MockFileInfo("contents3", metadata={"order": 3})
    skipped_file_1 = MockFileInfo("contents4")
    skipped_file_2 = MockFileInfo("contents5")
    files = {
        "a.md": ordered_file_3,
        "x.js": skipped_file_1,
        "b.md": ordered_file_2,
        "y.js": skipped_file_2,
        "z.md": ordered_file_1,
    }

    build_info = BuildInfo(files)
    collection = Collection(collection_name="test", match_pattern="*.md", order_by="order", reverse=reverse)
    collection.build(build_info)

    assert COLLECTIONS_KEY in build_info.metadata
    assert "test" in build_info.metadata[COLLECTIONS_KEY]

    if reverse:
        assert build_info.metadata[COLLECTIONS_KEY]["test"] == [
            ordered_file_3,
            ordered_file_2,
            ordered_file_1,
        ]
    else:
        assert build_info.metadata[COLLECTIONS_KEY]["test"] == [
            ordered_file_1,
            ordered_file_2,
            ordered_file_3,
        ]
