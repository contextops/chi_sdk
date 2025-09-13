# CHI TUI + CHI SDK — Cheat Sheet (E2E)

This document gives a complete, practical overview of the project: what CHI is (CLI → JSON) + the TUI (Ratatui), how to add it to your own Python CLI, how to configure the TUI, how to run it, available options, and how to test.

## What It Is and Why
- Python: the source of truth. Typed commands (Pydantic v2 + Click) emit a stable JSON envelope plus a `schema` for the TUI.
- Rust (Ratatui): thin presentation layer. Renders views based on JSON without duplicating business logic.
- Goal: quickly attach a TUI to an existing CLI (or greenfield) while keeping a clean separation of concerns.

Repository structure:
- `python-chi-sdk/` — SDK: `@chi_command` decorator, `build_cli()`, envelope (`emit_ok/emit_error/emit_progress`), `schema`.
- `rust-tui/` — TUI: navigation via YAML (`.tui/chi-index.yaml`), A/B panels, widgets (`json_viewer`, `menu`, `form`, `panel`).
- `example-apps/example-app/` — sample backend with commands and a launcher `example-app ui`.
- `chi-tui-bin/` — prebuilt TUI shipped as a Python package (entrypoint `chi-tui`).

## Quick Start

Variant A — local development (Rust + Python)
1) Python dev environment:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -U pip black ruff pytest mypy pydantic click pre-commit
   pip install -e python-chi-sdk
   ```
2) Check the TUI builds:
   ```bash
   cd rust-tui && cargo check
   ```
3) Ensure TUI binary and run example app:
   ```bash
   chi-admin ensure-chi --compile   # or: --download
   # Auto-add install dir to PATH (Windows/macOS/Linux):
   # chi-admin ensure-chi --compile --add-to-path
   pip install -e example-apps/example-app
   example-app ui
   ```

Variant B — no Rust toolchain (use the admin helper)
1) Install the SDK:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -U pip
   pip install chi-sdk
   ```
2) Ensure TUI binary and launch the TUI with your own backend:
   ```bash
   chi-admin ensure-chi --download
   # Auto-add install dir to PATH (Windows/macOS/Linux):
   # chi-admin ensure-chi --download --add-to-path
   CHI_APP_BIN=my-app chi-tui
   ```
3) Alternative: run the TUI via the app wrapper:
   ```bash
   CHI_APP_BIN=my-app chi-tui
   ```

## Integrate With Your CLI (Python)
Minimal example (Pydantic v2 + Click)
```python
# my_app/cli.py
from typing import List
from pydantic import BaseModel, Field
from chi_sdk import chi_command, build_cli, emit_progress

class HelloIn(BaseModel):
    name: str = Field(..., description="User name")
    shout: bool = Field(False, description="Uppercase the greeting")

class HelloOut(BaseModel):
    greeting: str

@chi_command(input_model=HelloIn, output_model=HelloOut, description="Say hello")
def hello(inp: HelloIn) -> HelloOut:
    txt = f"Hello, {inp.name}!"
    return HelloOut(greeting=txt.upper() if inp.shout else txt)

# (optional) progress streaming
class WorkOut(BaseModel):
    status: str

@chi_command(output_model=WorkOut, description="Simulate work with progress")
def do_work() -> WorkOut:
    for i in range(3):
        emit_progress(message=f"step {i+1}", percent=(i/3)*100, stage="run", command="do-work")
    return WorkOut(status="done")

cli = build_cli("my-app")

def main():
    cli()

if __name__ == "__main__":
    main()
```
Run (text or JSON):
```bash
python -m my_app.cli hello --name Ada
python -m my_app.cli --json hello --name Ada
```
Result envelope (short):
```json
{
  "version": "1.0",
  "ok": true,
  "type": "result",
  "command": "hello",
  "data": {"greeting": "Hello, Ada!"},
  "meta": {}
}
```
Streaming (NDJSON): a few `type: "progress"` events, then the final `type: "result"`.

Schemas for the TUI:
```bash
python -m my_app.cli --json schema
```
Returns command descriptions and their JSON Schemas (the TUI can automatically map fields in forms).

Conventions:
- Models: `*In` for input, `*Out` for output (e.g., `HelloIn`, `HelloOut`).
- CLI names: function `snake_case` → command `kebab-case` (`sum_numbers` → `sum-numbers`).
- No `print()`: use the envelope (`emit_ok/emit_error/emit_progress`) for all output.

## Running the TUI With a Backend
- Direct (binary from the package): `CHI_APP_BIN=<your-cli> chi-tui`
- From the example: `example-app ui` (builds and launches the Rust TUI)
- Wrapper (POSIX):
  ```sh
  # my-app-ui
  #!/usr/bin/env sh
  set -e
  CHI_APP_BIN="my-app" CHI_TUI_JSON=1 exec chi-tui "$@"
  ```
- Admin helper (`chi-admin`):
  - Integration scaffold: `chi-admin init . --binary-name=my-app --config=.tui/`
  - Installation check: `chi-admin doctor` (JSON: `CHI_TUI_JSON=1 chi-admin doctor`)
  - Binary via admin: `chi-admin ensure-chi --download`

## TUI Configuration (YAML)
Main navigation: `.tui/chi-index.yaml` in your project.
- Menu items: header (`widget: header`), leaf with a command (`command: ...`), dynamic list (`lazy_items` / `autoload_items`), panel (`widget: panel`).
- Stable markers in titles (e.g., `[[7]]`) — used for manual tests.

Panel (A/B view):
- `panel_layout`: `horizontal|vertical`
- `panel_size`: `1:1`, `1:2`, `2:1`, `1:3`, `3:1`, `2:3`, `3:2`
- Content sources:
  - Inline: `pane_a_cmd`, `pane_b_cmd` (CLI commands)
  - From file: `pane_a_yaml`, `pane_b_yaml` (e.g., `panels/panel_b.yaml`)

Widgets (spec → widget):
- `json_viewer`: fields `cmd` (execute a command) or `yaml` (load YAML/JSON). Uses the unified ResultViewer — keys: arrows/PgUp/PgDn/Home/End, `w` wrap, `j` raw JSON toggle.
- `menu`: fields `spec` (path to AppConfig) or `config` (inline). Keys: arrows, PgUp/PgDn, Home/End.
- `form`: `fields[]` (types: `text`, `password`, `textarea`, `checkbox`, `select`, `multiselect`, `number`, `array`), `submit.command`. Dynamic options: `options_cmd` + `unwrap`.
- `panel`: nested panel in B (keeps focus B.A/B.B).
- `markdown`: fields `path` (or `text`); fenced code blocks highlighted via syntect; keys: arrows/PgUp/PgDn/Home/End, `w` wrap.
- `watchdog`: fields `commands` and optional `sequential: true`; splits pane vertically and streams each command's output.
 - Title overrides:
   - Spec-level: many widgets accept `title:` in their spec (`json_viewer`, `menu`, `markdown`, `watchdog`).
   - In menu items: `pane_b_title:` overrides the Pane B header for the item.

Focus and navigation:
- Tab cycles: A → B.A → B.B → A (gdy Pane B ma panel zagnieżdżony). Bez panelu zagnieżdżonego: A ↔ B. Shift+Tab cykl odwrotny.
- Modal textarea: Ctrl+S save, Esc cancel.

Screen options (top-level in `.tui/*.yaml`):
- `auto_enter`: auto-enter a menu item by id when the screen loads (focus stays on Pane A)
- `can_close`: allow leaving panel view with Esc (default `true`); set to `false` to lock the layout

Menu item streaming:
- Add `stream: true` on a menu item to ensure streaming updates render even when a panel is open.

YAML examples (short):
```yaml
# Pane B → JSON from a command
type: json_viewer
cmd: "example-app list-items"
```
```yaml
# Pane B → menu from AppConfig
type: menu
spec: "chi-index.yaml"
```

## Environment Variables and Options
Backend/CLI and I/O:
- `CHI_TUI_JSON=1` — forces the JSON envelope in the CLI (how the TUI talks to the backend).
- `CHI_APP_BIN=<cli-name>` — your CLI’s name (used as `${APP_BIN}` in YAMLs).

TUI configuration:
- `CHI_TUI_CONFIG_DIR=/abs/path/to/.tui` — points to the configuration directory (must contain `chi-index.yaml`).
- Auto-detection: if `chi-index.yaml` is found (in `CWD`, `CWD/.tui`, ancestors' `.tui`, or `~/.tui`), the TUI uses it and sets `CHI_TUI_CONFIG_DIR` accordingly.

Headless/smoke (non-interactive) mode:
- `CHI_TUI_HEADLESS=1` — run without a TTY (test render).
- `CHI_TUI_TICKS=10` — number of “ticks” (default 10).
- `CHI_TUI_HEADLESS_ENTER_ID=<id>` — auto-Enter the menu item with the given `id`.
- `CHI_TUI_SMOKE_SUMMARY=1` — print a summary to stdout (JSON).

Form options (cache):
- `CHI_TUI_OPTIONS_TTL_SEC` — TTL for form options cache (default 30s; `0` = disable cache).

## Headless Mode — Examples
- 10 ticks + summary:
  ```bash
  CHI_TUI_HEADLESS=1 CHI_TUI_SMOKE_SUMMARY=1 example-app ui --release
  ```
- Auto-enter by `id` from `nav.yaml`:
  ```bash
  CHI_TUI_HEADLESS=1 CHI_TUI_SMOKE_SUMMARY=1 \
  CHI_TUI_HEADLESS_ENTER_ID=panel_yaml_demo \
  example-app ui --release
  ```
- Change number of ticks:
  ```bash
  CHI_TUI_HEADLESS=1 CHI_TUI_TICKS=20 example-app ui
  ```
