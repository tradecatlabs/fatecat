# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 audit contracts、verifier、local-ci、tests、AGENTS/roadmap 和任务文档。
- [x] 不连接真实生产 API、Bot、OIDC、SIEM、监控平台、developer portal 或外部审计 SaaS。
- [x] 不保存真实 secret、DSN、私钥、证书、生产日志、用户报告正文或外部账号数据。
- [x] generator、verifier、focused tests、ruff、secret scan 和 quick local-ci 已通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 复核 0068 handoff contract、generator、local-ci artifact 和 MI-100.10.04 缺口。
Verify: `sed` / `rg` / roadmap。
Gate: 当前 dry-run 缺口明确。

## TP-02.01

- [x] 新增 audit dry-run contract。
Verify: JSON syntax。
Gate: non-claim 与 ship gate policy 明确。

## TP-02.02

- [x] 新增 audit handoff dry-run verifier。
Verify: verifier CLI。
Gate: Markdown/JSON 写入成功。

## TP-03.01

- [x] 新增 audit dry-run 回归测试。
Verify: focused pytest。
Gate: dry-run passed 与 shipGate blocked 语义同时被锁定。

## TP-03.02

- [x] 接入 local-ci artifact 和目录级 AGENTS。
Verify: local-ci/script docs。
Gate: `auditDryRun` artifact 可发现。

## TP-03.03

- [x] 同步 roadmap 与任务索引。
Verify: diff review。
Gate: 文档不夸大第三方审计或 live evidence。

## TP-04.01

- [x] 运行 focused validation 和 secret scan。
Verify: pytest/ruff/secret scan。
Gate: no sensitive assignment output。

## TP-04.02

- [x] 运行 quick local-ci、任务校验并收口证据。
Verify: quick local-ci + validators。
Gate: 本地 quick CI 通过。

## Evidence Checklist

- [x] `python3 -m json.tool contracts/fate/audit/dry-run.json`
- [x] `bash scripts/audit-handoff.sh --output-dir /tmp/fatecat-audit-dry-run-0069/handoff`
- [x] `bash scripts/audit-handoff-dry-run.sh --bundle-json /tmp/fatecat-audit-dry-run-0069/handoff/audit-handoff.json --bundle-markdown /tmp/fatecat-audit-dry-run-0069/handoff/AUDIT_HANDOFF.md --output-dir /tmp/fatecat-audit-dry-run-0069/dry-run`
- [x] `.venv/bin/python -m pytest -q tests/regression/test_audit_handoff.py tests/regression/test_audit_handoff_dry_run.py`
- [x] `.venv/bin/python -m ruff check scripts/audit-handoff-dry-run.py tests/regression/test_audit_handoff_dry_run.py`
- [x] `bash scripts/secret-scan.sh --output-json /tmp/fatecat-secret-scan-0069.json`
- [x] `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0069`
- [x] task validators
