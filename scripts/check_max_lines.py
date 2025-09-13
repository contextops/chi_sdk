#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def count_lines(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--max-lines", type=int, default=600)
    args = ap.parse_args(argv)

    max_lines = args.max_lines
    violations: list[tuple[str, int]] = []
    for fn in args.files:
        p = Path(fn)
        if not p.exists():
            continue
        n = count_lines(p)
        if n > max_lines:
            violations.append((fn, n))

    if violations:
        print("Files exceeding max lines ({}):".format(max_lines))
        for fn, n in violations:
            print(f" - {fn}: {n} lines")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
