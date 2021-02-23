import argparse
import ipaddress
import os
import sys
from typing import Optional, Sequence, Union

import pkg_resources

__version__ = pkg_resources.get_distribution(__name__).version


def parse_args(
    argv: Optional[Sequence[str]] = sys.argv[1:],
) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
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
    parser.add_argument("--version", action="version", version=__version__)

    args = parser.parse_args(args=argv)
    if not args.password:
        parser.error("Password is required: ({!r})".format(args.password))
    return args


def get_ip() -> Union[None, ipaddress.IPv6Address, ipaddress.IPv4Address]:
    ip: Union[None, ipaddress.IPv6Address, ipaddress.IPv4Address] = None
    try:
        ip = ipaddress.ip_address("2001:DB8::1")
    except ipaddress.AddressValueError as e:
        return None
    return ip


def main() -> None:
    args = parse_args()
    print("gurka")
