import os


def get_cache_dir():
    return "cache"


def get_source_dir(target):
    build_dir = get_cache_dir()
    return os.path.join(build_dir, "sources", target)
