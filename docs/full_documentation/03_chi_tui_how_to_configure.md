# Configuring the TUI

This chapter explains how to add screens and wire them into the TUI using YAML and the widget registry.

## Navigation (`.tui/chi-index.yaml`)
File: `.tui/chi-index.yaml` defines menu structure and screens for your application. Each item may be:
- Static header (`widget: header`)
- Command leaf (`command: ...`)
- Dynamic list (`widget: lazy_items` or `autoload_items` + `command` + `unwrap`)
- Panel (`widget: panel`) with Pane A/B sources

Top-level screen options:
- `auto_enter`: optional id of a menu item to auto-enter when the screen loads (focus remains on Pane A)
- `can_close`: whether Esc leaves panel view; defaults to `true`. Set `false` to lock the panel layout.

Items may include markers in titles for your own testing, but they are optional.

Example (excerpt):

```
menu:
  - id: "panel_yaml_demo"
    title: "Panel Demo (YAML json_viewer)"
    widget: "panel"
    panel_layout: "horizontal"
    panel_size: "1:1"
    pane_b_yaml: "panels/panel_b.yaml"
```

## Panel View
- Layout: `horizontal` or `vertical` (`panel_layout`)
- Ratio: `1:1`, `1:2`, `2:1`, `1:3`, `3:1`, `2:3`, `3:2` (`panel_size`)
- Pane A/B content sources:
  - Inline via `pane_a_cmd` / `pane_b_cmd` (CLI commands)
  - External YAML via `pane_a_yaml` / `pane_b_yaml`
  - Title override (Pane B): `pane_b_title: "…"` — sets the header title for widgets rendered in Pane B

### Example: JSON viewer in Pane B
1) Create `.tui/panels/panel_b.yaml`:

```
# Shows the result of a CLI command in Pane B
# Resolved via the widget registry

type: json_viewer
cmd: "example-app list-items"
```

2) Point nav item to it (`pane_b_yaml: .tui/panels/panel_b.yaml`).

Expected: Pane B renders JSON viewer; content loads asynchronously from the command.

### Example: Menu in Pane B
1) Create `.tui/panels/panel_b_menu.yaml`:

```
type: menu
spec: "chi-index.yaml"
```

Expected: Pane B renders a menu widget using the same AppConfig as the main nav.

## Widget Registry (spec → widget)
The registry normalizes/recognizes YAML specs and builds widgets early:
- `json_viewer`: fields `cmd` or `yaml` (path)
- `menu`: fields `spec` (path) or `config` (inline AppConfig)
- `panel`: inline nested panel (advanced)
- `form`: basic form spec (submit via `submit.command`)
- `markdown`: fields `path` (or `text` inline); fenced code blocks highlighted via syntect
- `watchdog`: fields `commands` (list of commands) and optional `sequential: true` to run one-by-one

Unknown specs fall back to the legacy loader paths; existing YAMLs continue to work unchanged.

## Streaming Commands
- On a menu item, set `stream: true` to force streaming behavior, including when a panel is open. The TUI will run the command in stream mode and render updates using the unified ResultViewer.

Example:
```yaml
- id: "streaming_list"
  title: "Streaming updates [[8]]"
  command: "${APP_BIN} list-streaming"
  stream: true
```

## Key Bindings (Pane B)
- Panel focus: Tab cycles across panes. If Pane B hosts a nested panel: `A → B.A → B.B → A` (Shift+Tab w odwrotnej kolejności). Otherwise: `A ↔ B`.
- JSON/Result viewer: Up/Down/PageUp/PageDown/Home/End; `w` toggles wrap; `j` toggles raw JSON
- Form: Enter edits fields; Space toggles checkbox/multiselect; Ctrl+S saves textarea modal; Esc cancels textarea modal

## Headless/Smoke
- `CHI_TUI_HEADLESS=1` runs the app headlessly
- `CHI_TUI_TICKS=10` sets loop length; `CHI_TUI_SMOKE_SUMMARY=1` prints a summary
- `CHI_TUI_HEADLESS_ENTER_ID=<id>` selects a menu item by id on start

## How to verify (examples)
- JSON viewer wiring
  - `example-app ui`
  - Wejście do pozycji z `pane_b_yaml: panels/panel_b.yaml` powinno pokazać wynik w widoku JSON.
- Menu wiring
  - Wejście do pozycji z `type: menu` i `spec: chi-index.yaml` powinno pokazać przewijalne menu.
- Form interactions
  - Enter `[[22]]` (Text Area) → Enter opens modal; Ctrl+S saves; Esc cancels.
- Markdown
  - Enter `[[23]]` (Markdown) → Pane B shows README markdown with highlighted code blocks; `w` toggles wrapping.
- Watchdog
  - Enter `[[24]]` (Watchdog) → Pane B splits into two logs; with `sequential: true` the second starts after the first finishes.
