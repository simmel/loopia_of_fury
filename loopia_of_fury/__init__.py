__version__ = "0.1.0"
import argparse
import os
import sys
from typing import Optional, Sequence


def parse_args(
    argv: Optional[Sequence[str]] = sys.argv[1:],
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument(
        "--password",
        default=os.getenv("LOOPIA_PASSWORD"),
        help="You can also set the password via the environment variable LOOPIA_PASSWORD",
    )

    args = parser.parse_args(args=argv)
    return args


def main() -> None:
    args = parse_args()
    print("gurka")
