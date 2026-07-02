# Acceptance Checklist

# Global Standards
- [x] 默认不开启 webhook callback。
- [x] URL 校验拒绝本机、内网、保留地址和带用户名密码的 URL。
- [x] 提供 secret 时使用 HMAC-SHA256 签名。
- [x] callback payload 不包含 Markdown 正文、姓名、出生地区、请求体或 secret。
- [x] callback 失败不影响 report job 终态。
- [x] contract/docs/env/AGENTS/roadmap 已同步。
- [x] quick local-ci 通过。
- [x] closeout packet 已生成。

# Task Package Checklists
## TP-01.01 context audit
- [x] Verify: `rg -n "report/jobs|CalculationJob|webhook" docs contracts governance scripts tests domains/experience-delivery/services/fatecat-delivery/src`
- [x] Gate: MI-03.03 缺口明确。

## TP-02.01 webhook runtime primitives
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k webhook`
- [x] Gate: payload/signature/URL validation 可本地验证。

## TP-02.02 terminal transitions
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k webhook`
- [x] Gate: succeeded/failed/cancelled 终态触发。

## TP-02.03 API headers
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k webhook`
- [x] Gate: 默认禁用、启用后不回显 secret。

## TP-03.01 webhook smoke
- [x] Verify: `bash scripts/webhook-smoke.sh --output-json /tmp/fatecat-webhook-smoke.json`
- [x] Gate: no external network, JSON status passed。

## TP-03.02 regression tests
- [x] Verify: `.venv/bin/python -m pytest -q tests/regression/test_webhook_smoke.py`
- [x] Gate: smoke run and CLI both pass。

## TP-03.03 quick local-ci
- [x] Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-webhook`
- [x] Gate: quick CI passes。

## TP-04.01 docs/contracts
- [x] Verify: `python3 -m json.tool contracts/fate/security/registry.json`
- [x] Gate: no live webhook/retry overclaim。

## TP-04.02 closeout
- [x] Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0031-measurement-infrastructure-webhook-callbacks --phase closeout`
- [x] Gate: closeout packet exists。
