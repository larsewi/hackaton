import argparse
import logging as log


def parse_args():
    parser = argparse.ArgumentParser(description="CFEngine Hackaton")
    parser.add_argument(
        "--log",
        default="info",
        choices=["critical", "error", "warning", "info", "debug"],
        help="select log level",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    loglevel = log._nameToLevel[args.log.upper()]
    log.basicConfig(format="%(levelname)8s: %(message)s", level=loglevel)
