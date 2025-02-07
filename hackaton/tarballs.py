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


def fetch_tarball(url, tarball):
    if os.path.exists(tarball):
        log.debug(f"Skipping fetching url '{url}': Tarball '{tarball}' already exists")
        return

    log.info(f"Fetching {tarball}: Url '{url}'")
    urllib.request.urlretrieve(url, tarball)


def verify_tarball(tarball, checksum):
    log.info(f"Verifying checksum {checksum[:7]}... of tarball '{tarball}'")

    sha = hashlib.sha256()
    with open(tarball, "rb") as f:
        content = f.read()
        sha.update(content)

    digest = sha.digest().hex()
    if checksum != digest:
        log.error(f"Checksum mismatch for target '{tarball}': ")
        os.remove(tarball)
        exit(1)


def extract_tarball(tarball: str, target: str):
    source_dir = get_source_dir(target)
    if os.path.exists(source_dir):
        log.debug(
            f"Skipping extracting tarball '{tarball}': Source directory '{source_dir}' already exists"
        )
        return

    log.info(f"Extracting tarball '{tarball}' to source directory '{source_dir}'")
    with tarfile.open(tarball) as f:
        members = f.getmembers()
        prefix = os.path.commonprefix([m.name for m in members])

        for member in f.getmembers():
            member.name = member.name[len(prefix) :].lstrip(os.sep)
            f.extract(member, source_dir)
