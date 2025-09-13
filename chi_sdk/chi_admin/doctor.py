"""Doctor command for validating CHI TUI setup."""

import os
import re
import shutil
from pathlib import Path
from typing import Optional

import click

from ..sdk import emit_ok


def _json_mode(ctx: Optional[click.Context] = None) -> bool:
    ctx = ctx or click.get_current_context(silent=True)
    env = os.getenv("CHI_TUI_JSON", "")
    return bool(
        (ctx and ctx.obj and ctx.obj.get("json")) or env in ("1", "true", "yes")
    )


def _read_app_bin_from_config(config_dir: Path) -> Optional[str]:
    cfg = config_dir / "config.yaml"
    if not cfg.exists():
        return None
    try:
        text = cfg.read_text(encoding="utf-8")
        # very minimal parse: look for a line like `app_bin: value` (value may be quoted)
        m = re.search(r"(?m)^\s*app_bin\s*:\s*['\"]?([^'\"\s]+)['\"]?\s*$", text)
        if m:
            return m.group(1)
    except Exception:
        return None
    return None


def _which(prog: str) -> Optional[str]:
    return shutil.which(prog)


def _chi_sdk_cached_binary() -> Optional[Path]:
    from .utils import _cache_bin_path

    bin_dir = _cache_bin_path()
    name = "chi-tui.exe" if os.name == "nt" else "chi-tui"
    p = bin_dir / name
    return p if p.exists() else None


@click.command("doctor", help="Validate setup: chi-tui on PATH, backend available")
@click.option(
    "--config", "config_path", default=".tui", show_default=True, help="Config dir"
)
@click.option(
    "--binary-name", default=None, help="Backend CLI name (overrides config/env)"
)
@click.pass_context
def doctor_cmd(ctx, config_path: str, binary_name: Optional[str]):
    problems = []
    info = {}

    chi_tui = _which("chi-tui")
    info["chi_tui"] = chi_tui
    if not chi_tui:
        cached = _chi_sdk_cached_binary()
        info["chi_sdk_cache"] = str(cached) if cached else None
        if not cached:
            problems.append("chi-tui not found on PATH. Install: pip install chi-sdk")

    cfg_dir = Path(config_path)
    app_bin = (
        os.getenv("CHI_APP_BIN") or binary_name or _read_app_bin_from_config(cfg_dir)
    )
    info["app_bin"] = app_bin
    if not app_bin:
        problems.append(
            "Backend app_bin not set. Set CHI_APP_BIN or .tui/config.yaml: app_bin: <name>"
        )
    else:
        backend = _which(app_bin)
        info["backend_path"] = backend
        if not backend:
            problems.append(f"Backend '{app_bin}' not found on PATH.")

    ok = len(problems) == 0
    if _json_mode(ctx):
        emit_ok(
            {"ok": ok, "problems": problems, "info": info}, command="chi-admin doctor"
        )
    else:
        if ok:
            click.echo("OK: chi-tui and backend available.")
        else:
            click.echo("Problems detected:")
            for p in problems:
                click.echo(f"- {p}")
            raise click.exceptions.Exit(2)
