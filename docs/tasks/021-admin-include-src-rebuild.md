# [ARCHIVED] Admin Include-Src + Rebuild: Overlay Sources and Local Build

> Status: Archived. This plan referenced `chi-admin rebuild` and a `.tui/src` overlay.
> Current flow favors `chi-admin ensure-chi --compile` to build from local sources without
> maintaining an overlay under `.tui/`. Use your app's built-in `ui` subcommand to launch.

## Summary
- Extend `chi-admin init` with `--include-src` to scaffold a source overlay under `.tui/src/`.
- Add `chi-admin rebuild [--release]` to build the TUI locally with Rust toolchain, replacing the binary in `.tui/bin/`.

## Goals
- Let advanced users customize visuals and hooks without forking the repo.
- Keep overlay changes confined to `.tui/` in the host project.

## Non-Goals
- Publishing prebuilt wheels (022).
- Auto-installing Rust toolchain.

## Deliverables
- `chi-admin init ... --include-src` adds:
  - `.tui/src/banner.rs`
  - `.tui/src/background.rs`
  - `.tui/src/custom_hooks.rs`
  - Comments in each file describing extension points.
- `chi-admin rebuild [--release]`:
  - Compiles the TUI using the overlay (uses cargo).
  - Replaces `.tui/bin/chi-tui[.exe]` with the build artifact.
- `.tui/README.md` updated with rebuild instructions and troubleshooting.
- Windows support: generate `.bat` wrapper and ensure rebuild copies the correct `.exe`.

## Implementation Notes
- Overlay mechanism: template project or patch set applied onto the upstream TUI sources during build.
- Rebuild should validate cargo presence, show helpful error if missing, and suggest installing rustup.
- Consider checksum of upstream to detect drift and warn users.

## How to Verify
- Scaffold with sources:
  - Command: `chi-admin init . --binary-name=mypro --config=.tui/ --include-src`
  - Expect: `.tui/src/{banner.rs,background.rs,custom_hooks.rs}` present.
- Rebuild:
  - Command: `chi-admin rebuild`
  - Expect: successful cargo build; `.tui/bin/chi-tui` updated; `doctor` remains OK.
- Visual tweak smoke test:
  - Edit `.tui/src/banner.rs` to change header text.
  - Command: `chi-admin rebuild && mypro-ui`
  - Expect: header shows the modified text; navigate to `[[7]]` JSON viewer and confirm interaction unchanged.

## Acceptance Criteria
- `--include-src` creates the overlay files on Linux/macOS/Windows.
- `rebuild` succeeds with a standard Rust toolchain and updates the binary.
- TUI reflects overlay changes after rebuild.

## Discussion
- See `docs/tasks/021-admin-include-src-rebuild-discuss.md` for ongoing Q&A.
