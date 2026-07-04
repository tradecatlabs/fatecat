# Acceptance Checklist

# Global Standards

- [x] 不保存真实 token、secret、DSN、raw URL、private key 或生产日志 payload。
- [x] 不把本地 dry-run 或 schema accepted 写成 production live passed。
- [x] 所有新增入口必须有 contract、test、AGENTS 或 roadmap 接线。
- [x] 本地 quick CI 必须通过后才能提交推送。

# Task Package Checklists

## TP-01 Scope Confirmation

Verify: `rg -n "MI-100.A.02 proof-ref" docs/reference-materials/roadmap/测算基础设施100%实现计划.md`

Gate: 不扩大到 category runbook 或 live validation。

- [x] 确认 0119 work queue 是输入。
- [x] 确认 0120 只输出 proof-ref contract/verifier。

## TP-02 Contract And Gate

Verify: `rg -n "external-validation-proof-ref" contracts scripts`

Gate: schema accepted 仍保持 `shipGate.status=blocked`。

- [x] Contract 定义 allowed prefixes 和 required fields。
- [x] Schema 定义 proof-ref bundle。
- [x] Script 校验 work queue、evidence bundle、source binding、hash 和时间窗。
- [x] Script 拒绝 raw URL、placeholder、fake、token/secret/DSN/private-key marker。
- [x] Certification audit domain 消费 proof-ref gate。

## TP-03 Regression And Local-CI

Verify: `.venv/bin/python -m pytest -q tests/regression/test_external_validation_proof_ref_gate.py tests/regression/test_measurement_infrastructure_certification.py`

Gate: pending、accepted bundle、raw URL rejection 和 wiring 覆盖。

- [x] 新增 proof-ref regression。
- [x] local-ci 跑 proof-ref gate。
- [x] local-ci summary 记录 `externalValidationProofRefGate`。

## TP-04 Validation

Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-proof-ref-0120`

Gate: quick CI passed 且无 live evidence 时 certification 仍 blocked。

- [x] Targeted pytest passed.
- [x] Ruff check passed.
- [x] Ruff format check passed.
- [x] Secret scan passed.
- [x] Real proof-ref gate chain passed.
- [x] local quick CI passed.
- [x] Task docs closeout validation passed after final doc sync.

## TP-05 Delivery

Verify: `git status --short --branch`

Gate: 远端 CI 结果不预写入仓库，推送后单独观察。

- [x] Local delivery package prepared.
- [x] Remote CI observation kept out of repository evidence before push.
