from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_quick_workflow_covers_pull_requests_and_main_pushes():
    workflow = (ROOT / ".github" / "workflows" / "quick.yml").read_text(encoding="utf-8")

    assert "pull_request:" in workflow
    assert "push:" in workflow
    assert "- main" in workflow
    assert "workflow_dispatch:" in workflow
    assert "bash scripts/local-ci.sh --profile quick --with-dev" in workflow
    assert 'PYTHONDONTWRITEBYTECODE: "1"' in workflow
    assert "cancel-in-progress: true" in workflow
    assert "actions/upload-artifact@v7" in workflow


def test_heavy_release_workflows_remain_explicitly_triggered():
    acceptance = (ROOT / ".github" / "workflows" / "acceptance.yml").read_text(encoding="utf-8")
    container = (ROOT / ".github" / "workflows" / "container.yml").read_text(encoding="utf-8")
    hf_deploy = (ROOT / ".github" / "workflows" / "hf-space-deploy.yml").read_text(encoding="utf-8")

    for workflow in (acceptance, container, hf_deploy):
        assert "workflow_dispatch:" in workflow
        assert "pull_request:" not in workflow
        assert "push:" not in workflow
