import argparse
import ipaddress
import os
import re
import sys
import urllib.request
import xmlrpc.client
from typing import Any, Match, Optional, Sequence, Union

import pkg_resources

__metadata__ = {
    i[0]: i[1]
    for i in [
        a.split(": ")
        for a in pkg_resources.get_distribution("loopia_of_fury")
        .get_metadata("METADATA")
        .rstrip()
        .split("\n")
    ]
}
__version__ = __metadata__["Version"]

API_SERVER = "https://api.loopia.se/RPCSERV"


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

    def ip_address(
        ip: str,
    ) -> Union[None, ipaddress.IPv6Address, ipaddress.IPv4Address]:
        parsed_ip: Union[None, ipaddress.IPv6Address, ipaddress.IPv4Address] = None
        try:
            parsed_ip = ipaddress.ip_address(ip)
        except Exception as e:
            raise argparse.ArgumentTypeError(e)
        return parsed_ip

    parser.add_argument(
        "--ip",
        type=ip_address,
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
                    __metadata__["Home-page"],
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


def get_zonerecords(
    *, client: xmlrpc.client.ServerProxy, args: argparse.Namespace
) -> Any:
    zone_records = client.getZoneRecords(
        args.username, args.password, args.domain, args.subdomain
    )
    return zone_records


def main() -> None:
    args = parse_args()
    print("gurka")
