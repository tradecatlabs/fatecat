#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tomllib
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SBOM_FILENAME = "sbom.cyclonedx.json"
PROVENANCE_FILENAME = "provenance.slsa.json"
MANIFEST_FILENAME = "release-artifacts-manifest.json"

CORE_MATERIALS = (
    "pyproject.toml",
    "requirements.lock.txt",
    "requirements-dev.lock.txt",
    "infra/docker/Dockerfile.delivery",
    "infra/docker/entrypoint.delivery.sh",
    "contracts/fate/delivery/release-gate.json",
    "contracts/fate/delivery/registry.json",
    "contracts/fate/capabilities/registry.json",
    "scripts/live-release-gate.py",
    "scripts/release-artifacts.py",
)

SENSITIVE_ASSIGNMENT_NAMES = ("token", "secret", "password", "passwd", "private_key")
SENSITIVE_TOKENS = tuple(f"{name}=" for name in SENSITIVE_ASSIGNMENT_NAMES) + ("BEGIN RSA", "BEGIN OPENSSH")


@dataclass(frozen=True)
class Dependency:
    name: str
    version: str
    scope: str
    source: str


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def run_capture(args: list[str], *, timeout_seconds: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )


def git_value(*args: str) -> str:
    result = run_capture(["git", *args], timeout_seconds=10)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def git_status_counts() -> dict[str, Any]:
    result = run_capture(["git", "status", "--porcelain"], timeout_seconds=10)
    if result.returncode != 0:
        return {"dirtyCount": 0, "untrackedCount": 0, "clean": True}
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    untracked = [line for line in lines if line.startswith("??")]
    return {"dirtyCount": len(lines), "untrackedCount": len(untracked), "clean": len(lines) == 0}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_pyproject() -> dict[str, Any]:
    with (REPO_ROOT / "pyproject.toml").open("rb") as fh:
        return tomllib.load(fh)


def parse_lockfile(path: Path, *, scope: str) -> list[Dependency]:
    dependencies: list[Dependency] = []
    if not path.exists():
        return dependencies
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "==" not in stripped:
            continue
        name, version = stripped.split("==", 1)
        name = name.strip()
        version = version.strip()
        if name and version:
            dependencies.append(Dependency(name=name, version=version, scope=scope, source=path.name))
    return dependencies


def normalized_dependencies() -> list[Dependency]:
    seen: dict[tuple[str, str], Dependency] = {}
    for dep in parse_lockfile(REPO_ROOT / "requirements.lock.txt", scope="required"):
        seen[(dep.name.lower(), dep.scope)] = dep
    for dep in parse_lockfile(REPO_ROOT / "requirements-dev.lock.txt", scope="optional"):
        key = (dep.name.lower(), dep.scope)
        if key not in seen:
            seen[key] = dep
    return sorted(seen.values(), key=lambda item: (item.scope, item.name.lower()))


def material_entry(path_text: str) -> dict[str, Any]:
    path = REPO_ROOT / path_text
    return {
        "uri": path_text,
        "digest": {"sha256": sha256_file(path)} if path.is_file() else {},
        "exists": path.is_file(),
    }


def build_sbom(*, generated_at: str, git_commit: str) -> dict[str, Any]:
    pyproject = load_pyproject()
    project = pyproject.get("project", {})
    dependencies = normalized_dependencies()
    components = [
        {
            "type": "application",
            "name": project.get("name", "fatecat"),
            "version": project.get("version", "0.0.0"),
            "bom-ref": "pkg:generic/fatecat",
            "licenses": [{"license": {"id": "MIT"}}],
        }
    ]
    for dep in dependencies:
        components.append(
            {
                "type": "library",
                "name": dep.name,
                "version": dep.version,
                "scope": dep.scope,
                "bom-ref": f"pkg:pypi/{dep.name.lower()}@{dep.version}",
                "purl": f"pkg:pypi/{dep.name.lower()}@{dep.version}",
                "properties": [{"name": "fatecat:lockfile", "value": dep.source}],
            }
        )
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, f'fatecat:{git_commit}:sbom')}",
        "version": 1,
        "metadata": {
            "timestamp": generated_at,
            "tools": [{"vendor": "TradeCat Labs", "name": "scripts/release-artifacts.py", "version": "1"}],
            "component": components[0],
            "properties": [
                {"name": "fatecat:gitCommit", "value": git_commit},
                {"name": "fatecat:source", "value": "pyproject.toml + requirements lock files"},
                {"name": "fatecat:boundary", "value": "local SBOM baseline; not a registry attestation"},
            ],
        },
        "components": components,
    }


def build_provenance(
    *,
    generated_at: str,
    git_commit: str,
    branch: str,
    sbom_digest: str,
) -> dict[str, Any]:
    materials = [material_entry(path) for path in CORE_MATERIALS]
    materials = [item for item in materials if item["exists"]]
    git_status = git_status_counts()
    return {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [
            {
                "name": SBOM_FILENAME,
                "digest": {"sha256": sbom_digest},
            }
        ],
        "predicateType": "https://slsa.dev/provenance/v1",
        "predicate": {
            "buildDefinition": {
                "buildType": "https://tradecatlabs.github.io/fatecat/buildtypes/local-release-artifacts/v1",
                "externalParameters": {
                    "repository": "local-worktree",
                    "branch": branch,
                    "commit": git_commit,
                    "dirty": not git_status["clean"],
                },
                "internalParameters": {
                    "script": "scripts/release-artifacts.py",
                    "sbomFormat": "CycloneDX 1.5 compatible",
                    "provenanceFormat": "in-toto statement with SLSA v1 predicate",
                },
                "resolvedDependencies": materials,
            },
            "runDetails": {
                "builder": {"id": "fatecat-local-release-artifacts"},
                "metadata": {
                    "invocationId": str(uuid.uuid5(uuid.NAMESPACE_URL, f"fatecat:{git_commit}:{generated_at}")),
                    "startedOn": generated_at,
                    "finishedOn": generated_at,
                },
                "byproducts": [
                    {"name": SBOM_FILENAME, "digest": {"sha256": sbom_digest}},
                    {"name": "gitDirtyCount", "value": str(git_status["dirtyCount"])},
                    {"name": "gitUntrackedCount", "value": str(git_status["untrackedCount"])},
                ],
            },
        },
    }


def artifact_entry(output_dir: Path, filename: str, *, artifact_type: str) -> dict[str, Any]:
    path = output_dir / filename
    return {
        "type": artifact_type,
        "path": str(path),
        "filename": filename,
        "sizeBytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def contains_sensitive_value(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    return any(marker.lower() in lowered for marker in SENSITIVE_TOKENS)


def verify_artifacts(output_dir: Path) -> list[str]:
    errors: list[str] = []
    sbom_path = output_dir / SBOM_FILENAME
    provenance_path = output_dir / PROVENANCE_FILENAME
    manifest_path = output_dir / MANIFEST_FILENAME
    for path in (sbom_path, provenance_path, manifest_path):
        if not path.is_file():
            errors.append(f"missing artifact: {path}")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON {path}: {exc}")
        if contains_sensitive_value(path):
            errors.append(f"artifact appears to contain sensitive value marker: {path}")

    if not manifest_path.is_file():
        return errors
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in manifest.get("artifacts", []):
        path = Path(item["path"])
        if not path.is_file():
            errors.append(f"manifest artifact path missing: {path}")
            continue
        actual = sha256_file(path)
        if actual != item.get("sha256"):
            errors.append(f"manifest sha256 mismatch: {path}")

    if sbom_path.is_file():
        sbom = json.loads(sbom_path.read_text(encoding="utf-8"))
        if sbom.get("bomFormat") != "CycloneDX":
            errors.append("SBOM is not CycloneDX compatible")
        if not sbom.get("components"):
            errors.append("SBOM has no components")
    if provenance_path.is_file():
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        if provenance.get("_type") != "https://in-toto.io/Statement/v1":
            errors.append("provenance is not an in-toto statement")
        if provenance.get("predicateType") != "https://slsa.dev/provenance/v1":
            errors.append("provenance predicateType is not SLSA v1")
    return errors


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def generate_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_at = utc_now()
    branch = git_value("rev-parse", "--abbrev-ref", "HEAD")
    commit = git_value("rev-parse", "--verify", "HEAD")
    sbom = build_sbom(generated_at=generated_at, git_commit=commit)
    sbom_path = output_dir / SBOM_FILENAME
    write_json(sbom_path, sbom)
    provenance = build_provenance(
        generated_at=generated_at,
        git_commit=commit,
        branch=branch,
        sbom_digest=sha256_file(sbom_path),
    )
    provenance_path = output_dir / PROVENANCE_FILENAME
    write_json(provenance_path, provenance)
    artifacts = [
        artifact_entry(output_dir, SBOM_FILENAME, artifact_type="sbom"),
        artifact_entry(output_dir, PROVENANCE_FILENAME, artifact_type="provenance"),
    ]
    manifest = {
        "schemaVersion": 1,
        "generatedAt": generated_at,
        "resourceType": "ReleaseArtifactManifest",
        "apiVersion": "fatecat.tradecatlabs/v1",
        "git": {
            "branch": branch,
            "commit": commit,
            **git_status_counts(),
        },
        "artifacts": artifacts,
        "privacyBoundary": "Release artifacts contain dependency names, versions, source file hashes and git metadata only; no token, secret, DSN, user report or production log body.",
        "localVerification": [
            f"bash scripts/release-artifacts.sh --verify-dir {output_dir}",
            "bash scripts/live-release-gate.sh --sbom-path <sbom> --provenance-path <provenance>",
        ],
        "limitations": [
            "Local SBOM/provenance baseline is not a remote CI attestation.",
            "Container image digest and registry signature are not generated by this script.",
            "Dirty worktree is recorded but does not fail local artifact generation.",
        ],
    }
    write_json(output_dir / MANIFEST_FILENAME, manifest)
    return manifest


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate or verify FateCat release artifacts")
    parser.add_argument(
        "--output-dir", default="infra/runtime/local-state/release-artifacts", help="artifact output dir"
    )
    parser.add_argument("--verify-dir", default="", help="verify an existing artifact dir instead of generating")
    parser.add_argument("--summary-json", default="", help="write machine-readable summary")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    target_dir = Path(args.verify_dir or args.output_dir)
    if not target_dir.is_absolute():
        target_dir = REPO_ROOT / target_dir
    manifest = None if args.verify_dir else generate_artifacts(target_dir)
    errors = verify_artifacts(target_dir)
    status = "failed" if errors else "passed"
    if manifest is None and (target_dir / MANIFEST_FILENAME).is_file():
        manifest = json.loads((target_dir / MANIFEST_FILENAME).read_text(encoding="utf-8"))
    summary = {
        "schemaVersion": 1,
        "status": status,
        "outputDir": str(target_dir),
        "artifacts": len((manifest or {}).get("artifacts", [])),
        "sbomPath": str(target_dir / SBOM_FILENAME),
        "provenancePath": str(target_dir / PROVENANCE_FILENAME),
        "manifestPath": str(target_dir / MANIFEST_FILENAME),
        "errors": errors,
    }
    if args.summary_json:
        summary_path = Path(args.summary_json)
        if not summary_path.is_absolute():
            summary_path = REPO_ROOT / summary_path
        write_json(summary_path, summary)
    print(json.dumps(summary, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
