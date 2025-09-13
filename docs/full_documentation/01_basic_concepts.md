# Basic Concepts

## Architecture
- Python CLI is the source of truth (logic, data, schemas)
- Rust TUI is a thin client that renders CLI JSON
- Contract: stable JSON envelope + `schema` command
- Output rendering is unified via a single ResultViewer (pretty human view + raw JSON toggle)

## JSON Envelope
- Top-level: `{ ok: bool, type: 'data'|'error'|'progress', data: {...} }`
- Stream mode: progress events (text, percent) + final result
- Snapshot tests ensure envelope stability

## Headless and JSON Modes
- `CHI_TUI_JSON=1` forces JSON from the CLI
- `CHI_TUI_HEADLESS=1` enables TUI smoke mode
- `CHI_TUI_TICKS=N` controls headless loop length

## Navigation & Panel
- Config-driven nav (`.tui/chi-index.yaml`)
- Panel view has Pane A (menu) and Pane B (content)
- Registry maps YAML specs → widgets, keeps UI code simple
