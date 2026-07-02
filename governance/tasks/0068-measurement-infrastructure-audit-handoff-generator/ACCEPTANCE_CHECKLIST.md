# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 audit contracts、generator、local-ci、tests、AGENTS/roadmap 和任务文档。
- [x] 不连接真实生产 API、Bot、OIDC、SIEM、监控平台或外部 developer portal。
- [x] 不保存真实 secret、DSN、私钥、证书、生产日志、用户报告正文或外部账号数据。
- [x] generator、focused tests、ruff、secret scan 和 quick local-ci 已通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 复核现有 closeout、release gate、local-ci、roadmap 和 pending external validation 事实。
Verify: `rg` / `sed` / `git status`。
Gate: 当前差距明确。

## TP-02.01

- [x] 新增 audit handoff contract。
Verify: JSON syntax。
Gate: pending external validation policy 明确。

## TP-02.02

- [x] 新增 audit handoff generator。
Verify: generator CLI。
Gate: Markdown/JSON 写入成功。

## TP-03.01

- [x] 新增 audit handoff 回归测试。
Verify: focused pytest。
Gate: pendingExternalValidationCount 等于 tracked + untracked non-ignored occurrence count。

## TP-03.02

- [x] 接入 local-ci artifact 和目录级 AGENTS。
Verify: local-ci/script docs。
Gate: `auditHandoff` artifact 可发现。

## TP-03.03

- [x] 同步 roadmap 与任务索引。
Verify: diff review。
Gate: 文档不夸大 live evidence。

## TP-04.01

- [x] 运行 focused validation 和 secret scan。
Verify: pytest/ruff/secret scan。
Gate: no sensitive assignment output。

## TP-04.02

- [x] 运行 quick local-ci、任务校验并收口证据。
Verify: quick local-ci + validators。
Gate: 本地 quick CI 通过。

## Evidence Checklist

- [x] `python3 -m json.tool contracts/fate/audit/handoff.json`
- [x] `bash scripts/audit-handoff.sh --output-dir /tmp/fatecat-audit-handoff-0068`
- [x] `.venv/bin/python -m pytest -q tests/regression/test_audit_handoff.py`
- [x] `.venv/bin/python -m ruff check scripts/audit-handoff.py tests/regression/test_audit_handoff.py`
- [x] `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0068.json`
- [x] `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0068`
- [x] task validators
