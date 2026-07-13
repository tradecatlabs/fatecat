#!/usr/bin/env python3
"""校验 GEO 采样题集的稳定性、来源完整性和非结果边界。"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
QUERY_SET = ROOT / "contracts" / "fate" / "discovery" / "query-set.json"
REQUIRED_GROUPS = {"brand_verification", "capability", "integration", "evidence", "privacy", "risk"}
ALLOWED_SOURCE_HOSTS = {"tradecatlabs-fatecat.hf.space", "github.com"}
FORBIDDEN_RESULT_KEYS = {
    "answer",
    "answerText",
    "brandMentioned",
    "brandRecommended",
    "citationRate",
    "platformResult",
    "rank",
}


def fail(message: str) -> None:
    raise ValueError(message)


def nonempty_strings(value: object, field: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        fail(f"{field} 必须是非空字符串数组")
    return value


def validate() -> dict[str, object]:
    payload = json.loads(QUERY_SET.read_text(encoding="utf-8"))
    if payload.get("schemaVersion") != 1 or payload.get("kind") != "fatecat.geo_query_set":
        fail("schemaVersion 或 kind 无效")
    groups = set(nonempty_strings(payload.get("queryGroups"), "queryGroups"))
    if groups != REQUIRED_GROUPS:
        fail(f"queryGroups 必须精确为 {sorted(REQUIRED_GROUPS)}")

    policy = payload.get("samplingPolicy")
    if not isinstance(policy, dict) or policy.get("resultState") != "external_validation_pending":
        fail("samplingPolicy.resultState 必须保持 external_validation_pending")
    nonempty_strings(policy.get("minimumEvidence"), "samplingPolicy.minimumEvidence")
    nonempty_strings(policy.get("nonClaims"), "samplingPolicy.nonClaims")

    prompts = payload.get("prompts")
    if not isinstance(prompts, list) or len(prompts) < 12:
        fail("prompts 至少需要 12 个稳定问题")
    ids: set[str] = set()
    observed_groups: set[str] = set()
    for index, prompt in enumerate(prompts):
        if not isinstance(prompt, dict):
            fail(f"prompts[{index}] 必须是对象")
        leaked_keys = FORBIDDEN_RESULT_KEYS & set(prompt)
        if leaked_keys:
            fail(f"prompts[{index}] 不得保存平台结果字段: {sorted(leaked_keys)}")
        prompt_id = prompt.get("id")
        if not isinstance(prompt_id, str) or not prompt_id.strip() or prompt_id in ids:
            fail(f"prompts[{index}].id 缺失或重复")
        ids.add(prompt_id)
        group = prompt.get("group")
        if group not in groups:
            fail(f"{prompt_id}.group 无效")
        observed_groups.add(group)
        if prompt.get("locale") != "zh-CN":
            fail(f"{prompt_id}.locale 必须是 zh-CN")
        if not isinstance(prompt.get("question"), str) or not prompt["question"].strip():
            fail(f"{prompt_id}.question 不能为空")
        nonempty_strings(prompt.get("targetEntities"), f"{prompt_id}.targetEntities")
        nonempty_strings(prompt.get("expectedFacts"), f"{prompt_id}.expectedFacts")
        nonempty_strings(prompt.get("forbiddenClaims"), f"{prompt_id}.forbiddenClaims")
        source_urls = nonempty_strings(prompt.get("expectedSourceUrls"), f"{prompt_id}.expectedSourceUrls")
        for url in source_urls:
            parsed = urlsplit(url)
            if parsed.scheme != "https" or parsed.hostname not in ALLOWED_SOURCE_HOSTS:
                fail(f"{prompt_id} 含非官方或非 HTTPS 来源: {url}")
    if observed_groups != REQUIRED_GROUPS:
        fail(f"prompts 未覆盖全部 query group: {sorted(REQUIRED_GROUPS - observed_groups)}")
    return {
        "status": "passed",
        "kind": payload["kind"],
        "promptCount": len(prompts),
        "groupCount": len(groups),
        "resultState": policy["resultState"],
    }


def main() -> int:
    try:
        result = validate()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
