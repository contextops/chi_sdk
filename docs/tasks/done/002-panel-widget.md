Title: PanelWidget — Nested A/B pane as a widget
Status: done
Why:
- Concentrate nested panel layout and focus logic outside `ui.rs`.
- Prepare for registry-driven composition.
Scope:
- Create `PanelWidget` with props: layout, ratio, A/B contents.
- Move nested focus handling (B.A/B.B) and drawing here.
- `ui.rs` delegates to `PanelWidget` when a panel is requested.
Acceptance:
- Tab/Shift-Tab cycle behavior remains as before (tests updated if needed).
- Manual: panel renders and behaves identically.
Notes:
- Keep effects/messages flowing through existing router for now.
