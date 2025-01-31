import os
import json
import logging as log
from utils import get_build_dir
from context import check_context


def get_tarballs_dir():
    build_dir = get_build_dir()
    return os.path.join(build_dir, "tarballs")

def fetch_tarball(ctx, pkg_name, pkg_info):
    pass

def package_dependencies(ctx):
    tarballs_dir = get_tarballs_dir()
    log.debug(f"Creating directory '{tarballs_dir}'")
    os.makedirs(tarballs_dir, exist_ok=True)

    with open("deps-packaging.json", "r") as f:
        deps = json.load(f)

    for pkg_name, pkg_info in deps.items():
        expr = pkg_info.get("expression", "any")
        if expr and not check_context(ctx, expr):
            log.debug(f"Skipping dependency {pkg_name}: Not in context")
            continue

