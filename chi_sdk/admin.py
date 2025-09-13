from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Tuple

import click
import importlib.metadata as importlib_metadata

from .sdk import emit_ok
from .chi_admin import starter_templates
from .chi_admin.utils import _ensure_executable


def _json_mode(ctx: Optional[click.Context] = None) -> bool:
    ctx = ctx or click.get_current_context(silent=True)
    env = os.getenv("CHI_TUI_JSON", "")
    return bool(
        (ctx and ctx.obj and ctx.obj.get("json")) or env in ("1", "true", "yes")
    )


def _make_wrapper_scripts(
    config_dir: Path, binary_name: str
) -> Tuple[Optional[Path], Optional[Path]]:
    bindir = config_dir / "bin"
    bindir.mkdir(parents=True, exist_ok=True)

    # POSIX shell wrapper
    posix_path = bindir / f"{binary_name}-ui"
    posix_script = starter_templates.POSIX_WRAPPER_SCRIPT.format(
        binary_name=binary_name
    )
    posix_path.write_text(posix_script, encoding="utf-8")
    _ensure_executable(posix_path)

    # Windows cmd wrapper
    win_path = bindir / f"{binary_name}-ui.bat"
    win_script = starter_templates.WINDOWS_WRAPPER_SCRIPT.format(
        binary_name=binary_name
    )
    win_path.write_text(win_script, encoding="utf-8")
    return posix_path, win_path


@click.group(
    help="chi-admin — scaffold and maintain CHI TUI integration",
    invoke_without_command=True,
)
@click.option("--json", "json_mode", is_flag=True, help="Emit JSON envelope to stdout")
@click.option("--version", "show_version", is_flag=True, help="Show version and exit")
@click.pass_context
def cli(ctx, json_mode: bool, show_version: bool):
    ctx.ensure_object(dict)
    ctx.obj["json"] = json_mode
    if show_version:
        try:
            ver = str(importlib_metadata.version("chi-sdk"))
        except Exception:
            ver = "0.0.0.dev"
        if _json_mode(ctx):
            emit_ok({"app": "chi-admin", "version": ver}, command="version")
        else:
            click.echo(f"chi-admin {ver}")
        raise click.exceptions.Exit(0)


@cli.command("init", help="Scaffold .tui/ and wrapper for your CLI")
@click.argument("path", type=click.Path(file_okay=False, dir_okay=True), default=".")
@click.option("--binary-name", required=True, help="Your CLI name to act as backend")
@click.option(
    "--config", "config_path", default=".tui", show_default=True, help="Config dir"
)
@click.option(
    "--create-demo", is_flag=True, help="Include demo notes in .tui/README.md"
)
@click.option("--force", is_flag=True, help="Overwrite existing files if present")
@click.pass_context
def init_cmd(
    ctx, path: str, binary_name: str, config_path: str, create_demo: bool, force: bool
):
    root = Path(path).resolve()
    cfg_dir = (root / config_path).resolve()
    cfg_dir.mkdir(parents=True, exist_ok=True)

    # Write config.yaml
    cfg_file = cfg_dir / "config.yaml"
    if not cfg_file.exists() or force:
        cfg_file.write_text(
            starter_templates.CONFIG_YAML.format(binary_name=binary_name),
            encoding="utf-8",
        )

    # Write .tui/README.md
    readme = cfg_dir / "README.md"
    if not readme.exists() or force:
        readme.write_text(
            starter_templates.README_TEMPLATE.format(binary_name=binary_name),
            encoding="utf-8",
        )

    # Create wrapper scripts
    posix_path, win_path = _make_wrapper_scripts(cfg_dir, binary_name)

    # Create comprehensive default nav (`.tui/chi-index.yaml`) with helpful comments
    main_yaml = cfg_dir / "chi-index.yaml"
    if not main_yaml.exists() or force:
        header_title = binary_name.replace("-", " ").title() + " - Terminal UI"
        main_yaml.write_text(
            starter_templates.CHI_INDEX_YAML.format(
                binary_name=binary_name, header_title=header_title
            ),
            encoding="utf-8",
        )
    panel_b = cfg_dir / "panel_b.yaml"
    if not panel_b.exists() or force:
        panel_b.write_text(
            starter_templates.PANEL_B_YAML.format(binary_name=binary_name),
            encoding="utf-8",
        )

    # Create styles configuration (optional but helpful)
    styles_yaml = cfg_dir / "styles.yaml"
    if not styles_yaml.exists() or force:
        styles_yaml.write_text(
            starter_templates.STYLES_YAML,
            encoding="utf-8",
        )

    payload = {
        "path": str(root),
        "config_dir": str(cfg_dir),
        "default_nav": str(main_yaml),
        "panel_config": str(panel_b),
        "styles_config": str(styles_yaml),
        "wrapper_posix": str(posix_path),
        "wrapper_windows": str(win_path),
        "notes": "Customize .tui/*.yaml files to personalize your TUI",
    }
    if _json_mode(ctx):
        emit_ok(payload, command="chi-admin init")
    else:
        click.echo(f"Scaffolded .tui/ under: {cfg_dir}")
        click.echo(f"Wrapper (POSIX): {posix_path}")
        click.echo(f"Wrapper (Windows): {win_path}")


"""Additional admin CLI commands live outside this module to keep it small."""

# Register external admin commands
from .chi_admin.doctor import doctor_cmd  # noqa: E402
from .chi_admin.download import download_cmd  # noqa: E402
from .chi_admin.ensure_chi import ensure_chi_cmd  # noqa: E402

cli.add_command(doctor_cmd)
cli.add_command(download_cmd)
cli.add_command(ensure_chi_cmd)


def main():
    cli()


if __name__ == "__main__":  # pragma: no cover
    main()
