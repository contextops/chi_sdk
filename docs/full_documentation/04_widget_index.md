# Widget Index

This section lists available widget specs and links to details.

## result_viewer (renderer)
- Unified renderer used by JSON viewer, Pane B results, and nested panels
- Keys: arrows/PgUp/PgDn/Home/End; `w` wrap; `j` raw JSON toggle
- Details: `../../docs/widgets/result_viewer.md`

## menu
- Spec fields: `type: menu`, `spec` (path) or `config` (inline AppConfig)
- Renders a right-pane menu; routes key events to scroll/select
- Details: `../../docs/widgets/menu.md`

## json_viewer
- Spec fields: `type: json_viewer`, `cmd`, `yaml`
- Delegates to the unified result viewer; async content load via effects; keys `j`/`w` supported
- Details: `../../docs/widgets/json_viewer.md`

## panel
- Spec fields: `type: panel`, `layout`, `size`, `a`, `b`
- Nested panel inside Pane B; preserves nested focus
- Details: `../../docs/widgets/panel.md`

## form
- Spec fields: `type: form`, `title`, `fields[]`, `submit.command`
- Supports text/checkbox/select/multiselect/number/array/textarea
- Dynamic options via `options_cmd` and `unwrap`
- Textarea modal: Ctrl+S save, Esc cancel
- Details: `../../docs/widgets/form.md`

See also: `../widgets_spec.md` for quick field references.
## markdown
- Spec fields: `type: markdown`, `path` (or inline `text`)
- Renders Markdown; fenced code blocks highlighted via syntect; wrap toggle `w`
- Details: `../../docs/widgets/markdown.md`

## watchdog
- Spec fields: `type: watchdog`, `commands`, optional `sequential: true`
- Splits pane vertically and streams each command's output; shared scroll
- Details: `../../docs/widgets/watchdog.md`
