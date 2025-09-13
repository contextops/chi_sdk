#!/usr/bin/env python3
"""
Run helper for this repo.

Launches the example app TUI from the correct directory, ensuring the
freshly built chi-tui binary (under .tui/bin) is on PATH. This avoids
needing a global install during development.

Usage:
  ./run.py [--headless] [--ticks N] [--enter-id ID]
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
EXAMPLE_APP = REPO_ROOT / "example-apps" / "example-app"
EXAMPLE_SRC = EXAMPLE_APP / "src"
SDK_SRC = REPO_ROOT / "python-chi-sdk" / "src"


def run() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--headless", action="store_true", help="Run TUI in headless smoke mode"
    )
    ap.add_argument(
        "--ticks", type=int, default=15, help="Headless ticks (default: 15)"
    )
    ap.add_argument(
        "--enter-id",
        dest="enter_id",
        default=None,
        help="Headless: menu id to auto-enter (e.g., paginated_list)",
    )
    args = ap.parse_args()

    env = os.environ.copy()

    # Ensure .tui/bin is on PATH to pick up local chi-tui built by rebuild.py
    bin_dir = str(EXAMPLE_APP / ".tui" / "bin")
    env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")

    # Support headless smoke
    if args.headless:
        env["CHI_TUI_HEADLESS"] = "1"
        env["CHI_TUI_TICKS"] = str(args.ticks)
        if args.enter_id:
            env["CHI_TUI_HEADLESS_ENTER_ID"] = args.enter_id

    # Prefer module execution to avoid requiring pip install -e
    # Prefer the console script if available (in local .venv or PATH)
    exe = "example-app.exe" if sys.platform == "win32" else "example-app"
    candidates = [
        REPO_ROOT / ".venv" / ("Scripts" if sys.platform == "win32" else "bin") / exe,
        Path(exe),
    ]
    for cand in candidates:
        if cand.exists():
            cmd = [str(cand), "ui"]
            print("$", " ".join(cmd), f"(cwd={EXAMPLE_APP})")
            return subprocess.call(cmd, cwd=str(EXAMPLE_APP), env=env)

    # Fallback: run via Python with local sources on PYTHONPATH (requires console script not to be used)
    extra_paths = [str(SDK_SRC), str(EXAMPLE_SRC)]
    env["PYTHONPATH"] = os.pathsep.join(extra_paths + [env.get("PYTHONPATH", "")])
    cmd = [sys.executable, "-c", "import example_app.cli as m; m.cli()", "ui"]
    print("$", " ".join(cmd), f"(cwd={EXAMPLE_APP})")
    return subprocess.call(cmd, cwd=str(EXAMPLE_APP), env=env)


if __name__ == "__main__":
    raise SystemExit(run())
