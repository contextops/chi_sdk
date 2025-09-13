# Installation and Usage

This guide gets you from a fresh checkout to a running TUI, and shows the common dev/test flows used in this repo.

## Prerequisites
- Python 3.11+
- Rust toolchain (stable) with `cargo` (https://rustup.rs)
- make (optional)

## Quickstart (local dev)
1) Create a virtualenv and install dev deps

```
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip black ruff pytest mypy pydantic click pre-commit
```

2) Install the Python SDK in editable mode

```
pip install -e python-chi-sdk
```

3) Check/build the TUI

```
cd rust-tui && cargo check
```

4) Ensure chi-tui binary and run example app

```
chi-admin ensure-chi --compile   # or: --download
pip install -e example-apps/example-app
example-app ui
```

## Quickstart (prebuilt TUI — no Rust)
1) Create a virtualenv and install the SDK:

```
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install chi-sdk
```

2) Ensure TUI binary and run the TUI with your backend:

```
chi-admin ensure-chi --download   # or: --compile (if sources available)
CHI_APP_BIN=my-app chi-tui
```

3) Optional: scaffold integration files under your project:

```
chi-admin init . --binary-name=my-app --config=.tui/
chi-admin doctor
```

## Development Workflow
- Lint/format (Python): `ruff .` and `black .`
- Tests (Python): `pytest -q` (tests under `python-chi-sdk/tests/`)
- Check/tests (Rust): `cd rust-tui && cargo check && cargo test`
- Ensure TUI: `chi-admin ensure-chi --compile` (or `--download`)
- Run demo app: `example-app ui`
- Schema JSON check: `CHI_TUI_JSON=1 example-app schema`

## JSON Envelope: quick peek
Every CLI command writes a stable JSON envelope to stdout, e.g.:

```
CHI_TUI_JSON=1 example-app hello --name Ada --shout
```

Yields (abbreviated):

```
{
  "ok": true,
  "type": "data",
  "data": {
    "greeting": "HELLO, ADA!"
  }
}
```

Errors are reported as:

```
{
  "ok": false,
  "type": "error",
  "data": {
    "message": "...",
    "details": {"errors": [ {"loc": ["field"], "msg": "..."} ]}
  }
}
```

## Headless smoke mode (non‑interactive)
The TUI can render headlessly for CI/smoke.

Examples:

- Run headless for 10 ticks and print a summary

```
CHI_TUI_HEADLESS=1 CHI_TUI_SMOKE_SUMMARY=1 example-app ui --release
```

- Using the app `ui` command with auto-enter:

```
CHI_TUI_HEADLESS=1 CHI_TUI_SMOKE_SUMMARY=1 \
CHI_TUI_HEADLESS_ENTER_ID=panel_yaml_demo \
example-app ui --release
```

- Auto‑enter a menu item by id (from your `.tui/chi-index.yaml`)

```
CHI_TUI_HEADLESS=1 CHI_TUI_SMOKE_SUMMARY=1 \
CHI_TUI_HEADLESS_ENTER_ID=panel_yaml_demo \
example-app ui --release
```

Summary structure (stdout):

```
{
  "ok": true,
  "progress_seen": false,
  "status_seen": false,
  "view": "Panel",
  "result_present": true,
  "enter_done": true
}
```

Adjust ticks:

```
CHI_TUI_HEADLESS=1 CHI_TUI_TICKS=20 example-app ui
```

Direct cargo runs: set `CHI_TUI_CONFIG_DIR=<path to your .tui>` and `CHI_APP_BIN=<path to your CLI>` to avoid PATH/cwd issues.

## Troubleshooting
- cargo not found: install Rust (https://rustup.rs), re‑open shell.
- Virtualenv missing: ensure `source .venv/bin/activate` before `pip install -e ...`.
- JSON not printed: prefix commands with `CHI_TUI_JSON=1` or ensure the app sets it when spawning.
- Terminal keys: if running inside tmux/screen, ensure `TERM` supports CSI sequences.

## Repo pointers
- Python SDK (CLI, schemas): `python-chi-sdk/`
- TUI (Ratatui): `rust-tui/`
- Demo app: `example-apps/example-app/`
- Config directory: `.tui/` (entry: `chi-index.yaml`)
