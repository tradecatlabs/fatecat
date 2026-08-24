from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HYGIENE_SCRIPT = ROOT / "scripts" / "check-export-hygiene.sh"


def test_public_export_rejects_vendor_without_distribution_permission(tmp_path: Path):
    vendor_root = tmp_path / "tools" / "reference-repos"
    blocked_vendor = vendor_root / "github" / "blocked-engine"
    blocked_vendor.mkdir(parents=True)
    (blocked_vendor / "engine.py").write_text("VALUE = 1\n", encoding="utf-8")
    (vendor_root / "vendor_sources.json").write_text(
        json.dumps(
            {
                "required": [
                    {
                        "id": "blocked-engine",
                        "path": "github/blocked-engine",
                        "licenseStatus": "missing_upstream_license",
                        "distributionAllowed": False,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    internal = subprocess.run(["bash", str(HYGIENE_SCRIPT), str(tmp_path)], text=True, capture_output=True)
    public = subprocess.run(
        ["bash", str(HYGIENE_SCRIPT), str(tmp_path), "--public"],
        text=True,
        capture_output=True,
    )

    assert internal.returncode == 0
    assert public.returncode == 1
    assert "blocked-engine" in public.stderr
    assert "missing_upstream_license" in public.stderr


def test_lite_export_excludes_runtime_state_and_unselected_reference_assets():
    export_script = (ROOT / "scripts" / "export-runtime.sh").read_text(encoding="utf-8")

    assert "--exclude '.git'" in export_script
    assert "--exclude 'infra/runtime/local-state/'" in export_script
    assert "--exclude 'tools/reference-repos/web/'" in export_script
    assert "--exclude 'tools/reference-repos/datasets/'" in export_script
    assert "--exclude 'tools/reference-repos/github/*'" in export_script
    assert "导出目录必须为空，避免旧文件残留" in export_script
