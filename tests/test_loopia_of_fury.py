import os

import pytest
from loopia_of_fury import __version__, argparse, parse_args


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
    envs = {"LOOPIA_PASSWORD": password}
    monkeypatch.setattr(os, "environ", envs)
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
    "provided,expected", [("192.0.2.1", "192.0.2.1"), (None, None)]
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
    args = parse_args(argv=argv)
    assert args.ip == expected
