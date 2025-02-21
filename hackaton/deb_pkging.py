import os
import subprocess
import logging as log
from datetime import datetime as dt

from hackaton.utils import get_sources_dir


def get_target_dir(pkg_name: str, pkg_version: str):
    sources_dir = get_sources_dir()
    pkg_name = f"cfbuild-{pkg_name.lower()}"
    return os.path.join(sources_dir, f"{pkg_name}_{pkg_version}")


def get_debian_dir(target_dir):
    return os.path.join(target_dir, "debian")


def clean_debian_dir(debian_dir):
    """Some repositories provide their own debian directory and we don't want to
    use that."""

    log.info(f"Cleaning debian directory '{debian_dir}'")
    for root, dirs, files in os.walk(debian_dir, topdown=False):
        for file in files:
            path = os.path.join(root, file)
            log.debug(f"Deleting file '{path}'")
            os.remove(path)
        for dir in dirs:
            path = os.path.join(root, dir)
            log.debug(f"Deleting directory '{path}'")
            os.rmdir(path)


def create_debian_changelog(pkg_name: str, pkg_version: str):
    """This is the log of changes to the Debian package. It does not need to
    list everything that has changed in upstream code, but a summary is helpful
    for others. We will not log anything, because we are lazy. However, we still
    need to make a changelog entry, because the packaging tools read information
    from the changelog: most importantly, the package version. For more
    information on changelog, see
    https://www.debian.org/doc/debian-policy/ch-controlfields.html"""

    target_dir = get_target_dir(pkg_name, pkg_version)
    debian_dir = get_debian_dir(target_dir)
    changelog_file = os.path.join(debian_dir, "changelog")

    now = dt.now().astimezone().strftime("%a, %d %b %Y %H:%M:%S %z")

    with open(changelog_file, "w") as f:
        print(
            f"cfbuild-{pkg_name.lower()} ({pkg_version}) UNRELEASED; urgency=low",
            file=f,
        )
        print("", file=f)  # Extra newline
        print("  * Initial release.", file=f)
        print("", file=f)  # Extra newline
        print(f" -- CFEngine Packager <cfengine@northern.tech>  {now}", file=f)

    log.info(f"Created changelog file '{changelog_file}'")


def create_debian_control(pkg_name: str, pkg_version: str):
    """The control file describes the source and binary package, and gives some
    information about them, such as their names, who the package maintainer is,
    and so on. See
    https://www.debian.org/doc/debian-policy/ch-controlfields.html for more
    information"""

    target_dir = get_target_dir(pkg_name, pkg_version)
    debian_dir = get_debian_dir(target_dir)
    control_file = os.path.join(debian_dir, "control")

    with open(control_file, "w") as f:
        # Source package stanza
        print(f"Source: cfbuild-{pkg_name.lower()}", file=f)
        print("Section: libs", file=f)
        print("Priority: optional", file=f)
        print("Maintainer: CFEngine Packager <cfengine@northern.tech>", file=f)
        print("Standards-Version: 4.7.0", file=f)
        print("Build-Depends: debhelper-compat (= 13)", file=f)

        print(file=f)  # Extra newline

        # Binary package stanza
        print(f"Package: cfbuild-{pkg_name.lower()}", file=f)
        print("Section: libs", file=f)
        print("Architecture: any", file=f)
        print(f"Description: CFEngine -- {pkg_name}", file=f)
        print(f" CFEngine Build Automation -- {pkg_name}", file=f)

        print(file=f)  # Extra newline

        # Developer binary package stanza
        print(f"Package: cfbuild-{pkg_name.lower()}-devel", file=f)
        print("Section: libdevel", file=f)
        print("Architecture: any", file=f)
        print(f"Description: CFEngine -- {pkg_name} -- development files", file=f)
        print(f" CFEngine Build Automation -- {pkg_name} -- development files", file=f)

    log.info(f"Created control file '{control_file}'")

def create_debian_install(pkg_name: str, pkg_version: str):
    target_dir = get_target_dir(pkg_name, pkg_version)
    debian_dir = get_debian_dir(target_dir)
    install_file = os.path.join(debian_dir, f"cfbuild-{pkg_name.lower()}.install")

    with open(install_file, "w") as f:
        print(f"/var/cfengine/lib/*", file=f)

def create_debian_devel_install(pkg_name: str, pkg_version: str):
    target_dir = get_target_dir(pkg_name, pkg_version)
    debian_dir = get_debian_dir(target_dir)
    install_file = os.path.join(debian_dir, f"cfbuild-{pkg_name.lower()}-devel.install")

    with open(install_file, "w") as f:
        print(f"/var/cfengine/lib/*", file=f)
        print(f"/var/cfengine/include/*", file=f)

def create_debian_copyright(pkg_name: str, pkg_version: str):
    """It is quite an important file, but for now we will be happy enough with an
    empty file."""

    target_dir = get_target_dir(pkg_name, pkg_version)
    debian_dir = get_debian_dir(target_dir)
    copyright_file = os.path.join(debian_dir, "copyright")

    with open(copyright_file, "w"):
        pass

    log.info(f"Created copyright file '{copyright_file}'")


def create_debian_rules(pkg_name, pkg_version):
    target_dir = get_target_dir(pkg_name, pkg_version)
    debian_dir = get_debian_dir(target_dir)
    rules_file = os.path.join(debian_dir, "rules")

    with open(rules_file, "w") as f:
        print("#!/usr/bin/make -f", file=f)
        print("%:", file=f)
        print("\tdh $@", file=f)
        print(file=f)

        print("override_dh_auto_configure:", file=f)
        print("\tdh_auto_configure -- --prefix=/var/cfengine --libdir=/var/cfengine/lib --enable-shared --disable-static", file=f)
        print(file=f)

        print("override_dh_auto_install:", file=f)
        print("\tdh_auto_install", file=f)
        print("\trm -f debian/tmp/var/cfengine/lib/*.la", file=f)

    log.info(f"Created rules file '{rules_file}'")


def create_debian_format(pkg_name, pkg_version):
    """The purpose of the source format file in Debian is to specify the format
    of a package and how it should be built."""

    target_dir = get_target_dir(pkg_name, pkg_version)
    debian_dir = get_debian_dir(target_dir)
    format_dir = os.path.join(debian_dir, "source")
    format_file = os.path.join(format_dir, "format")

    log.debug(f"Creating directory '{format_dir}'")
    os.mkdir(format_dir)

    with open(format_file, "w") as f:
        print("3.0 (quilt)", file=f)

    log.info(f"Created format file '{format_file}'")


def build_debian_package(pkg_name, pkg_version):
    target_dir = get_target_dir(pkg_name, pkg_version)
    sources_dir = get_sources_dir()
    log_file = os.path.join(sources_dir, f"cfbuild-{pkg_name}-debuild.log")

    log.info(
        f"Building debian package for target '{target_dir}' ..."
    )
    with open(log_file, "w") as f:
        res = subprocess.run(
            ["debuild", "-b", "-us", "-uc", "-rfakeroot"], cwd=target_dir, stdout=subprocess.DEVNULL, stderr=f
        )
    if res.returncode != 0:
        exit(1)


def prepare_debian_dir(pkg_name, pkg_version):
    target_dir = get_target_dir(pkg_name, pkg_version)
    debian_dir = get_debian_dir(target_dir)

    if os.path.exists(debian_dir):
        clean_debian_dir(debian_dir)
    else:
        log.debug(f"Creating directory '{debian_dir}'")
        os.makedirs(debian_dir, exist_ok=True)

    create_debian_changelog(pkg_name, pkg_version)
    create_debian_control(pkg_name, pkg_version)
    create_debian_copyright(pkg_name, pkg_version)
    create_debian_rules(pkg_name, pkg_version)
    create_debian_format(pkg_name, pkg_version)
    create_debian_install(pkg_name, pkg_version)
    create_debian_devel_install(pkg_name, pkg_version)
    build_debian_package(pkg_name, pkg_version)
