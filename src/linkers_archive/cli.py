"""Simple CLI entrypoint for linkers-archive"""

import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="linkers-archive")
    parser.add_argument("--version", action="store_true", help="Show package version")
    args = parser.parse_args(argv)

    if args.version:
        from . import __version__

        print(__version__)
