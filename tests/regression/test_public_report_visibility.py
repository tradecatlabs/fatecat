from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CORE_SRC = ROOT / "domains" / "fate-analysis" / "services" / "fate-core" / "src"
DELIVERY_SRC = ROOT / "domains" / "experience-delivery" / "services" / "fatecat-delivery" / "src"
for source_root in (CORE_SRC, DELIVERY_SRC):
    if str(source_root) not in sys.path:
        sys.path.insert(0, str(source_root))

from bazi_calculator import BaziCalculator  # noqa: E402
from report_generator import build_report_hide, generate_full_report  # noqa: E402
from report_visibility import (  # noqa: E402
    PublicReportContractError,
    load_public_markdown_contract,
    validate_public_markdown,
)


def _result() -> dict:
    return BaziCalculator(
        datetime(1990, 1, 1, 8),
        "male",
        116.4074,
        latitude=39.9042,
        name="测试用户",
        birth_place="北京",
        use_true_solar_time=True,
    ).calculate(hide=build_report_hide("ziwei"))


def test_public_profiles_declare_complete_visibility_contract() -> None:
    schema = json.loads((ROOT / "contracts/fate/capabilities/schemas/report.schema.json").read_text(encoding="utf-8"))
    required = set(schema["requiredPublicMarkdownProfileFields"])
    for report_system in ("bazi", "ziwei"):
        profile = json.loads(
            (ROOT / f"contracts/fate/capabilities/profiles/{report_system}.json").read_text(encoding="utf-8")
        )
        assert set(profile["publicMarkdown"]) == required
        contract = load_public_markdown_contract(report_system)
        assert contract["allowedHeadings"]
        assert contract["allowedTableHeaders"]
        assert contract["machineOnlyResultPaths"]


def test_public_reports_match_allowlist_and_keep_machine_evidence_structured() -> None:
    result = _result()
    reports = {
        report_system: generate_full_report(
            result,
            hide=build_report_hide(report_system),
            report_system=report_system,
        )
        for report_system in ("bazi", "ziwei")
    }
    for report_system, markdown in reports.items():
        assert validate_public_markdown(markdown, report_system) == markdown

    assert result["analysisEvidence"]["visibilityDefault"] == "hidden"
    assert result["ziTimeAnalysis"]["dayPillarNormal"]
    assert result["yongShen"]["basisSource"]
    assert any(item.get("source") for item in result["branchRelations"]["canonical"])
    assert "analysisEvidence" not in reports["bazi"]


@pytest.mark.parametrize(
    ("markdown", "message"),
    [
        ("# 命理排盘报告：测试\n\n### 内部调试\n", "未允许标题"),
        ("# 命理排盘报告：测试\n\n| 内部字段 | 内容 |\n| :-- | :-- |\n", "未允许表头"),
        ("# 命理排盘报告：测试\n\n|内部字段|内容|\n|---|:---:|\n", "未允许表头"),
        ("# 命理排盘报告：测试\n\n| 项目 | 内容 |\n| :-- | :-- |\n| 内部编码 | x |\n", "未允许元数据标签"),
        ("# 命理排盘报告：测试\n\nanalysisEvidence\n", "机器字段进入公开报告"),
    ],
)
def test_public_report_contract_rejects_unregistered_content(markdown: str, message: str) -> None:
    with pytest.raises(PublicReportContractError, match=message):
        validate_public_markdown(markdown, "bazi")
