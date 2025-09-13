Title: Registry Phase 1 — Extract Menu and JSON widgets
Status: done
Why:
- Reduce `ui.rs` complexity by moving rendering and key handling into widgets.
- Establish consistent widget trait usage for non-form components.
Scope:
- Add `MenuWidget` and `JsonViewerWidget` under `rust-tui/src/widgets/`.
- Move rendering and key handling from `ui.rs` to widgets.
- Keep public behavior unchanged; `ui.rs` only picks/dispatches to widgets.
Acceptance:
- `cargo check` and tests pass.
- Manual: menu selection and JSON scroll work as before.
Notes:
- Reuse existing helper styles from `theme.rs`.
