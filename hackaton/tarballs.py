import os
import urllib
import hashlib
import tarfile
import urllib.request
import logging as log
from utils import get_cache_dir, get_source_dir


def get_tarballs_dir():
    build_dir = get_cache_dir()
    return os.path.join(build_dir, "tarballs")


def get_tarball_path(tarball):
    tarballs_dir = get_tarballs_dir()
    return os.path.join(tarballs_dir, tarball)


def fetch_tarball(url, tarball):
    tarball_path = get_tarball_path(tarball)

    if os.path.exists(tarball_path):
        log.debug(
            f"Skipping fetching url '{url}': Tarball '{tarball_path}' already exists"
        )
        return

    log.info(f"Fetching {tarball_path}: Url '{url}'")
    urllib.request.urlretrieve(url, tarball_path)


def verify_tarball(tarball, checksum):
    tarball_path = get_tarball_path(tarball)

    log.info(f"Verifying checksum {checksum[:7]}... of tarball '{tarball_path}'")

    sha = hashlib.sha256()
    with open(tarball_path, "rb") as f:
        content = f.read()
        sha.update(content)

    digest = sha.digest().hex()
    if checksum != digest:
        log.error(f"Checksum mismatch for target '{tarball_path}': ")
        os.remove(tarball_path)
        exit(1)


def extract_tarball(tarball: str, target: str):
    tarball_path = get_tarball_path(tarball)
    source_dir = get_source_dir(target)

    if os.path.exists(source_dir):
        log.debug(
            f"Skipping extracting tarball '{tarball_path}': Source directory '{source_dir}' already exists"
        )
        return

    log.info(f"Extracting tarball '{tarball_path}' to source directory '{source_dir}'")
    with tarfile.open(tarball_path) as f:
        members = f.getmembers()
        prefix = os.path.commonprefix([m.name for m in members])

        for member in f.getmembers():
            member.name = member.name[len(prefix) :].lstrip(os.sep)
            f.extract(member, source_dir)
