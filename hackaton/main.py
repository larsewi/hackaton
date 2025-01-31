import logging as log
from args import parse_args


def main():
    args = parse_args()
    loglevel = "DEBUG" if args.debug else "INFO"
    log.basicConfig(format="[%(filename)s:%(lineno)d][%(levelname)s]: %(message)s", level=loglevel)
    log.debug("Test")
