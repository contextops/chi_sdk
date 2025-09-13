Title: Registry Phase 2 — Widget‑first routing
Status: todo
Why:
- Unify spec→widget construction for non-form screens (menu, json_viewer) to reduce coupling in `app/ui` and make the registry the single place that resolves YAML/JSON specs.
- Continue migration started with PanelWidget; pave the way for form to move fully under registry later.

Scope:
- Add a spec normalizer in `chi_core/registry.rs` that folds variants (cmd/yaml/spec fields) into a stable internal spec.
- Implement builders that return concrete widgets (trait objects) for:
  - `menu` (AppConfig-like spec → MenuWidget)
  - `json_viewer` (cmd/yaml → JsonViewerWidget, using async load via existing effects where needed)
- Prefer registry resolution inside the pane YAML load path (or earlier), keeping a compatibility fallback to Effects for unknown or partial specs.
- Minimize `PaneContent` branches in `ui.rs` by hosting Pane B content as widgets where practical (without breaking current behavior).
- Keep autoload/lazy items compatible; children expansion should still function as before.
- Document supported fields for each widget spec under `docs/` with small examples.

Acceptance:
- Existing YAML screens continue to work without changes.
- Unit tests: spec→widget mapping for `menu` and `json_viewer`; unknown specs route back to Effects.
- No observable behavior changes in TUI; `cargo test` green; `make smoke-ci` passes.

Notes:
- Panel is already a widget; forms remain as-is for now (covered by a separate task).
- Headless smoke remains unchanged; registry mapping should be transparent for stream scenarios.
