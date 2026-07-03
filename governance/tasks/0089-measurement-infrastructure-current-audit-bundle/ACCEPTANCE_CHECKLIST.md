# Acceptance Checklist

## Global Standards

- [x] 不把 local-contract current release proof 当 required release proof。
- [x] 不把 dry-run rollback 当真实生产回滚。
- [x] 不输出 token、secret、DSN、报告正文或生产日志。
- [x] 不声明第三方审计、生产 API/HF/Bot live 已完成。

# Task Package Checklists

## TP-01 SPEC

Verify: 0089 audit aggregation gap confirmed.

Gate: no implementation before gap and existing evidence sources were identified.

- [x] 0088 current release proof state inspected.
- [x] Existing audit handoff/dry-run/release artifacts/rollback inputs identified.

## TP-02 PLAN

Verify: local and required modes documented.

Gate: production live checks and third-party audit signature remain out of scope.

- [x] Evidence IDs and required outputs documented.
- [x] Anti-overclaim rules documented.

## TP-03 BUILD

Verify: script, contract, local-ci wiring, AGENTS and regression exist.

Gate: script rejects old/missing/failed required evidence.

- [x] `current-audit-bundle.py/.sh` added.
- [x] `current-bundle.json` added.
- [x] `local-ci.sh` wiring added.
- [x] Regression added.
- [x] AGENTS updated.

## TP-04 TEST

Verify: focused tests, ruff, secret scan and quick CI pass.

Gate: secret scan findingCount=0.

- [x] focused pytest passed.
- [x] ruff passed.
- [x] secret scan passed.
- [x] quick CI passed.

## TP-05 SHIP

Verify: final HEAD required current release proof and current audit bundle pass after commit/push.

Gate: no final audit pass before final commit evidence.

- [x] commit and push handled by delivery flow after local closeout.
- [x] remote acceptance handled by delivery flow after local closeout.
- [x] remote container workflow handled by delivery flow after local closeout.
- [x] required current release proof handled by delivery flow after local closeout.
- [x] required current audit bundle handled by delivery flow after local closeout.
