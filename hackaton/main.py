import argparse
import logging as log


def parse_args():
    parser = argparse.ArgumentParser(description="CFEngine Hackaton")
    parser.add_argument(
        "--log",
        default="info",
        choices=["critical", "error", "warning", "info", "debug"],
        help="log level",
    )
    parser.add_argument(
        "--build-type",
        default="debug",
        choices=["release", "debug"],
        help="select build type",
    )
    parser.add_argument(
        "--project",
        default="community",
        choices=["community", "nova"],
        help="select edition",
    )
    parser.add_argument(
        "--role",
        default="agent",
        choices=["hub", "agent"],
        help="select package type",
    )
    parser.add_argument(
        "--work-dir",
        default="/var/cfengine",
        help="override CFEngine working directory",
    )
    parser.add_argument(
        "--version-string",
        help="set version string for binary/package",
    )
    parser.add_argument(
        "--core",
        default="master",
        help="select core branch",
    )
    parser.add_argument(
        "--enterprise",
        default="master",
        help="select enterprise branch",
    )
    parser.add_argument(
        "--nova",
        default="master",
        help="select nova branch",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    loglevel = log._nameToLevel[args.log.upper()]
    log.basicConfig(format="[%(filename)s:%(lineno)d][%(levelname)s]: %(message)s", level=loglevel)
    log.debug("Test")
