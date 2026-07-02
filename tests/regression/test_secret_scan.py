from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCANNER_PATH = ROOT / "scripts" / "secret-scan.py"


def _load_scanner_module():
    spec = importlib.util.spec_from_file_location("fatecat_secret_scan", SCANNER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_secret_scan_detects_realistic_secret_without_exposing_value():
    scanner = _load_scanner_module()
    allowlist = scanner.load_allowlist()
    secret_value = "sk-" + ("A" * 24) + "bCDefGhIjKlMnOpQr"

    findings = scanner.scan_text("example.py", f"OPENAI_API_KEY={secret_value}\n", allowlist)

    assert len(findings) >= 1
    assert "openai_api_key" in {item.rule for item in findings}
    assert all(secret_value not in item.redacted for item in findings)
    assert all(item.fingerprint for item in findings)


def test_secret_scan_ignores_placeholders_and_function_calls():
    scanner = _load_scanner_module()
    allowlist = scanner.load_allowlist()
    content = "\n".join(
        [
            "FATE_BOT_TOKEN=${placeholder_token}",
            "request_id_token = _request_id_context.set(request_id)",
            "LLM_API_KEY=sk-your-openai-key-here",
        ]
    )

    findings = scanner.scan_text("scripts/example.sh", content, allowlist)

    assert findings == []


def test_secret_scan_cli_writes_summary(tmp_path):
    scanner = _load_scanner_module()
    output_json = tmp_path / "secret-scan.json"

    exit_code = scanner.main(["--output-json", str(output_json)])

    assert exit_code == 0
    stored = json.loads(output_json.read_text(encoding="utf-8"))
    assert stored["schemaVersion"] == 1
    assert stored["status"] == "passed"
    assert stored["summary"]["findingCount"] == 0
    assert "密钥原文" in stored["privacyBoundary"]
