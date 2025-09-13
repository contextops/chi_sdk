from __future__ import annotations

import io
import json
import os
from click.testing import CliRunner
from unittest.mock import patch

from chi_sdk.admin import cli


class _Resp:
    def __init__(self, data: bytes):
        self._bio = io.BytesIO(data)

    def read(self, n: int = -1) -> bytes:
        return self._bio.read(n)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_admin_download_prefers_raw_asset(tmp_path):
    # Fake GitHub release JSON with a Linux raw asset
    assets = [
        {
            "name": "chi-tui-Linux",
            "browser_download_url": "https://example.invalid/chi-tui-Linux",
        }
    ]
    release_json = json.dumps({"assets": assets}).encode("utf-8")

    def fake_urlopen(req, timeout=0):
        # Distinguish JSON vs raw asset by URL string
        url = req if isinstance(req, str) else getattr(req, "full_url", "")
        if url.endswith("/releases/latest"):
            return _Resp(release_json)
        # raw asset content
        return _Resp(b"#!/bin/sh\necho chi-tui\n")

    env = os.environ.copy()
    # Force Linux pathing and cache location
    env["CHI_TUI_JSON"] = "1"
    env["XDG_CACHE_HOME"] = str(tmp_path)
    env["PATH"] = "/nonexistent"

    runner = CliRunner()
    with patch("urllib.request.urlopen", side_effect=fake_urlopen), patch(
        "platform.system", return_value="Linux"
    ), patch("platform.machine", return_value="x86_64"):
        res = runner.invoke(cli, ["download"], env=env)
    assert res.exit_code == 0
    out = json.loads(res.output)
    assert out["ok"] is True
    data = out["data"]
    # After merging chi-tui-bin into chi-sdk, download now just guides to pip install
    assert data["installed"] is False
    assert "pip install chi-sdk" in data["guidance"]
