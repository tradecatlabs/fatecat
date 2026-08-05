from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOP_DIR = ROOT / "governance" / "processes" / "sops"
INDEX_PATH = SOP_DIR / "INDEX.md"
CAPABILITY_REGISTRY_PATH = ROOT / "contracts" / "fate" / "capabilities" / "registry.json"

REQUIRED_HEADINGS = (
    "## 任务定义",
    "## 当前状态",
    "## 适用场景",
    "## 输入要求",
    "## 前置条件",
    "## 默认工具链",
    "## 固定路径",
    "## 成熟参数",
    "## 分步执行流程",
    "## 幂等与增量策略",
    "## 限速与并发规则",
    "## 输出目录",
    "## 命名规范",
    "## 质量验收门禁",
    "## 失败处理",
    "## 恢复与重试策略",
    "## 安全边界",
    "## 临时文件清理",
    "## 运行记录登记",
    "## 明确禁止事项",
)


def _sop_paths() -> list[Path]:
    return sorted(path for path in SOP_DIR.glob("*.md") if path.name not in {"AGENTS.md", "INDEX.md"})


def _frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path}: 缺少 frontmatter"
    _, raw, _ = text.split("---", 2)
    result: dict[str, object] = {}
    for line in raw.strip().splitlines():
        key, separator, value = line.partition(":")
        assert separator, f"{path}: 无效 frontmatter 行: {line}"
        normalized = value.strip()
        result[key.strip()] = json.loads(normalized) if normalized.startswith("[") else normalized
    return result


def _normalize_alias(value: str) -> str:
    return re.sub(r"[\s_/：:，,；;（）()\-]+", "", value).casefold()


def test_sop_index_has_exactly_one_link_for_every_sop() -> None:
    index = INDEX_PATH.read_text(encoding="utf-8")
    links = re.findall(r"\]\(([^)]+\.md)\)", index)
    expected = {path.name for path in _sop_paths()}

    assert len(links) == len(set(links)), "SOP 索引包含重复链接"
    assert set(links) == expected
    assert len(expected) == 41


def test_every_sop_has_complete_single_task_contract() -> None:
    for path in _sop_paths():
        text = path.read_text(encoding="utf-8")
        metadata = _frontmatter(path)

        assert metadata.get("type") == "process"
        assert metadata.get("id")
        assert metadata.get("owner")
        assert metadata.get("route_key")
        aliases = metadata.get("route_aliases")
        assert isinstance(aliases, list) and aliases
        assert len(re.findall(r"^# ", text, flags=re.MULTILINE)) == 1
        for heading in REQUIRED_HEADINGS:
            assert text.count(heading) == 1, f"{path}: {heading} 数量不为 1"


def test_route_keys_and_natural_language_aliases_are_globally_unique() -> None:
    route_keys: dict[str, Path] = {}
    aliases: dict[str, Path] = {}

    for path in _sop_paths():
        metadata = _frontmatter(path)
        route_key = str(metadata["route_key"])
        assert route_key not in route_keys, f"route_key 重复: {route_key}: {route_keys[route_key]} / {path}"
        route_keys[route_key] = path

        for raw_alias in metadata["route_aliases"]:
            alias = _normalize_alias(str(raw_alias))
            assert alias not in aliases, f"route alias 重复: {raw_alias}: {aliases[alias]} / {path}"
            aliases[alias] = path

    assert len(route_keys) == len(_sop_paths())


def test_capability_sop_status_matches_registry() -> None:
    registry = json.loads(CAPABILITY_REGISTRY_PATH.read_text(encoding="utf-8"))
    capabilities = {item["capabilityId"]: item for item in registry["capabilities"]}
    seen: set[str] = set()

    for path in _sop_paths():
        metadata = _frontmatter(path)
        capability_id = metadata.get("capability_id")
        if not capability_id:
            continue
        capability = capabilities[str(capability_id)]
        seen.add(str(capability_id))
        if capability["availability"] == "planned":
            assert metadata["status"] == "current"
            assert metadata["execution_status"] == "blocked"
            text = path.read_text(encoding="utf-8").casefold()
            assert "blocked" in text
            assert "## 质量验收门禁" in text
            assert "禁止" in text
        else:
            assert metadata["status"] == "current"

    assert seen == set(capabilities)


def test_referenced_repository_scripts_exist() -> None:
    script_pattern = re.compile(r"(?<![\w/])(scripts/[A-Za-z0-9_.*/-]+)")
    for path in _sop_paths():
        text = path.read_text(encoding="utf-8")
        for raw in script_pattern.findall(text):
            if "*" in raw:
                assert list(ROOT.glob(raw)), f"{path}: 通配脚本无匹配: {raw}"
                continue
            candidate = raw.rstrip(".,;:)")
            assert (ROOT / candidate).is_file(), f"{path}: 脚本不存在: {candidate}"


def test_index_aliases_match_sop_frontmatter() -> None:
    index = INDEX_PATH.read_text(encoding="utf-8")
    for path in _sop_paths():
        metadata = _frontmatter(path)
        assert f"`{metadata['route_key']}`" in index
        for alias in metadata["route_aliases"]:
            assert str(alias) in index, f"{path}: 索引缺少别名: {alias}"
