import os
import json
import logging as log

from hackaton.context import check_context
from hackaton.tarballs import (
    get_tarballs_dir,
    fetch_tarball,
    extract_tarball,
    verify_tarball,
)
from hackaton.debian_packaging import prepare_debian_dir, create_debian_changelog


def package_dependencies(ctx):
    tarballs_dir = get_tarballs_dir()
    if not os.path.exists(tarballs_dir):
        log.info(f"Creating directory '{tarballs_dir}'")
        os.makedirs(tarballs_dir, exist_ok=True)

    filename = "deps-packaging.json"
    with open(filename, "r") as f:
        deps = json.load(f)

    for pkg_name, pkg_info in deps.items():
        expr = pkg_info.get("expression", "any")
        if expr and not check_context(ctx, expr):
            log.debug(f"Skipping dependency {pkg_name}: Not in context '{expr}'")
            continue
        log.info(f"Building dependency '{pkg_name}'")

        for field in ("source", "tarball", "checksum", "version"):
            if field not in pkg_info:
                log.error(
                    f"Missing required field \"{field}\" in file '{filename}' for package '{pkg_name}'"
                )
                exit(1)

        url = f'{pkg_info["source"]}/{pkg_info["tarball"]}'
        tarball = pkg_info["tarball"]
        fetch_tarball(url, tarball)

        checksum = pkg_info["checksum"]
        verify_tarball(tarball, checksum)

        target = f'{pkg_name}_{pkg_info["version"]}'
        extract_tarball(tarball, target)

        prepare_debian_dir(target)

        create_debian_changelog(target, pkg_name, pkg_info)
