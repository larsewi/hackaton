import os
import json
import urllib
import hashlib
import logging as log
import urllib.request
from utils import get_build_dir
from context import check_context


def get_tarballs_dir():
    build_dir = get_build_dir()
    return os.path.join(build_dir, "tarballs")

def fetch_target(url, target, checksum):
    if os.path.exists(target):
        log.info(f"Skipping fetching url '{url}': target '{target}' already exists")
        return

    log.info(f"Fetching url '{url}'")
    urllib.request.urlretrieve(url, target)

    sha = hashlib.sha256()
    with open(target, 'rb') as f:
        content = f.read()
        sha.update(content)

    digest = sha.digest().hex()
    if checksum != digest:
        log.error(f"Checksum mismatch for target '{target}': ")
        os.remove(target)
        exit(1)

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
                log.error(f"Missing required field \"{field}\" in file '{filename}' for package '{pkg_name}'")
                exit(1)

        url = pkg_info["source"] + "/" + pkg_info["tarball"]
        target = os.path.join(tarballs_dir, pkg_info["tarball"])
        checksum = pkg_info["checksum"]
        fetch_target(url, target, checksum)
