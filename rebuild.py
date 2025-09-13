#!/usr/bin/env python3
"""
Rebuild helper for this repo.

Actions:
- Build Rust TUI binary (debug or --release)
- Optionally install Python packages in editable mode (--install)
- Copy the built `chi-tui` binary into the example app's `.tui/bin/`

Usage:
  ./rebuild.py [--release] [--install]
"""

from __future__ import annotations

import argparse
import shutil
import stat
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
RUST_TUI = REPO_ROOT / "rust-tui"
EXAMPLE_APP = REPO_ROOT / "example-apps" / "example-app"
EXAMPLE_BIN_DIR = EXAMPLE_APP / ".tui" / "bin"


def run(
    cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None
) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def build_rust(release: bool) -> Path:
    profile = "release" if release else "debug"
    cmd = ["cargo", "build"] + (["--release"] if release else [])
    run(cmd, cwd=RUST_TUI)
    exe = "chi-tui.exe" if sys.platform == "win32" else "chi-tui"
    built = RUST_TUI / "target" / profile / exe
    if not built.exists():
        raise FileNotFoundError(f"Built binary not found: {built}")
    return built


def ensure_executable(p: Path) -> None:
    if sys.platform != "win32":
        mode = p.stat().st_mode
        p.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def copy_binary(src: Path, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)
    ensure_executable(dest)
    print(f"Copied: {src} -> {dest}")
    return dest


def install_python() -> None:
    # Install local SDK and example app in editable mode using current interpreter
    run([sys.executable, "-m", "pip", "install", "-U", "pip"])
    run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-e",
            str(REPO_ROOT / "python-chi-sdk"),
            "-e",
            str(EXAMPLE_APP),
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--release", action="store_true", help="Build Rust TUI in release mode"
    )
    ap.add_argument(
        "--install",
        action="store_true",
        help="Install python-chi-sdk and example-app in editable mode",
    )
    args = ap.parse_args()

    # Optionally install Python deps
    if args.install:
        install_python()

    # Build Rust and copy into example app's .tui/bin
    built = build_rust(args.release)
    copy_binary(built, EXAMPLE_BIN_DIR)

    print("\nDone.")
    print("Next:")
    print("  - Run ./run.py to launch the TUI")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}", file=sys.stderr)
        raise
