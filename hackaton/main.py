import logging as log
from args import parse_args
from context import get_context
from deps_packaging import package_dependencies


def main():
    args = parse_args()
    loglevel = "DEBUG" if args.debug else "INFO"
    log.basicConfig(
        format="[%(filename)s:%(lineno)d][%(levelname)s]: %(message)s", level=loglevel
    )

    ctx = get_context(args)
    package_dependencies(ctx)
