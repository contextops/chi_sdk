# Security Policy

Supported versions
- Active development: main branch (pre-1.0)
- Releases: latest minor/patch versions

Reporting a vulnerability
- Please open a private security advisory or email the maintainers listed in `python-chi-sdk/pyproject.toml`.
- Provide a minimal reproduction, affected versions, and impact.
- We will acknowledge receipt within 72 hours and coordinate a fix and disclosure timeline.

Best practices
- Avoid executing untrusted backends. Prefer `CHI_TUI_JSON=1` and envelope validation.
- Keep dependencies up to date; run `pre-commit` hooks and CI.
