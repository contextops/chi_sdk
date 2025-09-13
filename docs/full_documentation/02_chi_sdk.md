# Python CHI SDK

This section describes the Python SDK conventions and how to expose commands and schemas to the TUI.

## Overview
- Pydantic v2 models (`*In` / `*Out`) and Click commands via `@chi_command`
- CLI names: kebab-case; Python functions: snake_case
- No ad‑hoc prints — always emit a JSON envelope (`emit_ok`/`emit_error` used by the SDK)

## Example app commands
Commands are defined under `example-apps/example-app/src/example_app/cli.py` using `@chi_command`:
- `hello` — input: `HelloIn(name: str, shout: bool)`; output: `HelloOut(greeting: str)`
- `sum-numbers` — input: list of numbers; output: total and count
- `list-items`, `list-items-slow` — lists to drive dynamic/lazy screens
- `list-projects`, `list-tasks`, `task-detail` — nested navigation demos
- `simulate-progress` — streaming progress for TUI spinners
- `test-params` — numeric fields for auto‑mapping
- `validate-text` — text constraints demo

Run a command with a JSON envelope:

```
CHI_TUI_JSON=1 example-app hello --name Ada --shout
```

Output (abbrev.):

```
{ "ok": true, "type": "data", "data": { "greeting": "HELLO, ADA!" } }
```

Errors are reported as `{ ok: false, type: "error", data: { message, details } }`.

## Schema emission (`schema`)
The SDK adds a `schema` command to the CLI that emits machine‑readable contract metadata:

```
example-app schema
```

Abbreviated structure:

```
{
  "ok": true,
  "type": "data",
  "data": {
    "commands": [
      {
        "name": "hello",
        "description": "Say hello.",
        "input_schema": { "$schema": "https://json-schema.org/...", "type": "object", ... },
        "output_schema": { "type": "object", "properties": { "greeting": {"type":"string"} } }
      },
      ...
    ]
  }
}
```

TUI may use `input_schema` to auto‑map fields (text/number/array/select/multiselect/textarea).

## Naming & conventions
- Models: `*In` for inputs, `*Out` for outputs (e.g., `HelloIn`, `HelloOut`)
- CLI function names: snake_case; CLI command names: kebab-case
- All output goes through the envelope; no direct `print()` from commands

## Testing
- Use `pytest` and snapshot the JSON envelope for stability
- Keep behavior deterministic and back‑compatible where possible
- Aim for ≥80% coverage when coverage tooling is added

## Tips
- Force JSON envelope for ad‑hoc runs with `CHI_TUI_JSON=1`
- Use `example-app schema` in development to verify the contract and field types
