__version__ = "0.1.0"
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="test")
    args = parser.parse_args()
    return args


def main() -> None:
    print("gurka")
