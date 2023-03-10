import argparse
import examples

def parse_args():
    parser = argparse.ArgumentParser(description="CFEngine Hackaton")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debug messages",
    )

    subparsers = parser.add_subparsers(title="examples")

    select = subparsers.add_parser("select", help="select prompt example")
    select.add_argument("--question", default="How are you?", help="question to be prompted")
    select.add_argument("--choices", default=["Not good", "OK", "Very good"], nargs="+", help="choices to select from")
    select.set_defaults(func=lambda args: examples.select(args.question, args.choices))

    return parser.parse_args()
