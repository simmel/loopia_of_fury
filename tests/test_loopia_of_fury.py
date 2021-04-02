import ipaddress
import os
import urllib
import xmlrpc.client

import loopia_of_fury
import pytest
from loopia_of_fury import (__version__, argparse, check_results, get_ip,
                            get_zonerecords, parse_args, update_zonerecords)


class MockResponse:
    def __init__(self, *, data):
        self.data = data

    def read(self):
        return self.data

    def close(self):
        pass


def test_version():
    assert __version__ == "0.1.0"


def test_args_password_none():
    with pytest.raises(SystemExit) as e:
        args = parse_args()
    assert e.type == SystemExit
    assert e.value.code == 2


def test_args_required():
    username = "arg-username"
    password = "arg-password"
    domain = "arg-domain"
    args = parse_args(
        argv=["--username", username, "--password", password, "--domain", domain]
    )
    assert args.username == username
    assert args.password == password
    assert args.domain == domain


def test_args_password_env(monkeypatch):
    password = "env-password"
    monkeypatch.setenv("LOOPIA_PASSWORD", password)
    args = parse_args(argv=["--username", "arg-username", "--domain", "arg-domain"])
    assert args.password == password


@pytest.mark.parametrize(
    "provided,expected", [("arg-subdomain", "arg-subdomain"), (None, "@")]
)
def test_args_subdomain(provided, expected):
    argv = [
        "--username",
        "arg-username",
        "--password",
        "arg-password",
        "--domain",
        "arg-domain",
    ]
    if provided:
        argv.extend(
            [
                "--subdomain",
                provided,
            ]
        )
    args = parse_args(argv=argv)
    assert args.subdomain == expected


@pytest.mark.parametrize(
    "provided,expected", [("arg-record-type", "arg-record-type"), (None, "A")]
)
def test_args_record_type(provided, expected):
    argv = [
        "--username",
        "arg-username",
        "--password",
        "arg-password",
        "--domain",
        "arg-domain",
    ]
    if provided:
        argv.extend(
            [
                "--record-type",
                provided,
            ]
        )
    args = parse_args(argv=argv)
    assert args.record_type == expected


@pytest.mark.parametrize(
    "provided,expected",
    [
        ("192.0.2.1", ipaddress.ip_address("192.0.2.1")),
        ("2001:db8::1", ipaddress.ip_address("2001:db8::1")),
        (None, None),
        ("gurka", Exception),
    ],
)
def test_args_ip(provided, expected):
    argv = [
        "--username",
        "arg-username",
        "--password",
        "arg-password",
        "--domain",
        "arg-domain",
    ]
    if provided:
        argv.extend(
            [
                "--ip",
                provided,
            ]
        )
    if expected is Exception:
        with pytest.raises(SystemExit) as e:
            args = parse_args(argv=argv)

    else:
        args = parse_args(argv=argv)
        assert args.ip == expected


@pytest.mark.parametrize(
    "provided,expected",
    [
        ("192.0.2.1", ipaddress.ip_address("192.0.2.1")),
        ("2001:db8::1", ipaddress.ip_address("2001:db8::1")),
    ],
)
def test_get_ip(monkeypatch, provided, expected):
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda _a: MockResponse(data=provided.encode("utf-8")),
    )
    monkeypatch.setattr(
        loopia_of_fury,
        "loopia_find_ip",
        lambda a: a,
    )
    assert get_ip() == expected


def test_get_zonerecords(monkeypatch):
    monkeypatch.setattr(
        xmlrpc.client.ServerProxy,
        "__getattr__",
        lambda _a, _b: lambda _u, _p, _d, _s: [
            {
                "ttl": 3600,
                "record_id": 1337,
                "type": "A",
                "priority": 0,
                "rdata": "192.0.2.1",
            }
        ],
    )
    argv = [
        "--username",
        "arg-username",
        "--password",
        "arg-password",
        "--domain",
        "arg-domain",
    ]
    args = parse_args(argv=argv)
    client = xmlrpc.client.ServerProxy(uri="https://soy.se")
    zone_records = get_zonerecords(client=client, args=args)

    assert type(zone_records) == list
    assert type(zone_records[0]) == dict
    assert all(
        key in zone_records[0]
        for key in ["ttl", "record_id", "type", "priority", "rdata"]
    )


@pytest.mark.parametrize(
    "ip_provided,ip_expected,record_type_provided,record_type_expected,result_provided,result_expected",
    [
        ("192.0.2.1", "192.0.2.2", "A", "A", "OK", "OK"),
        ("2001:db8::1", "2001:db8::2", "AAAA", "AAAA", "OK", "OK"),
        ("2001:db8::1", "192.0.2.2", "AAAA", "AAAA", "UNKNOWN_ERROR", "UNKNOWN_ERROR"),
        ("192.0.2.2", "2001:db8::1", "A", "A", "UNKNOWN_ERROR", "UNKNOWN_ERROR"),
    ],
)
def test_update_zonerecords(
    monkeypatch,
    ip_provided,
    ip_expected,
    record_type_provided,
    record_type_expected,
    result_provided,
    result_expected,
):
    record = [
        {
            "ttl": 3600,
            "record_id": 1337,
            "type": record_type_provided,
            "priority": 0,
            "rdata": ip_provided,
        }
    ]
    monkeypatch.setattr(
        xmlrpc.client.ServerProxy,
        "__getattr__",
        lambda _a, _b: lambda _u, _p, _d, _s, zone_record: result_provided,
    )
    argv = [
        "--username",
        "arg-username",
        "--password",
        "arg-password",
        "--domain",
        "arg-domain",
        "--ip",
        ip_expected,
        "--record-type",
        record_type_expected,
    ]
    args = parse_args(argv=argv)
    client = xmlrpc.client.ServerProxy(uri="https://soy.se")
    results = update_zonerecords(client=client, args=args, zone_records=record)

    result = results[record[0]["record_id"]]

    assert result["result"] == result_expected
    assert result["zone_record"]["rdata"] == ip_expected
    assert result["zone_record"]["type"] == record_type_expected


@pytest.mark.parametrize(
    "provided,expected",
    [
        (["OK", "OK"], True),
        (["OK", "UNKNOWN_ERROR"], False),
        (["AUTH_ERROR", "OK"], False),
        (["OK", "BAD_INDATA"], False),
    ],
)
def test_check_results(
    provided,
    expected,
):
    results = {}
    for i in range(len(provided)):
        results[i] = {
            "zone_record": {},
            "result": provided[i],
        }

    result = check_results(results)

    assert result == expected
