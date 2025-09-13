Title: Move schema→form mapping into widgets/form
Status: done
Why:
- Centralize form logic; simplify `app/mod.rs` and `ui.rs`.
Scope:
- Extract schema-driven form field mapping and YAML overrides from `app/mod.rs` into `widgets/form` module(s).
- Add unit tests for mapping (required, numbers, arrays, enums, overrides).
Acceptance:
- Form auto-mapping works as before on demo screens.
- Tests cover representative cases.
Notes:
- Keep submit/validation pipeline unchanged.
