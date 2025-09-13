# [ARCHIVED] Admin Init — MVP: Prebuilt TUI, .tui Scaffold, Wrapper, Doctor

> Status: Archived. This proposal referenced `chi-admin download` and wrapper-first flows.
> The current approach simplifies usage:
> - Ensure TUI binary with `chi-admin ensure-chi --compile|--download`.
> - Launch via your app: `your-app ui` (built-in subcommand), or `CHI_APP_BIN=your-app chi-tui`.
> - Config anchor: `CHI_TUI_CONFIG_DIR` → `.tui/chi-index.yaml`.

## Summary
- Enable Python developers to add a TUI without compiling Rust.
- Provide `chi-admin init` to scaffold `.tui/`, place a prebuilt TUI binary, and create a wrapper.
- Provide `chi-admin doctor` to validate environment and setup.
- Optional: `chi-admin download` to fetch the correct prebuilt binary when not packaged via wheels.

## Goals
- Zero‑Rust setup for Case‑1.
- Clear, minimal footprint in the target repo under `.tui/`.
- Predictable wrapper to launch the TUI against an existing CLI.

## Non‑Goals
- No source overlay or rebuild flow (covered in 021).
- No PyPI wheels for the binary yet (covered in 022).

## Deliverables
- New CLI tool: `chi-admin` with subcommands:
  - `init <path> --binary-name <name> --config <path> [--create-demo]`
  - `doctor`
  - `download [--force]` (if binary not shipped via wheel in MVP)
- Files created by `init`:
  - `.tui/config.yaml` (basic config incl. app bin name)
  - `.tui/README.md` (how to run, path setup, troubleshooting)
  - `.tui/bin/chi-tui[.exe]` (prebuilt TUI)
  - `mypro-ui` wrapper script (and `.bat` on Windows) that sets env and runs the TUI

## Implementation Notes
- Wrapper sets `CHI_APP_BIN=<binary-name>` and `CHI_TUI_JSON=1` before launching TUI.
- `doctor` checks:
  - TUI binary executable and runnable.
  - Backend binary is on PATH (or resolvable via config).
  - JSON mode env ready.
- Distribution of the binary in MVP:
  - Either via `chi-admin download` from GitHub Releases based on OS/arch,
  - Or via a stop‑gap file server; the long‑term solution is wheels (022).

## How to Verify
- Scaffold (no Rust required):
  - Command: `chi-admin init . --binary-name=mypro --config=.tui/`
  - Expect:
    - `.tui/config.yaml` and `.tui/README.md` created.
    - `.tui/bin/chi-tui` (or `.exe` on Windows) present and executable.
    - Wrapper script `mypro-ui` created.
- Doctor:
  - Command: `chi-admin doctor`
  - Expect: all checks pass; prints a short OK summary.
- Launch TUI (using example backend):
  - Command: `CHI_APP_BIN=example-app mypro-ui`
  - Expect: TUI starts; navigate to “Panel Demo (YAML json_viewer) [[7]]” → JSON viewer works.
- JSON contract sanity:
  - Command: `CHI_TUI_JSON=1 example-app schema`
  - Expect: `ok: true`, `data.commands[]` non‑empty.

## Acceptance Criteria
- `chi-admin init` scaffolds `.tui/` and a working wrapper on Linux, macOS, Windows.
- `chi-admin doctor` reports OK when the binary and backend are in place.
- TUI launches via wrapper and renders against a known backend (e.g., `example-app`).
