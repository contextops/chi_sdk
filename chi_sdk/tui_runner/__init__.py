from __future__ import annotations

from importlib.resources import files
from pathlib import Path
import platform


def binary_name() -> str:
    return "chi-tui.exe" if platform.system().lower().startswith("win") else "chi-tui"


def binary_path() -> Path:
    # Binary is now in chi_sdk/bin/
    base = files("chi_sdk") / "bin" / binary_name()
    return Path(str(base))
