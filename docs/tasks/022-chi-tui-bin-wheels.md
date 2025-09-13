# [ARCHIVED] chi-tui-bin Wheels + chi-sdk[tui] Extra

> Status: Archived. Replaced by `chi-admin ensure-chi` (compile/download) as the primary
> way to provide the `chi-tui` binary. The extras-based `chi-sdk[tui]` approach is no longer
> the recommended path in current docs.

## Summary
- Package prebuilt TUI binaries as platform wheels `chi-tui-bin`.
- Add optional extra `chi-sdk[tui]` to depend on the appropriate `chi-tui-bin` so `pip install "chi-sdk[tui]"` yields a working TUI without downloads.

## Goals
- Zero download at runtime; rely on pip to install the right artifact.
- Cross-platform support (Linux/macos/Windows; x86_64/arm64 where feasible).

## Non-Goals
- Source overlay or rebuild (021).

## Deliverables
- Build matrix in CI for Rust binary across platforms.
- Packaging step to wrap binary into wheels (per-platform tags) under `chi-tui-bin`.
- `chi-sdk` extra `tui` that pulls `chi-tui-bin`.
- Release workflow publishing wheels to PyPI and creating GitHub Releases.

## Implementation Notes
- Wheel contents:
  - `chi_tui_bin/` with the executable and a small launcher if needed.
  - Post-install script to mark executable bit on POSIX (if necessary).
- Versioning: keep `chi-tui-bin` and `rust-tui` in lockstep; encode build metadata.

## How to Verify
- Linux:
  - Command: `pip install "chi-sdk[tui]"`
  - Expect: TUI binary available on PATH or discoverable by `chi-admin doctor`; `doctor` passes.
- macOS:
  - Command: `pip install "chi-sdk[tui]"`
  - Expect: same as Linux; codesign/notarization not required for CLI terminal app (validate run).
- Windows:
  - Command: `pip install "chi-sdk[tui]"`
  - Expect: `.exe` present; `doctor` passes.
- End-to-end smoke:
  - Command: `chi-admin init . --binary-name=mypro --config=.tui/ && mypro-ui`
  - Expect: TUI launches and renders `[[7]]` JSON viewer when selected.

## Acceptance Criteria
- Wheels published for supported platforms; installation provides a runnable TUI.
- `chi-admin` detects installed wheel binary and skips `download`.

## Discussion
- See `docs/tasks/022-chi-tui-bin-wheels-discuss.md` for ongoing Q&A.
