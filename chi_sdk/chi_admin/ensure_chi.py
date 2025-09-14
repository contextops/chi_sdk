"""Ensure CHI TUI binary is available - compile or download."""
import json
import os
import platform
import shutil
import subprocess
import tarfile
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional, Dict, Any

import click

from ..sdk import emit_error, emit_ok
from .utils import _ensure_executable


def _json_mode(ctx: Optional[click.Context] = None) -> bool:
    ctx = ctx or click.get_current_context(silent=True)
    env = os.getenv("CHI_TUI_JSON", "")
    return bool(
        (ctx and ctx.obj and ctx.obj.get("json")) or env in ("1", "true", "yes")
    )


def _which(prog: str) -> Optional[str]:
    return shutil.which(prog)


def _get_user_bin_dir() -> Path:
    """Get user bin directory for installing executables."""
    sysname = platform.system().lower()
    home = Path.home()

    if sysname == "windows":
        # Windows: use %LOCALAPPDATA%\Programs\chi-sdk
        base = os.environ.get("LOCALAPPDATA") or str(home / "AppData" / "Local")
        return Path(base) / "Programs" / "chi-sdk"
    else:
        # Unix-like: use ~/.local/bin
        return home / ".local" / "bin"


def _get_chi_sdk_bin_dir() -> Path:
    """Get chi_sdk package bin directory."""
    import chi_sdk

    sdk_path = Path(chi_sdk.__file__).parent
    return sdk_path / "bin"


def _get_chi_sdk_sources_dir() -> Optional[Path]:
    """Get chi_sdk sources directory - check multiple locations."""
    # 1. Check current working directory for rust-tui (dev environment)
    cwd = Path.cwd()
    rust_tui_dir = cwd / "rust-tui"
    if rust_tui_dir.exists() and (rust_tui_dir / "Cargo.toml").exists():
        return rust_tui_dir

    # 2. Check parent directories (in case we're in a subdirectory)
    for parent in cwd.parents[:3]:  # Check up to 3 levels up
        rust_tui_dir = parent / "rust-tui"
        if rust_tui_dir.exists() and (rust_tui_dir / "Cargo.toml").exists():
            return rust_tui_dir

    # 3. Check if chi_sdk is installed in editable mode
    import chi_sdk

    sdk_path = Path(chi_sdk.__file__).parent

    # For editable installs, check multiple possible repo locations
    # Pattern: python-chi-sdk/src/chi_sdk -> need to go to repo root
    possible_repos = [
        sdk_path.parent.parent.parent,  # chi_sdk repo root (from python-chi-sdk/src/chi_sdk)
        sdk_path.parent.parent,  # python-chi-sdk root
        sdk_path.parent,  # src root (unlikely but check)
    ]

    for repo in possible_repos:
        rust_tui_dir = repo / "rust-tui"
        if rust_tui_dir.exists() and (rust_tui_dir / "Cargo.toml").exists():
            return rust_tui_dir

    # 4. Check for sources installed via pip install chi_sdk[sources]
    sources_dir = sdk_path / "chi-tui-sources"
    if sources_dir.exists():
        return sources_dir

    return None


def _compile_from_sources(sources_dir: Path, target_dir: Path) -> bool:
    """Compile chi-tui from Rust sources."""
    # Check if cargo is available
    if not _which("cargo"):
        return False

    try:
        # Create target directory
        target_dir.mkdir(parents=True, exist_ok=True)

        # Run cargo build
        result = subprocess.run(
            ["cargo", "build", "--release"],
            cwd=sources_dir,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes timeout
        )

        if result.returncode != 0:
            return False

        # Find the compiled binary
        release_dir = sources_dir / "target" / "release"
        binary_name = "chi-tui.exe" if os.name == "nt" else "chi-tui"
        compiled_binary = release_dir / binary_name

        if not compiled_binary.exists():
            # Try without extension on Windows too
            compiled_binary = release_dir / "chi-tui"
            if not compiled_binary.exists():
                return False

        # Copy to target directory
        target_binary = target_dir / binary_name
        shutil.copy2(compiled_binary, target_binary)
        _ensure_executable(target_binary)

        return True
    except Exception:
        return False


def _download_binary(target_dir: Path) -> bool:
    """Download chi-tui binary from GitHub releases."""
    owner_repo = os.environ.get("CHI_TUI_GH_REPO", "contextops/chi_tui")
    tag = os.environ.get("CHI_TUI_BIN_TAG")  # if not set, use latest

    def _fetch_json(url: str):
        req = urllib.request.Request(
            url, headers={"Accept": "application/vnd.github+json"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))

    try:
        if tag:
            rel = _fetch_json(
                f"https://api.github.com/repos/{owner_repo}/releases/tags/{tag}"
            )
        else:
            # Get all releases (including pre-releases) and pick the first one
            releases = _fetch_json(
                f"https://api.github.com/repos/{owner_repo}/releases"
            )
            if not releases:
                return False
            rel = releases[0]  # GitHub returns them sorted by created_at desc
    except Exception:
        return False

    assets = rel.get("assets", [])
    sysname = platform.system().lower()
    # mach = platform.machine().lower()

    # Determine platform and architecture
    machine = platform.machine().lower()
    arch = "arm64" if machine in ("aarch64", "arm64") else "amd64"

    def _match_asset(asset_name: str) -> bool:
        n = asset_name.lower()
        if not n.startswith("chi-tui"):
            return False

        # Check for architecture match
        if arch == "arm64" and "arm64" not in n and "aarch64" not in n:
            return False
        if arch == "amd64" and "arm64" not in n and "aarch64" not in n:
            # For amd64, we want assets without arm64
            pass

        # Check for OS match
        if sysname == "windows":
            return ("windows" in n or "win" in n) and n.endswith(".zip")
        if sysname == "darwin":
            return ("macos" in n or "darwin" in n) and n.endswith(".tar.gz")
        # Linux
        return "linux" in n and n.endswith(".tar.gz")

    # Find matching asset
    asset = next((a for a in assets if _match_asset(a.get("name", ""))), None)
    if not asset:
        return False

    url = asset.get("browser_download_url")
    if not url:
        return False

    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)

    # Download and extract binary
    binary_name = "chi-tui.exe" if os.name == "nt" else "chi-tui"
    target = target_dir / binary_name

    try:
        # Download to temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            with urllib.request.urlopen(url, timeout=60) as resp:
                shutil.copyfileobj(resp, tmp_file)
            tmp_path = tmp_file.name

        # Extract based on file type
        asset_name = asset.get("name", "").lower()
        if asset_name.endswith(".zip"):
            with zipfile.ZipFile(tmp_path, 'r') as z:
                # Find chi-tui binary in the archive
                for name in z.namelist():
                    # On Windows, look for .exe; on others, look for chi-tui without extension
                    if os.name == "nt":
                        if name.endswith("chi-tui.exe") or name == "chi-tui.exe":
                            with z.open(name) as src, open(target, "wb") as dst:
                                shutil.copyfileobj(src, dst)
                            break
                    else:
                        if (name.endswith("chi-tui") and not name.endswith(".exe")) or name == "chi-tui":
                            with z.open(name) as src, open(target, "wb") as dst:
                                shutil.copyfileobj(src, dst)
                            break
        elif asset_name.endswith(".tar.gz"):
            with tarfile.open(tmp_path, 'r:gz') as t:
                # Find chi-tui binary in the archive
                for member in t.getmembers():
                    if member.name.endswith("chi-tui") or member.name == "chi-tui":
                        with t.extractfile(member) as src, open(target, "wb") as dst:
                            shutil.copyfileobj(src, dst)
                        break

        # Clean up temp file
        os.unlink(tmp_path)

        # Make executable
        _ensure_executable(target)
        return True
    except Exception:
        return False


def _install_to_user_bin(source_binary: Path) -> Optional[Path]:
    """Install binary to user bin directory."""
    user_bin = _get_user_bin_dir()
    user_bin.mkdir(parents=True, exist_ok=True)

    binary_name = source_binary.name
    target = user_bin / binary_name

    try:
        # Copy or create symlink
        if platform.system().lower() != "windows":
            # On Unix, create symlink if possible
            if target.exists() or target.is_symlink():
                target.unlink()
            target.symlink_to(source_binary)
        else:
            # On Windows, copy the file
            shutil.copy2(source_binary, target)
            _ensure_executable(target)

        return target
    except Exception:
        return None


def _check_path_contains(directory: Path) -> bool:
    """Check if directory is in PATH."""
    path_env = os.environ.get("PATH", "")
    paths = path_env.split(os.pathsep)
    dir_str = str(directory)
    return any(os.path.normpath(p) == os.path.normpath(dir_str) for p in paths)


def _add_to_user_path(directory: Path) -> bool:
    """Attempt to add a directory to the user's PATH persistently.

    Currently implemented for Windows (updates HKCU\\Environment\\Path and broadcasts
    the change). Returns True if the path is already present or was added
    successfully; False on failure or if not supported on this platform.
    """
    try:
        if platform.system().lower() == "windows":
            try:
                import winreg  # type: ignore
            except Exception:
                return False

            target = str(directory)

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                "Environment",
                0,
                winreg.KEY_READ | winreg.KEY_SET_VALUE,
            )
            try:
                current_value, value_type = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current_value, value_type = "", winreg.REG_EXPAND_SZ

            current_value = current_value or ""
            parts = [p for p in current_value.split(";") if p]

            def _norm(p: str) -> str:
                return os.path.normcase(os.path.normpath(p))

            if any(_norm(p) == _norm(target) for p in parts):
                return True

            new_value = current_value
            if new_value and not new_value.endswith(";"):
                new_value += ";"
            new_value += target

            winreg.SetValueEx(key, "Path", 0, value_type, new_value)

            # Broadcast environment change (best-effort)
            try:
                import ctypes

                HWND_BROADCAST = 0xFFFF
                WM_SETTINGCHANGE = 0x001A
                SMTO_ABORTIFHUNG = 0x0002

                res = ctypes.c_ulong()
                ctypes.windll.user32.SendMessageTimeoutW(
                    HWND_BROADCAST,
                    WM_SETTINGCHANGE,
                    0,
                    ctypes.c_wchar_p("Environment"),
                    SMTO_ABORTIFHUNG,
                    5000,
                    ctypes.byref(res),
                )
            except Exception:
                pass

            return True

        # POSIX: append export line to a shell profile file (best-effort)
        home = Path.home()
        target = str(directory)
        shell = os.environ.get("SHELL", "")
        shell_name = Path(shell).name.lower()

        # If fish shell detected, prefer updating fish config
        fish_config = home / ".config" / "fish" / "config.fish"
        if "fish" in shell_name or fish_config.exists():
            begin = "# >>> chi-sdk (ensure-chi) PATH >>>"
            end = "# <<< chi-sdk (ensure-chi) PATH <<<"
            export_line = f'set -gx PATH "{target}" $PATH'

            def _ensure_fish() -> bool:
                try:
                    if fish_config.exists():
                        text = fish_config.read_text(encoding="utf-8", errors="ignore")
                    else:
                        text = ""
                    if target in text or export_line in text:
                        return True
                    block = f"\n{begin}\n{export_line}\n{end}\n"
                    fish_config.parent.mkdir(parents=True, exist_ok=True)
                    with open(fish_config, "a", encoding="utf-8") as fh:
                        fh.write(block)
                    return True
                except Exception:
                    return False

            if _ensure_fish():
                return True
            # If fish-specific update failed, continue with generic profile fallbacks

        # Choose candidate files based on shell (bash/zsh/others)
        candidates = []
        if "zsh" in shell_name:
            candidates = [home / ".zprofile", home / ".zshrc"]
        elif "bash" in shell_name:
            candidates = [home / ".bash_profile", home / ".bashrc", home / ".profile"]
        else:
            candidates = [home / ".profile"]

        begin = "# >>> chi-sdk (ensure-chi) PATH >>>"
        end = "# <<< chi-sdk (ensure-chi) PATH <<<"
        export_line = f'export PATH="{target}:$PATH"'

        def _ensure_block(fpath: Path) -> bool:
            try:
                if fpath.exists():
                    text = fpath.read_text(encoding="utf-8", errors="ignore")
                else:
                    text = ""
                # already present?
                if target in text or export_line in text:
                    return True
                block = f"\n{begin}\n{export_line}\n{end}\n"
                fpath.parent.mkdir(parents=True, exist_ok=True)
                with open(fpath, "a", encoding="utf-8") as fh:
                    fh.write(block)
                return True
            except Exception:
                return False

        # Update the first applicable file; if none exist, create the first in the list
        updated = False
        for f in candidates:
            if f.exists():
                updated = _ensure_block(f)
                break
        if not updated and candidates:
            updated = _ensure_block(candidates[0])

        return updated
    except Exception:
        return False


@click.command("ensure-chi", help="Ensure chi-tui binary is available")
@click.option(
    "--compile", "compile_only", is_flag=True, help="Only try compilation from sources"
)
@click.option(
    "--download", "download_only", is_flag=True, help="Only try downloading binary"
)
@click.option("--force", is_flag=True, help="Force reinstall even if already exists")
@click.option(
    "--add-to-path/--no-add-to-path",
    "add_to_path",
    is_flag=True,
    default=False,
    help="Add install dir to PATH if missing (Windows/macOS/Linux)",
)
@click.pass_context
def ensure_chi_cmd(
    ctx, compile_only: bool, download_only: bool, force: bool, add_to_path: bool
):
    """Ensure chi-tui binary is available - compile from sources or download."""

    if compile_only and download_only:
        error_msg = "Cannot use both --compile and --download flags"
        if _json_mode(ctx):
            emit_error(
                "invalid_flags", error_msg, command="chi-admin ensure-chi", exit_code=1
            )
        else:
            click.echo(f"Error: {error_msg}")
        return

    # Check if chi-tui already exists in PATH (skip if --force or explicit flags)
    if not force and not compile_only and not download_only:
        existing = _which("chi-tui")
        if existing:
            msg = {
                "status": "already_installed",
                "path": existing,
                "message": "chi-tui is already available in PATH (use --force to reinstall)",
            }
            if _json_mode(ctx):
                emit_ok(msg, command="chi-admin ensure-chi")
            else:
                click.echo(f"✓ chi-tui already installed: {existing}")
                click.echo("  Use --force to reinstall or update")
            return

    # Determine target directory (chi_sdk/bin)
    chi_sdk_bin = _get_chi_sdk_bin_dir()
    binary_name = "chi-tui.exe" if os.name == "nt" else "chi-tui"
    target_binary = chi_sdk_bin / binary_name

    # Check if binary already exists in chi_sdk/bin (skip if using explicit flags)
    if not compile_only and not download_only and target_binary.exists():
        # Install to user bin
        user_bin_path = _install_to_user_bin(target_binary)
        if user_bin_path:
            user_bin_dir = user_bin_path.parent
            in_path = _check_path_contains(user_bin_dir)
            path_updated = False
            if add_to_path and not in_path:
                path_updated = _add_to_user_path(user_bin_dir)

            msg_installed: Dict[str, Any] = {
                "status": "installed_to_user_bin",
                "source": str(target_binary),
                "target": str(user_bin_path),
                "in_path": in_path,
                "path_updated": path_updated,
            }

            if _json_mode(ctx):
                emit_ok(msg_installed, command="chi-admin ensure-chi")
            else:
                click.echo(f"✓ Installed chi-tui to: {user_bin_path}")
                if not in_path:
                    if add_to_path and path_updated:
                        click.echo("✓ Updated user PATH (open a new terminal)")
                    else:
                        if platform.system().lower() == "windows":
                            click.echo(
                                f"⚠ Add to PATH: {user_bin_dir} (or: chi-admin ensure-chi --add-to-path)"
                            )
                        else:
                            shell = os.environ.get("SHELL", "")
                            shell_name = Path(shell).name.lower()
                            if "fish" in shell_name:
                                click.echo(
                                    f'⚠ Add to PATH (fish): set -gx PATH "{user_bin_dir}" $PATH (or: chi-admin ensure-chi --add-to-path)'
                                )
                            else:
                                click.echo(
                                    f'⚠ Add to PATH: export PATH="{user_bin_dir}:$PATH" (or: chi-admin ensure-chi --add-to-path)'
                                )
            return

    success = False
    method = None

    # Try compilation if requested or no specific flag
    if compile_only or not download_only:
        sources_dir = _get_chi_sdk_sources_dir()
        if sources_dir:
            click.echo(f"Found sources at: {sources_dir}")
            click.echo("Compiling chi-tui from sources...")
            if _compile_from_sources(sources_dir, chi_sdk_bin):
                success = True
                method = "compiled"
            else:
                if compile_only:
                    error_msg = "Compilation failed. Make sure Rust/Cargo is installed."
                    if _json_mode(ctx):
                        emit_error(
                            "compile_failed",
                            error_msg,
                            command="chi-admin ensure-chi",
                            exit_code=2,
                        )
                    else:
                        click.echo(f"Error: {error_msg}")
                    return
        elif compile_only:
            error_msg = (
                "Sources not found. Checked:\n"
                "  - ./rust-tui/ (local repository)\n"
                "  - ../rust-tui/ (parent directories)\n"
                "  - chi_sdk/chi-tui-sources/ (pip install chi_sdk[sources])\n"
                "\nMake sure you're in the chi_sdk repository or install with: pip install chi_sdk[sources]"
            )
            if _json_mode(ctx):
                emit_error(
                    "no_sources", error_msg, command="chi-admin ensure-chi", exit_code=2
                )
            else:
                click.echo(f"Error: {error_msg}")
            return

    # Try download if compilation failed and not compile_only
    if not success and (download_only or not compile_only):
        click.echo("Downloading chi-tui binary...")
        if _download_binary(chi_sdk_bin):
            success = True
            method = "downloaded"
        elif download_only:
            error_msg = "Failed to download binary from GitHub releases"
            if _json_mode(ctx):
                emit_error(
                    "download_failed",
                    error_msg,
                    command="chi-admin ensure-chi",
                    exit_code=3,
                )
            else:
                click.echo(f"Error: {error_msg}")
            return

    if success:
        # Install to user bin
        user_bin_path = _install_to_user_bin(target_binary)
        if user_bin_path:
            user_bin_dir = user_bin_path.parent
            in_path = _check_path_contains(user_bin_dir)
            path_updated = False
            if add_to_path and not in_path:
                path_updated = _add_to_user_path(user_bin_dir)

            msg_success: Dict[str, Any] = {
                "status": "success",
                "method": method,
                "chi_sdk_bin": str(target_binary),
                "user_bin": str(user_bin_path),
                "in_path": in_path,
                "path_updated": path_updated,
            }

            if _json_mode(ctx):
                emit_ok(msg_success, command="chi-admin ensure-chi")
            else:
                click.echo(f"✓ Successfully {method} chi-tui")
                click.echo(f"✓ Installed to: {user_bin_path}")
                if not in_path:
                    if add_to_path and path_updated:
                        click.echo("✓ Updated user PATH (open a new terminal)")
                    else:
                        if platform.system().lower() == "windows":
                            click.echo(
                                f"⚠ Add to PATH: {user_bin_dir} (or: chi-admin ensure-chi --add-to-path)"
                            )
                        else:
                            shell = os.environ.get("SHELL", "")
                            shell_name = Path(shell).name.lower()
                            if "fish" in shell_name:
                                click.echo(
                                    f'⚠ Add to PATH (fish): set -gx PATH "{user_bin_dir}" $PATH (or: chi-admin ensure-chi --add-to-path)'
                                )
                            else:
                                click.echo(
                                    f'⚠ Add to PATH: export PATH="{user_bin_dir}:$PATH" (or: chi-admin ensure-chi --add-to-path)'
                                )
        else:
            msg_partial: Dict[str, Any] = {
                "status": "partial_success",
                "method": method,
                "chi_sdk_bin": str(target_binary),
                "message": "Binary available but could not install to user bin",
            }
            if _json_mode(ctx):
                emit_ok(msg_partial, command="chi-admin ensure-chi")
            else:
                click.echo(f"✓ Successfully {method} chi-tui to: {target_binary}")
                click.echo("⚠ Could not install to user bin directory")
    else:
        error_msg = (
            "Could not ensure chi-tui availability.\n"
            "Try one of:\n"
            "  - pip install chi_sdk[sources] && chi-admin ensure-chi --compile\n"
            "  - pip install chi_sdk[bin]\n"
            "  - chi-admin ensure-chi --download"
        )
        if _json_mode(ctx):
            emit_error(
                "ensure_failed", error_msg, command="chi-admin ensure-chi", exit_code=4
            )
        else:
            click.echo(f"Error: {error_msg}")
