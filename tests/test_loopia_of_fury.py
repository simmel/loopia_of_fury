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


def test_args_password_arg():
    password = "arg-password"
    args = parse_args(argv=["--password", password])
    assert args.password == password


def test_args_password_env(monkeypatch):
    password = "env-password"
    envs = {"LOOPIA_PASSWORD": password}
    monkeypatch.setattr(os, "environ", envs)
    args = parse_args()
    assert args.password == password
