from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path

from . import binary_path


def main() -> int:
    bin_path: Path = binary_path()
    if not bin_path.exists():
        sys.stderr.write(
            "chi-tui binary not found in package. This wheel may have been built without bundling the binary for your platform.\n"
        )
        sys.stderr.write(
            "If running from a development checkout, build the Rust TUI and place it under chi_sdk/bin/.\n"
        )
        return 127

    # Ensure executable bit on POSIX (safety)
    try:
        if os.name == "posix":
            mode = os.stat(bin_path).st_mode
            os.chmod(bin_path, mode | 0o111)
    except Exception:
        pass

    env = os.environ.copy()
    # Do not force CHI_APP_BIN here; wrappers or config should set it.
    try:
        # Use exec on POSIX for better signal handling; subprocess on Windows
        if os.name == "posix":
            os.execv(str(bin_path), [str(bin_path), *sys.argv[1:]])
            return 0  # not reached
        else:
            return subprocess.call([str(bin_path), *sys.argv[1:]], env=env)
    except FileNotFoundError:
        sys.stderr.write("Failed to execute chi-tui binary.\n")
        return 127


if __name__ == "__main__":
    raise SystemExit(main())
