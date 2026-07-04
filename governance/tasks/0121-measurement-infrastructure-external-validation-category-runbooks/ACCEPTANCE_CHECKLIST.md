# Acceptance Checklist

# Global Standards

- [x] 不保存真实 token、secret、DSN、raw URL、private key 或生产日志 payload。
- [x] 不把本地 runbook ready 写成 production live passed。
- [x] 所有新增入口必须有 contract、test、AGENTS 或 roadmap 接线。
- [x] 本地 quick CI 必须通过后才能提交推送。

# Task Package Checklists

## TP-01 Scope Confirmation

Verify: `rg -n "MI-100.A.03 external validation runbook per category" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Gate: 不扩大到 stale alert 或 live validation。

- [x] 确认 0121 只覆盖 category runbooks。
- [x] 确认 22 个当前 category 均要 profile。

## TP-02 Contract And Gate

Verify: `rg -n "external-validation-category-runbooks" contracts scripts`

Gate: runbook ready 仍保持 `shipGate.status=blocked`。

- [x] Contract 定义 required runbook fields。
- [x] Script 覆盖当前 22 个 category。
- [x] Script 拒绝 unknown category。
- [x] Script 拒绝 raw URL、token/secret/DSN/private-key marker。
- [x] Certification audit domain 消费 category runbooks。

## TP-03 Regression And Local-CI

Verify: `.venv/bin/python -m pytest -q tests/regression/test_external_validation_category_runbooks.py tests/regression/test_measurement_infrastructure_certification.py`

Gate: 22 category、unknown category、privacy、wiring 覆盖。

- [x] 新增 category runbooks regression。
- [x] local-ci 跑 category runbooks gate。
- [x] local-ci summary 记录 `externalValidationCategoryRunbooks`。

## TP-04 Validation

Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-category-runbooks-0121`

Gate: quick CI passed 且无 live evidence 时 certification 仍 blocked。

- [x] Targeted pytest passed.
- [x] Ruff check passed.
- [x] Ruff format check passed.
- [x] Secret scan passed.
- [x] Real category runbooks gate chain passed.
- [x] local quick CI passed.
- [x] Task docs closeout validation passed after final doc sync.

## TP-05 Delivery

Verify: `git status --short --branch`

Gate: 远端 CI 结果不预写入仓库，推送后单独观察。

- [x] Local delivery package prepared.
- [x] Remote CI observation kept out of repository evidence before push.
