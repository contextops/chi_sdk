"""Utility functions for CHI admin commands."""

import os
import platform
import stat
from pathlib import Path


def _ensure_executable(p: Path) -> None:
    try:
        if os.name == "posix":
            p.chmod(p.stat().st_mode | stat.S_IXUSR)
    except Exception:
        pass


def _user_cache_dir() -> Path:
    sysname = platform.system().lower()
    home = Path.home()
    if sysname == "darwin":
        return home / "Library" / "Caches" / "chi-tui"
    if sysname == "windows":
        base = os.environ.get("LOCALAPPDATA") or str(home / "AppData" / "Local")
        return Path(base) / "chi-tui"
    # linux and others
    return Path(os.environ.get("XDG_CACHE_HOME", str(home / ".cache"))) / "chi-tui"


def _cache_bin_path() -> Path:
    return _user_cache_dir() / "bin"
