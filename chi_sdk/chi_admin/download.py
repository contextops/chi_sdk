"""Deprecated download command.

Historically this command fetched a prebuilt chi-tui binary from GitHub
releases. Since merging the binary into the chi-sdk distribution, the
recommended path is to install via pip and use `chi-admin ensure-chi`.
"""

from typing import Optional

import click

from ..sdk import emit_ok


def _json_mode(ctx: Optional[click.Context] = None) -> bool:
    ctx = ctx or click.get_current_context(silent=True)
    import os

    env = os.getenv("CHI_TUI_JSON", "")
    return bool(
        (ctx and ctx.obj and ctx.obj.get("json")) or env in ("1", "true", "yes")
    )


@click.command(
    "download",
    help="[DEPRECATED] Prefer 'pip install chi-sdk' + 'chi-admin ensure-chi'",
)
@click.pass_context
def download_cmd(ctx):
    """Legacy command kept for backward compatibility.

    Emits guidance to install via pip and use ensure-chi.
    The JSON payload intentionally includes `installed` and `guidance`
    fields for consumers that relied on the old interface.
    """

    guidance = (
        "The 'download' command is deprecated.\n"
        "Install via pip and then run ensure-chi:\n"
        "  - pip install chi-sdk\n"
        "  - chi-admin ensure-chi           # Auto-detect and install\n"
        "  - chi-admin ensure-chi --compile # Compile from sources\n"
        "  - chi-admin ensure-chi --download # Download binary"
    )

    if _json_mode(ctx):
        # Maintain compatibility with tests/consumers expecting these keys
        emit_ok(
            {
                "installed": False,
                "guidance": guidance,
                "status": "deprecated",
            },
            command="chi-admin download",
        )
    else:
        click.echo("⚠ DEPRECATED\n" + guidance)
