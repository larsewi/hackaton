import os
import json
import urllib
import hashlib
import tarfile
import logging as log
import urllib.request
from utils import get_cache_dir
from context import check_context


def get_tarballs_dir():
    build_dir = get_cache_dir()
    return os.path.join(build_dir, "tarballs")


def get_sources_dir():
    build_dir = get_cache_dir()
    return os.path.join(build_dir, "sources")


def fetch_tarball(url, tarball):
    if os.path.exists(tarball):
        log.info(f"Skipping fetching url '{url}': Tarball '{tarball}' already exists")
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


def extract_tarball(tarball, source):
    if os.path.exists(source):
        log.info(
            f"Skipping extracting tarball '{tarball}': Source '{source}' already exists"
        )
        return

    with tarfile.open(tarball) as f:
        f.extractall(source)


def package_dependencies(ctx):
    tarballs_dir = get_tarballs_dir()
    log.info(f"Creating directory '{tarballs_dir}'")
    os.makedirs(tarballs_dir, exist_ok=True)

    filename = "deps-packaging.json"
    with open(filename, "r") as f:
        deps = json.load(f)

    for pkg_name, pkg_info in deps.items():
        expr = pkg_info.get("expression", "any")
        if expr and not check_context(ctx, expr):
            log.info(f"Skipping dependency {pkg_name}: Not in context '{expr}'")
            continue
        log.info(f"Building dependency '{pkg_name}'")

        for field in ("source", "tarball", "checksum"):
            if field not in pkg_info:
                log.error(
                    f"Missing required field \"{field}\" in file '{filename}' for package '{pkg_name}'"
                )
                exit(1)

        url = f"{pkg_info["source"]}/{pkg_info["tarball"]}"
        tarball = os.path.join(tarballs_dir, pkg_info["tarball"])
        fetch_tarball(url, tarball)

        checksum = pkg_info["checksum"]
        verify_tarball(tarball, checksum)

        sources_dir = get_sources_dir()
        source = f"{sources_dir}/{pkg_name}_{pkg_info["version"]}"
        extract_tarball(tarball, source)
