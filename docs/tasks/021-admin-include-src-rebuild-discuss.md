# 021 — Admin Include-Src + Rebuild — Discussion

Use this thread to track decisions. When replying to a question, prefix your response lines with:

>>

## Questions

1) How do we layer `.tui/src` onto the upstream code: full workspace template vs. patching selected modules?
   
2) Should we lock a compatible TUI version in `.tui/config.yaml` to avoid mismatch?
   
3) Where to emit build logs and artifacts: keep only final binary in `.tui/bin/` or store a `.tui/target/` cache?
