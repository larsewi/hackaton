import os
import json
import subprocess
import logging as log

from utils import get_source_dir
from context import check_context
from tarballs import get_tarballs_dir, fetch_tarball, extract_tarball, verify_tarball


def get_debian_dir(target):
    sources_dir = get_source_dir(target)
    return os.path.join(sources_dir, "debian")


def prepare_debian_dir(target):
    debian_dir = get_debian_dir(target)

    if os.path.exists(debian_dir):
        log.info(f"Cleaning debian directory '{debian_dir}' for target '{target}'")
        for root, dirs, files in os.walk(debian_dir):
            for file in files:
                path = os.path.join(root, file)
                log.debug(f"Deleting file '{path}'")
                os.remove(path)
            for dir in dirs:
                path = os.path.join(root, dir)
                log.debug(f"Deleting directory '{path}'")
                os.rmdir(path)
        return

    log.debug(f"Creating directory '{debian_dir}'")
    os.makedirs(debian_dir, exist_ok=True)
    return


def create_changelog(target, pkg_name, pkg_info):
    """This is the log of changes to the Debian package. It does not need to
    list everything that has changed in upstream code, but a summary is helpful
    for others. We will not log anything, because we are lazy. However, we still
    need to make a changelog entry, because the packaging tools read information
    from the changelog: most importantly, the package version."""

    source_dir = get_source_dir(target)
    debian_dir = get_debian_dir(target)
    changelog = os.path.join(debian_dir, "changelog")

    if os.path.exists(changelog):
        log.info(f"Skipping creating changelog: Changelog '{changelog}' already exists")
        return

    cmd = [
        "dch",
        "--create",  # Create new
        "--package",  # Package name
        pkg_name,
        "--newversion",  # Package version number
        f'{pkg_info["version"]}-1',
        "--urgency",  # How important is the package
        "low",
        "--empty",  # Don't add any change logs
    ]
    env = {"DEBFULLNAME": "CFEngine", "DEBEMAIL": "cfengine@northern.tech"}
    log.debug(
        f"Executing command '{' '.join(cmd)}' from directory '{source_dir}': Environment: {env}"
    )
    subprocess.run(cmd, cwd=source_dir, env=env)
    log.info(f"Created changelog '{changelog}' for target '{target}'")


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
        tarball = os.path.join(tarballs_dir, pkg_info["tarball"])
        fetch_tarball(url, tarball)

        checksum = pkg_info["checksum"]
        verify_tarball(tarball, checksum)

        target = f'{pkg_name}_{pkg_info["version"]}'
        extract_tarball(tarball, target)

        prepare_debian_dir(target)

        create_changelog(target, pkg_name, pkg_info)
