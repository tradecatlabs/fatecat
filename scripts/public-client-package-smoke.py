#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tarfile
import threading
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKAGE_ROOT = REPO_ROOT / "apps" / "developer-clients" / "python"
DEFAULT_MANIFEST = REPO_ROOT / "contracts" / "fate" / "developer" / "public-client-distribution.json"
DEFAULT_OUTPUT = Path("/tmp/fatecat-public-client-package-smoke")


class PublicClientPackageError(RuntimeError):
    """公开客户端分发闭包不满足契约。"""


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PublicClientPackageError(f"无法读取分发 manifest: {path}: {exc}") from exc
    if payload.get("kind") != "fatecat.public_client_distribution":
        raise PublicClientPackageError(f"未知分发 manifest: {path}")
    return payload


def _normalize_members(members: list[str], archive_kind: str) -> list[str]:
    normalized: list[str] = []
    for raw_name in members:
        candidate = raw_name.replace("\\", "/")
        if candidate.startswith("/") or re.match(r"^[A-Za-z]:/", candidate):
            raise PublicClientPackageError(f"archive member 越界: {raw_name}")
        name = candidate.strip("/")
        if archive_kind == "sdist" and "/" in name:
            name = name.split("/", 1)[1]
        elif archive_kind == "sdist":
            name = ""
        if not name:
            continue
        parts = Path(name).parts
        if ".." in parts:
            raise PublicClientPackageError(f"archive member 越界: {raw_name}")
        normalized.append(name)
    return normalized


def validate_archive_members(members: list[str], manifest: dict[str, Any], archive_kind: str) -> list[str]:
    if archive_kind not in {"wheel", "sdist"}:
        raise ValueError(f"unsupported archive kind: {archive_kind}")
    policy = manifest["archivePolicy"]
    normalized = _normalize_members(members, archive_kind)
    forbidden = tuple(fragment.casefold() for fragment in policy["forbiddenFragments"])
    for name in normalized:
        lowered = name.casefold()
        if any(fragment in lowered for fragment in forbidden):
            raise PublicClientPackageError(f"archive 含受限成员: {name}")
        if not any(fnmatch.fnmatchcase(name, pattern) for pattern in policy["allowedMembers"]):
            raise PublicClientPackageError(f"archive 成员不在 allowlist: {name}")
    required_key = "requiredWheelMembers" if archive_kind == "wheel" else "requiredSdistMembers"
    missing = sorted(set(policy[required_key]) - set(normalized))
    if missing:
        raise PublicClientPackageError(f"archive 缺少必要成员: {', '.join(missing)}")
    return normalized


def _archive_members(path: Path, archive_kind: str) -> list[str]:
    if archive_kind == "wheel":
        with zipfile.ZipFile(path) as archive:
            return archive.namelist()
    with tarfile.open(path, mode="r:gz") as archive:
        return archive.getnames()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class _SmokeHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send_json({"status": "ok"})
            return
        if self.path == "/capabilities":
            self._send_json({"items": [{"capabilityId": "bazi"}]})
            return
        self.send_error(404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/capabilities/bazi/calculate":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode("utf-8"))
        self._send_json({"success": True, "capabilityId": "bazi", "echo": payload})

    def _send_json(self, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args: object) -> None:
        return


def _run_clean_room_smoke(python: Path) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _SmokeHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}"
    code = """
from fatecat_client import FateCatClient
import os

client = FateCatClient(os.environ["FATECAT_CLIENT_SMOKE_URL"], timeout_seconds=2)
assert client.health() == {"status": "ok"}
assert client.capabilities()["items"][0]["capabilityId"] == "bazi"
result = client.calculate("bazi", {"sample": "public-client-smoke"})
assert result["success"] is True
assert result["echo"] == {"sample": "public-client-smoke"}
"""
    try:
        subprocess.run(
            [str(python), "-c", code],
            check=True,
            env={"FATECAT_CLIENT_SMOKE_URL": base_url},
            capture_output=True,
            text=True,
            timeout=30,
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def run(package_root: Path, manifest_path: Path, output_root: Path) -> dict[str, Any]:
    manifest = _load_manifest(manifest_path)
    if package_root.resolve() != (REPO_ROOT / manifest["publicClient"]["sourceRoot"]).resolve():
        raise PublicClientPackageError("package root 与 manifest 不一致")

    output_root.mkdir(parents=True, exist_ok=True)
    dist_dir = output_root / "dist"
    venv_dir = output_root / "venv"
    shutil.rmtree(dist_dir, ignore_errors=True)
    shutil.rmtree(venv_dir, ignore_errors=True)
    dist_dir.mkdir()

    subprocess.run(
        [sys.executable, "-m", "build", "--no-isolation", "--sdist", "--wheel", "--outdir", str(dist_dir)],
        cwd=package_root,
        check=True,
        timeout=120,
    )
    wheel = next(dist_dir.glob("*.whl"), None)
    sdist = next(dist_dir.glob("*.tar.gz"), None)
    if wheel is None or sdist is None:
        raise PublicClientPackageError("构建产物不完整")

    wheel_members = validate_archive_members(_archive_members(wheel, "wheel"), manifest, "wheel")
    sdist_members = validate_archive_members(_archive_members(sdist, "sdist"), manifest, "sdist")

    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True, timeout=60)
    clean_python = venv_dir / "bin" / "python"
    subprocess.run(
        [str(clean_python), "-m", "pip", "install", "--quiet", "--no-deps", str(wheel)],
        check=True,
        timeout=60,
    )
    _run_clean_room_smoke(clean_python)

    summary = {
        "schemaVersion": 1,
        "status": "passed",
        "package": manifest["publicClient"]["packageName"],
        "version": manifest["publicClient"]["version"],
        "registryStatus": manifest["packageRegistryStatus"],
        "wheel": {"path": str(wheel), "sha256": _sha256(wheel), "members": len(wheel_members)},
        "sdist": {"path": str(sdist), "sha256": _sha256(sdist), "members": len(sdist_members)},
        "runtimeDependencies": manifest["publicClient"]["runtimeDependencies"],
        "restrictedServerRuntime": manifest["restrictedServerRuntime"]["publicRegistryPublishAllowed"] is False,
        "externalConnectivity": "not_required_local_fixture",
    }
    (output_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="构建并验证 FateCat 公开 Python 客户端分发闭包")
    parser.add_argument("--package-root", type=Path, default=DEFAULT_PACKAGE_ROOT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        summary = run(args.package_root, args.manifest, args.output)
    except (OSError, subprocess.SubprocessError, PublicClientPackageError) as exc:
        print(f"public client package smoke failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
