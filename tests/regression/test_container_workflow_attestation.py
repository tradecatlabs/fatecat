from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_container_workflow_requires_registry_digest_and_attestation():
    workflow = (ROOT / ".github" / "workflows" / "container.yml").read_text(encoding="utf-8")

    assert "workflow_dispatch:" in workflow
    assert "push_image:" in workflow
    assert "id-token: write" in workflow
    assert "attestations: write" in workflow
    assert "artifact-metadata: write" in workflow
    assert "actions/upload-artifact@v4" in workflow
    assert "bash scripts/release-artifacts.sh" in workflow
    assert "docker buildx imagetools inspect" in workflow
    assert 'digest="$(docker buildx imagetools inspect' in workflow
    assert "actions/attest@v4" in workflow
    assert "subject-name: ${{ steps.push_main.outputs.image }}" in workflow
    assert "subject-digest: ${{ steps.push_main.outputs.digest }}" in workflow
    assert "subject-name: ${{ steps.push_release.outputs.image }}" in workflow
    assert "subject-digest: ${{ steps.push_release.outputs.digest }}" in workflow
    assert workflow.count("push-to-registry: true") >= 2
    assert 'gh attestation verify "oci://${{ steps.push_main.outputs.pushed_ref }}"' in workflow
    assert 'gh attestation verify "oci://${{ steps.push_release.outputs.pushed_ref }}"' in workflow
    assert "attestation-url" in workflow


def test_release_gate_declares_registry_attestation_evidence():
    gate = json.loads((ROOT / "contracts" / "fate" / "delivery" / "release-gate.json").read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "contracts" / "fate" / "delivery" / "registry.json").read_text(encoding="utf-8"))

    evidence = {item["id"]: item for item in gate["requiredEvidence"]}
    container = evidence["evidence.container_digest"]
    accepted = "\n".join(container["acceptedEvidence"])
    external_gate = "\n".join(gate["externalVerification"])
    external_registry = "\n".join(registry["releaseGate"]["externalVerification"])

    assert "GitHub artifact attestation" in accepted
    assert "gh attestation verify oci://ghcr.io/<owner>/fatecat-delivery@sha256:<64 hex>" in accepted
    assert "gh workflow run container.yml -f push_image=true" in external_gate
    assert "gh attestation verify oci://ghcr.io/<owner>/fatecat-delivery@sha256:<64 hex>" in external_gate
    assert "gh workflow run container.yml -f push_image=true" in external_registry
