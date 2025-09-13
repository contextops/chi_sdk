Title: Pane B Menu — finalize offset model
Status: done
Why:
- Unify naming and fields for Pane B list offset; tidy code.
Scope:
- Replace reused `b_scroll_y` with explicit `b_menu_offset` (or generalize to `b_list_offset`).
- Adjust rendering and key handlers accordingly.
Acceptance:
- Behavior unchanged; names clearer; `ui.rs` slimmer.
Notes:
- Do after registry/widget extraction if possible.
