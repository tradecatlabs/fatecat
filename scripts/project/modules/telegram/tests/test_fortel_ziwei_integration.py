#!/usr/bin/env python3
"""测试紫微 Node 依赖准备逻辑。"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from fortel_ziwei_integration import _ensure_iztro_ready, _resolve_node_package_entry


def test_resolve_node_package_entry_uses_package_main(tmp_path):
    repo_dir = tmp_path / "iztro-main"
    repo_dir.mkdir()
    (repo_dir / "package.json").write_text(
        json.dumps({"name": "iztro", "main": "build/index.js"}, ensure_ascii=False),
        encoding="utf-8",
    )

    entry_path = _resolve_node_package_entry(repo_dir)

    assert entry_path == repo_dir / "build" / "index.js"


def test_ensure_iztro_ready_installs_and_builds_when_entry_missing(tmp_path, monkeypatch):
    repo_dir = tmp_path / "iztro-main"
    repo_dir.mkdir()
    (repo_dir / "package.json").write_text(
        json.dumps(
            {
                "name": "iztro",
                "main": "lib/index.js",
                "scripts": {"build": "tsc"},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    calls: list[list[str]] = []

    def fake_run(repo_dir_arg, args, timeout):
        calls.append(args)
        if args[:1] == ["install"]:
            (repo_dir_arg / "node_modules").mkdir()
        if args[:2] == ["run", "build"]:
            lib_dir = repo_dir_arg / "lib"
            lib_dir.mkdir()
            (lib_dir / "index.js").write_text("module.exports = {};\n", encoding="utf-8")

    monkeypatch.setattr("fortel_ziwei_integration._run_npm_command", fake_run)

    entry_path = _ensure_iztro_ready(repo_dir)

    assert entry_path == repo_dir / "lib" / "index.js"
    assert entry_path.exists()
    assert calls == [["install", "--no-fund", "--no-audit"], ["run", "build"]]
