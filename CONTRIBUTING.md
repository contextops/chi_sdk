# Contributing

Thanks for your interest in improving this project! This repo pairs a typed Python CLI (source of truth) with a Rust TUI (thin presentation). Please follow the guidelines below to keep things clean and consistent.

## Quick Setup

- Python 3.11+, Rust toolchain (stable), and `cargo`.
- Create a venv and install dev deps:
  - `python3 -m venv .venv && source .venv/bin/activate`
  - `pip install -U pip`
  - `pip install -r requirements-dev.txt`
  - `pip install -e python-chi-sdk`

## Running and Testing

- Ensure TUI binary: `chi-admin ensure-chi --compile` (or `--download`)
- Run the example app UI: `pip install -e example-apps/example-app && example-app ui`
- Python lint/format: `ruff .` and `black .`
- Python tests (SDK): `cd python-chi-sdk && pytest -q`
- Rust checks: `cd rust-tui && cargo fmt --all && cargo clippy --all-targets -- -D warnings && cargo check`
- Rust tests: `cd rust-tui && cargo test`
- JSON contract check: `CHI_TUI_JSON=1 example-app schema`

## Coding Style

- Python
  - Types required. 4-space indent.
  - Pydantic v2 models: suffix with `*In` / `*Out` (e.g., `HelloIn`, `HelloOut`).
  - CLI function `snake_case` → CLI command `kebab-case`.
  - No ad‑hoc prints: emit through the envelope (`emit_ok`, `emit_error`, `emit_progress`).
  - Import module: `chi_sdk` (package distributed as `chi-sdk`).
- Rust
  - Keep the TUI pure (rendering/state) — no business logic.
  - `rustfmt` + `clippy` clean.

## Commits and PRs

- Use Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
- Keep changes focused and small; update docs when behavior or schema changes.
- PRs should include:
  - Clear description and linked issue.
- “How to verify” section with concrete commands and expected output (no special checklist format required).
  - If TUI changes visuals/UX: screenshots or a short GIF.
  - Mention if the JSON envelope or schema changed (and why).

## TUI Changes — Verification Protocol

When a change impacts the TUI, include a short checklist in the PR:

1) Provide commands to reproduce (e.g., `example-app ui`, `CHI_TUI_JSON=1 example-app schema`).
2) When relevant, reference stable navigation markers (e.g., `[[7]]`) from your `.tui/chi-index.yaml` to keep steps stable across changes.

## License

By contributing, you agree to the dual-licensing model:
- Rust TUI and prebuilt binary are distributed under AGPL-3.0.
- Python SDK and example app are distributed under Apache-2.0.

In addition, you grant the maintainers the right to relicense your contribution under a commercial license to support enterprise use (standard CLA intent). A dedicated CLA workflow may be introduced; until then, submitting a contribution implies consent to this relicensing right.
