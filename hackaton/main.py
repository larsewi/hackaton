import logging as log
from arguments import parse_args



def main():
    args = parse_args()
    log.basicConfig(
        format="%(levelname)8s: %(message)s",
        level=log.DEBUG if args.debug else log.INFO,
    )
    args.func(args)
