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

    select = subparsers.add_parser("select", help="selection prompt example")
    select.add_argument("--prompt", default="What's the greatest programming language?", help="selection prompt")
    select.add_argument("--choices", default=["Python", "JavaScipt", "Java", "C#", "C", "C++", "Go", "R", "Swift", "PHP"], nargs="+", help="choices to select from")
    select.set_defaults(func=lambda args: examples.select(args.prompt, args.choices))

    return parser.parse_args()
