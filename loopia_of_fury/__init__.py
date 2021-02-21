__version__ = "0.1.0"
import argparse
import ipaddress
import os
import sys
from typing import Optional, Sequence, Union


def parse_args(
    argv: Optional[Sequence[str]] = sys.argv[1:],
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument(
        "--username",
        required=True,
    )
    parser.add_argument(
        "--password",
        default=os.getenv("LOOPIA_PASSWORD"),
        help="You can also set the password via the environment variable LOOPIA_PASSWORD",
    )
    parser.add_argument(
        "--domain",
        required=True,
    )
    parser.add_argument(
        "--subdomain",
        default="@",
    )
    parser.add_argument(
        "--record-type",
        default="A",
    )
    parser.add_argument(
        "--ip",
    )

    args = parser.parse_args(args=argv)
    if not args.password:
        parser.error("Password is required: ({!r})".format(args.password))
    return args


def get_ip() -> Optional[Union[ipaddress.IPv4Address, ipaddress.IPv6Address]]:
    return None


def main() -> None:
    args = parse_args()
    print("gurka")
