import os


def scantree(path, parent=""):
    with os.scandir(path) as it:
        for entry in it:
            if (entry.is_dir()):
                yield from scantree(entry.path, os.path.join(parent, entry.name))
            else:
                yield (os.path.join(parent, entry.name), entry)
