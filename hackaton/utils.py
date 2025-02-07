import os


def get_cache_dir():
    return ".cache"


def get_sources_dir():
    cache_dir = get_cache_dir()
    return os.path.join(cache_dir, "sources")
