Title: CI & DX — Makefile and GitHub Actions
Status: done
Why:
- Ensure quick checks and shared workflows.
Scope:
- Makefile: `lint` (ruff, fmt, clippy), `test` (pytest, cargo test), `run`.
- GitHub Actions: matrix for Rust (stable) and Python (3.11), run checks.
Acceptance:
- `make lint && make test` passes locally.
- CI green on PRs.
Notes:
- Headless smoke test can be added as separate task.
