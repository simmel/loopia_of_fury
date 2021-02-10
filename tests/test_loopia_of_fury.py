from loopia_of_fury import __version__, argparse, parse_args


def test_version():
    assert __version__ == "0.1.0"


def test_args_parse():
    args = parse_args()
    assert type(args) == argparse.Namespace
