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
    from the changelog: most importantly, the package version."""

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

    # The above should produce the same output as the following command.
    f"debchange --create --package {pkg_name} --newversion {pkg_version} --urgency low --empty"
    # Check out `man debchange`` for more info.


def create_debian_control(pkg_name: str, pkg_version: str):
    """The control file describes the source and binary package, and gives some
    information about them, such as their names, who the package maintainer is,
    and so on."""

    target_dir = get_target_dir(pkg_name, pkg_version)
    debian_dir = get_debian_dir(target_dir)
    control_file = os.path.join(debian_dir, "control")

    with open(control_file, "w") as f:
        #########################################
        # Source package stanza
        #########################################

        # The source package name
        print(f"Source: cfbuild-{pkg_name.lower()}", file=f)
        print("Section: libs", file=f)
        # The priority of the package (one of 'required', 'important',
        # 'standard' or 'optional'). In general, a package is 'optional' unless
        # it's 'essential' for a standard functioning system, i.e., booting or
        # networking functionality.
        print("Priority: optional", file=f)
        # The name and e-mail address of the person responsible for the package.
        # We will put the blame on Mr. CFEngine Packager.
        print("Maintainer: CFEngine Packager <cfengine@northern.tech>", file=f)
        print("Standards-Version: 4.7.0", file=f)
        # The list of packages that need to be installed to build the package.
        # They might or might not be needed to actually use the package.
        print("Build-Depends: debhelper-compat (= 13)", file=f)

        print(file=f)  # Extra newline

        #########################################
        # Binary package stanza
        #########################################

        # The name of the binary package. The name might be different from the
        # source package name.
        print(f"Package: cfbuild-{pkg_name.lower()}", file=f)
        print("Section: libs", file=f)
        # Specifies which computer architectures the binary package is expected
        # to work on. "any" means that the package can be built for any
        # architecture. "all" means that the same package will work on all
        # architectures. For example, a package consisting only of shell scripts
        # would be "all".
        print("Architecture: any", file=f)
        # The full description of the binary package. It is meant to be helpful
        # to users. The first line is used as the short synopsis (summary)
        # description, and the rest of the description must be an independent
        # longer description of the package.
        print(f"Description: CFEngine Build Automation -- {pkg_name}", file=f)
        print(f" CFEngine Build Automation -- {pkg_name}", file=f)

        print(file=f)  # Extra newline

        #########################################
        # Developer binary package stanza
        #########################################

        print(f"Package: cfbuild-{pkg_name.lower()}-devel", file=f)
        print("Section: libdevel", file=f)
        print("Architecture: any", file=f)
        print(
            f"Description: CFEngine Build Automation -- {pkg_name} -- development files",
            file=f,
        )
        print(f" CFEngine Build Automation -- {pkg_name} -- development files", file=f)

    log.info(f"Created control file '{control_file}'")


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

    log.info(f"Created rules file '{rules_file}'")


def create_debian_format(pkg_name, pkg_version):
    """The final file we need is debian/source/format, and it should contain the
    version number for the format of the source package, which is "3.0 (quilt)".
    """

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
        f"Patience my friend: Building debian package for target '{target_dir}' ..."
    )
    with open(log_file, "w") as f:
        res = subprocess.run(
            ["debuild", "-us", "-uc"], cwd=target_dir, stdout=f, stderr=f
        )
    if res.returncode != 0:
        log.error(
            f"Failed to build package for target '{target_dir}': See '{log_file}' for logs"
        )
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
    build_debian_package(pkg_name, pkg_version)
