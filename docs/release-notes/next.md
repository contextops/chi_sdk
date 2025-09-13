# Unreleased

Fixes and improvements pending next release.

Highlights

- Config resolution simplified: TUI now anchors exclusively on `CHI_TUI_CONFIG_DIR` and expects `chi-index.yaml` inside it. Relative paths resolve against `CHI_TUI_CONFIG_DIR`. If not set, the TUI auto-discovers `chi-index.yaml` (in `CWD`, `CWD/.tui`, ancestors' `.tui`, or `~/.tui`).
- Watchdog UX: stats footer redesigned for clarity. New format `● LABEL  × COUNT` (color-coded: ERROR red, WARN yellow, INFO cyan, DEBUG blue) with a subtle background to separate it from logs. No changes to spec — continue using `stats: [{label, regexp}]`.
- Watchdog: auto-follow enabled by default. Manual scroll (↑/↓/PgUp/PgDn/Home) pauses follow; press `End` or `f` to resume and jump to the latest lines. Tab/Shift+Tab cycles the focused log section; only the focused section is highlighted and responds to scroll keys.
- Watchdog: new external mode — add `external_check_cmd` (and optional `external_kill_cmd`) to detect processes uruchomione poza TUI. Gdy wykryte, menu pokazuje wskaźnik `* running (external init)`. W tym trybie widget nie spawnuje komend; klawisz `s` wywołuje komendę kill, `r` jest niedostępne.
- Docs: replaced `chi-admin run-demo` with simplified flows: `chi-admin ensure-chi` (compile/download) and direct `your-app ui` / `chi-tui` usage; clarified headless/cargo workflows and environment variables.

Housekeeping

- Lints: clippy warnings addressed; fmt clean.
- Docs refreshed in widgets and guides.
