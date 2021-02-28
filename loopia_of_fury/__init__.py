import argparse
import importlib.metadata
import ipaddress
import os
import re
import sys
import urllib.request
from typing import Match, Optional, Sequence, Union

__version__ = importlib.metadata.version(__name__)



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
        help="Domain name to be updated, e.g: example.com",
    )
    parser.add_argument(
        "--subdomain",
        default="@",
        help="Subdomain name to be updated, e.g. smtp or www (default: %(default)s)",
    )
    parser.add_argument(
        "--record-type",
        default="A",
        help="DNS record to update, e.g. AAAA or CNAME (default: %(default)s)",
    )
    parser.add_argument(
        "--ip",
        help="IP address to update your DNS record to (default: find it via https://dyndns.loopia.se/checkip)",
    )
    parser.add_argument("--version", action="version", version=__version__)

    args = parser.parse_args(args=argv)
    if not args.password:
        parser.error("Password is required: ({!r})".format(args.password))
    return args


def loopia_find_ip(response: str) -> Optional[str]:
    match: Optional[Match[str]] = re.match(r".*: ([\d\.]*?)<.*", response)
    ip_found = None
    if match:
        ip_found = match.group(1)
    return ip_found


def get_ip() -> Union[None, ipaddress.IPv6Address, ipaddress.IPv4Address]:
    ip: Union[None, ipaddress.IPv6Address, ipaddress.IPv4Address] = None
    response = None
    request = urllib.request.urlopen(
        urllib.request.Request(
            "https://dyndns.loopia.se/checkip",
            headers={
                "User-Agent": "{}/{} (+{})".format(
                    __name__,
                    __version__,
                    importlib.metadata.metadata(__name__).get("Home-page"),
                )
            },
        )
    )
    response = request.read().decode("utf-8")
    ip_found = loopia_find_ip(response)

    try:
        ip = ipaddress.ip_address(ip_found)
    except ipaddress.AddressValueError as e:
        return None
    return ip


def main() -> None:
    args = parse_args()
    print("gurka")
