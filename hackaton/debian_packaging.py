import os
import logging as log
from datetime import datetime as dt

from hackaton.utils import get_sources_dir


def get_target_dir(pkg_name, pkg_version):
    sources_dir = get_sources_dir()
    return os.path.join(sources_dir, f"{pkg_name}_{pkg_version}")


def get_debian_dir(target_dir):
    return os.path.join(target_dir, "debian")


def clean_debian_dir(debian_dir):
    log.info(f"Cleaning debian directory '{debian_dir}'")
    for root, dirs, files in os.walk(debian_dir):
        for file in files:
            path = os.path.join(root, file)
            log.debug(f"Deleting file '{path}'")
            os.remove(path)
        for dir in dirs:
            path = os.path.join(root, dir)
            log.debug(f"Deleting directory '{path}'")
            os.rmdir(path)


def create_debian_changelog(pkg_name, pkg_version):
    """This is the log of changes to the Debian package. It does not need to
    list everything that has changed in upstream code, but a summary is helpful
    for others. We will not log anything, because we are lazy. However, we still
    need to make a changelog entry, because the packaging tools read information
    from the changelog: most importantly, the package version."""

    target_dir = get_target_dir(pkg_name, pkg_version)
    debian_dir = get_debian_dir(target_dir)
    changelog = os.path.join(debian_dir, "changelog")

    now = dt.now().astimezone().strftime("%a, %d %b %Y %H:%M:%S %z")

    with open(changelog, "w") as f:
        print(f"{pkg_name} ({pkg_version}-1) UNRELEASED; urgency=low", file=f)
        print("\n", file=f)  # Two newlines
        print(f" -- CFEngine <cfengine@northern.tech>  {now}", file=f)

    log.info(f"Created changelog '{changelog}'")

    # The above should produce the same output as the following command.
    f"debchange --create --package {pkg_name} --newversion {pkg_version}-1 --urgency low --empty"
    # Check out `man debchange`` for more info.


def prepare_debian_dir(pkg_name, pkg_version):
    target_dir = get_target_dir(pkg_name, pkg_version)
    debian_dir = get_debian_dir(target_dir)

    if os.path.exists(debian_dir):
        clean_debian_dir(debian_dir)
    else:
        log.debug(f"Creating directory '{debian_dir}'")
        os.makedirs(debian_dir, exist_ok=True)

    create_debian_changelog(pkg_name, pkg_version)
