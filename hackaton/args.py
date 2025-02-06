import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="CFEngine Hackaton")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debug log messages",
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
        choices=["community", "enterprise"],
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
        help="specify CFEngine working directory",
    )
    parser.add_argument(
        "--package-version",
        help="set version string for binary/package",
    )
    parser.add_argument(
        "--core",
        default="core",
        help="specify path to core directory",
    )
    parser.add_argument(
        "--enterprise",
        default="enterprise",
        help="specify path to master directory",
    )
    parser.add_argument(
        "--nova",
        default="master",
        help="specify path to nova directory",
    )
    return parser.parse_args()
