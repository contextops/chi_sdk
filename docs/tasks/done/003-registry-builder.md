Title: Registry — Build widgets from specs (spec→widget)
Status: done
Why:
- YAML/JSON specs should resolve to concrete widgets via a central registry.
Scope:
- Extend `chi_core/registry.rs` to return constructed widgets (trait object) instead of Effects where applicable.
- Add spec-normalizer: unify cmd/yaml/spec fields into a stable internal spec.
- Route unknown types back to Effects (compat mode) for incremental migration.
Acceptance:
- Existing YAML screens still work.
- Unit test: spec→widget mapping for json_viewer, menu, panel.
Notes:
- Keep panel submit/loader effects in router until form moves.
