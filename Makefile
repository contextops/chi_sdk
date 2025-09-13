PY := .venv/bin/python

.PHONY: lint lint-rust lint-py test test-rust test-py run smoke fmt fmt-rust fmt-py

lint: lint-py lint-rust


lint-py:
	@ruff check .
	@black --check .
	@mypy python-chi-sdk

lint-rust:
	@cd rust-tui && cargo fmt --all -- --check
	@cd rust-tui && cargo clippy --all-targets -- -D warnings

test: test-py test-rust

test-py:
	@python -m pip install -e python-chi-sdk -e example-apps/example-app >/dev/null 2>&1 || true
	@env PYTHONPATH=python-chi-sdk/src:example-apps/example-app/src pytest -q python-chi-sdk/tests

test-rust:
	@cd rust-tui && cargo test -q

run:
	@CHI_APP_BIN=example-app CHI_TUI_JSON=1 example-app ui

smoke:
	@cd rust-tui && CHI_TUI_HEADLESS=1 CHI_TUI_TICKS=15 cargo run -q

smoke-progress:
	@python -m pip install -e python-chi-sdk -e example-apps/example-app >/dev/null 2>&1 || true
	@cd rust-tui && CHI_TUI_HEADLESS=1 CHI_TUI_TICKS=30 CHI_TUI_HEADLESS_ENTER_ID=progress_demo CHI_TUI_SMOKE_SUMMARY=1 PATH="`python -c 'import site,sys;print(site.USER_BASE+"/bin")'`:`pwd`/../.venv/bin:${PATH}" cargo run -q


smoke-ci:
	@python -m pip install -e python-chi-sdk -e example-apps/example-app >/dev/null 2>&1 || true
	@bash -c 'cd rust-tui && CHI_TUI_HEADLESS=1 CHI_TUI_TICKS=40 CHI_TUI_HEADLESS_ENTER_ID=progress_demo CHI_TUI_SMOKE_SUMMARY=1 cargo run -q | tail -n 1 | python -c "import json,sys; d=json.load(sys.stdin); req=[\"ok\",\"progress_seen\",\"status_seen\",\"result_present\"]; \
	allok=all(d.get(k) for k in req); print(json.dumps(d)); sys.exit(0 if allok else 2)"'

fmt: fmt-py fmt-rust

fmt-py:
	@black .

fmt-rust:
	@cd rust-tui && cargo fmt --all
