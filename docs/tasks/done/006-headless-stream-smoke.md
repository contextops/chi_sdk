Title: Headless smoke — progress stream verification
Status: done
Why:
- Quick, non-interactive check of NDJSON progress flow.
Scope:
- Add a small script/target to run `example-app simulate-progress` via TUI in headless mode for N ticks and capture summary JSON.
- Verify `status` appears during progress and JSON view switches on completion.
Acceptance:
- Script exits 0; JSON summary has `ok=true` and non-empty `status` at least once.
Notes:
- Use `CHI_TUI_HEADLESS=1` and `CHI_TUI_TICKS` envs.
