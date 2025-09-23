"""Simple CLI entrypoint for linkers-archive"""

from __future__ import annotations

import argparse
from typing import Iterable, Optional


def _cmd_version() -> int:
    from . import __version__

    print(__version__)
    return 0


def _cmd_echo(message: str) -> int:
    print(message)
    return 0


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="linkers-archive")
    subparsers = parser.add_subparsers(dest="command")

    # version subcommand (keeps backward compatible --version flag)
    parser.add_argument("--version", action="store_true", help="Show package version")
    subparsers.add_parser("version", help="Show package version")

    # echo subcommand
    echo_parser = subparsers.add_parser("echo", help="Echo a message")
    echo_parser.add_argument("message", help="Message to echo")

    args = parser.parse_args(list(argv) if argv is not None else None)

    # backward-compatible flag
    if getattr(args, "version", False):
        return _cmd_version()

    if args.command == "version":
        return _cmd_version()

    if args.command == "echo":
        return _cmd_echo(args.message)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
