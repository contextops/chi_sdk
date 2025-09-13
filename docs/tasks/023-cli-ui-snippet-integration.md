# [ARCHIVED] CLI `ui` Subcommand Snippet — Opt‑In Integration

> Status: Archived. The SDK now provides an automatic `ui` subcommand via `build_cli()`.
> You can launch the TUI with `your-app ui`. Ensure the TUI binary with `chi-admin ensure-chi`.

## Summary
- Provide a ready‑to‑paste Python snippet to add a `ui` subcommand to an existing Click‑based CLI.
- The subcommand launches the TUI (wrapper or binary) with proper env, keeping business logic in Python.

## Goals
- Documented, low‑risk path to integrate TUI into arbitrary projects.
- No automatic code modification; users control where to place the snippet.

## Non-Goals
- Forcing a specific CLI framework beyond Click for v1.

## Deliverables
- A self-contained snippet with instructions, including Windows notes.
- Guidance on env vars (`CHI_TUI_JSON=1`, `CHI_APP_BIN=<your-cli>`), and config under `.tui/`.
- Troubleshooting section for PATH and exit codes.

## Snippet (Click)
- Instructions:
  - Add this to your CLI module after registering other commands.
  - Ensure `.tui/bin/chi-tui` exists (via `chi-admin init`).
- Example:
  - Command to run: `my-app ui [--release] [--rebuild]`.
  - Behavior: rebuild optional (delegates to `chi-admin rebuild`), then runs the TUI binary.

## How to Verify
- Add subcommand to a sample CLI and run:
  - Command: `my-app ui`
  - Expect: TUI starts and connects to `my-app` backend; `[[7]]` JSON viewer works.
- JSON contract still available:
  - Command: `CHI_TUI_JSON=1 my-app schema`
  - Expect: `ok: true`, includes your commands and schemas.

## Acceptance Criteria
- Snippet copy-pastes cleanly and works on Linux/macOS/Windows with `.tui/` present.
- Clear guidance is provided for non-Click users to create an equivalent subcommand.

## Discussion
- See `docs/tasks/023-cli-ui-snippet-integration-discuss.md` for ongoing Q&A.
