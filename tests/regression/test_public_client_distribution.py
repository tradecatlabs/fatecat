from __future__ import annotations

import importlib.util
import json
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "contracts" / "fate" / "developer" / "public-client-distribution.json"
VENDOR_MANIFEST_PATH = ROOT / "tools" / "reference-repos" / "vendor_sources.json"
SMOKE_PATH = ROOT / "scripts" / "public-client-package-smoke.py"
CLIENT_ROOT = ROOT / "apps" / "developer-clients" / "python"


def _load_smoke_module():
    spec = importlib.util.spec_from_file_location("fatecat_public_client_package_smoke", SMOKE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_public_client_distribution_separates_client_and_restricted_runtime():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    root_project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    client_project = tomllib.loads((CLIENT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert manifest["publicClient"]["packageName"] == "fatecat-client"
    assert manifest["publicClient"]["runtimeDependencies"] == []
    assert manifest["publicClient"]["executionModel"] == "remote_http_api_only"
    assert manifest["publicClient"]["distributionAllowed"] is True
    assert manifest["publicClient"]["serverImportsAllowed"] is False
    assert manifest["restrictedServerRuntime"]["publicRegistryPublishAllowed"] is False
    assert root_project["tool"]["fatecat"]["distribution"]["artifact-class"] == "restricted_server_runtime"
    assert root_project["tool"]["fatecat"]["distribution"]["public-registry-publish"] is False
    assert client_project["project"]["dependencies"] == []


def test_public_client_policy_preserves_unknown_vendor_license_boundaries():
    distribution = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    vendor_manifest = json.loads(VENDOR_MANIFEST_PATH.read_text(encoding="utf-8"))
    vendors = {item["id"]: item for item in vendor_manifest["required"]}
    restricted = {item["id"]: item for item in distribution["restrictedServerRuntime"]["unknownLicenseAssets"]}

    assert set(restricted) == {"bazi-1", "sxwnl"}
    for vendor_id, expected in restricted.items():
        actual = vendors[vendor_id]
        assert actual["license"] == expected["license"] == "NOASSERTION"
        assert actual["licenseStatus"] == expected["licenseStatus"] == "missing_upstream_license"
        assert actual["distributionAllowed"] is expected["distributionAllowed"] is False
        assert actual["usageRole"] == expected["usageRole"]


def test_public_client_archive_allowlist_rejects_server_members():
    smoke = _load_smoke_module()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    valid_members = [
        "fatecat_client/__init__.py",
        "fatecat_client/client.py",
        "fatecat_client/py.typed",
        "fatecat_client-0.1.0.dist-info/METADATA",
    ]

    assert smoke.validate_archive_members(valid_members, manifest, "wheel") == valid_members
    with pytest.raises(smoke.PublicClientPackageError, match="受限成员"):
        smoke.validate_archive_members([*valid_members, "fate_core/kernel/bazi_calculator.py"], manifest, "wheel")
    with pytest.raises(smoke.PublicClientPackageError, match="越界"):
        smoke.validate_archive_members([*valid_members, "/tmp/escaped.py"], manifest, "wheel")
    with pytest.raises(smoke.PublicClientPackageError, match="越界"):
        smoke.validate_archive_members([*valid_members, "C:/escaped.py"], manifest, "wheel")


def test_public_client_source_has_no_server_or_vendor_imports():
    source = (CLIENT_ROOT / "src" / "fatecat_client" / "client.py").read_text(encoding="utf-8").casefold()
    for forbidden in ("fate_core", "fatecat-delivery", "bazi-1", "sxwnl", "reference-repos"):
        assert forbidden not in source
