"""Command line front end for the wordcount package."""

from __future__ import annotations

import argparse
import sys

from .core import Report


def main(argv=None):
    parser = argparse.ArgumentParser(prog="wordcount")
    parser.add_argument("path", nargs="?", help="file to analyse (default: stdin)")
    parser.add_argument("-n", "--top", type=int, default=5)
    args = parser.parse_args(argv)

    if args.path:
        with open(args.path, encoding="utf-8") as handle:
            text = handle.read()
    else:
        text = sys.stdin.read()

    report = Report.build(text, limit=args.top)
    print("total words   {}".format(report.total_words))
    print("unique words  {}".format(report.unique_words))
    print("density       {}".format(report.lexical_density))
    for word, count in report.top:
        print("  {:>5}  {}".format(count, word))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
