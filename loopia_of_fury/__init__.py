__version__ = "0.1.0"
import argparse
import sys
from typing import Optional, Sequence


def parse_args(
    argv: Optional[Sequence[str]] = sys.argv[1:],
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument(
        "--password",
    )

    args = parser.parse_args(args=argv)
    return args


def main() -> None:
    print("gurka")
