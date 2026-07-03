# Acceptance Checklist

## Global Standards

- [x] 不新增 production capability。
- [x] 不把 MingLi-Bench 标准答案注入 production provider。
- [x] 不调用外部模型 API。
- [x] 不保存真实 token、secret、DSN 或生产账号。
- [x] 外部模型评测与专家人工复核仍标记为未完成。

# Task Package Checklists

## TP-01 SPEC: 复核 core corpus、MingLi-Bench 和供应链现状

Verify: core corpus、MingLi runner、vendor manifest、registry and upstream ls-remote inspected.

Gate: 不能把已有 stats 脚本误认为脱敏交付 gate。

- [x] core-quality-corpus gate 已检查。
- [x] MingLi-Bench runner 和 prediction generator 已检查。
- [x] vendor manifest 和 data supply chain registry 已检查。
- [x] 上游 HEAD 漂移事实已记录，不自动更新 vendor。

## TP-01.01 复核 core corpus、MingLi-Bench、vendor 和 evaluation registry

Verify: command evidence exists in task context.

Gate: upstream drift only recorded, not auto-updated.

- [x] `rg/sed` evidence collected.
- [x] local MingLi stats/prediction smoke executed.
- [x] upstream HEAD observed.

## TP-02 PLAN: 设计脱敏 aggregate gate

Verify: contract exists.

Gate: no per-question detail in report schema.

- [x] 新增 gate contract。
- [x] forbidden fragments 覆盖题干、出生信息、标准答案、逐题结果和 secret。
- [x] 只输出聚合字段。

## TP-02.01 新增 MingLi-Bench aggregate gate contract

Verify: `contracts/fate/evaluations/mingli-bench-gate.json`.

Gate: required local sources and forbidden fragments declared.

- [x] Required report fields declared.
- [x] Required benchmark fields declared.
- [x] Forbidden fragments declared.

## TP-03 BUILD: 实现 gate

Verify: CLI smoke.

Gate: no external model/API call.

- [x] Python gate 实现。
- [x] Shell wrapper 实现并可执行。
- [x] CLI summary 可写入 JSON。
- [x] no-leak 检查在 gate 内执行。

## TP-03.01 实现 `mingli-bench-gate.py/.sh`

Verify: syntax and smoke pass.

Gate: summary only aggregate.

- [x] Python script added.
- [x] Shell wrapper added.
- [x] Summary writes JSON.

## TP-04 BUILD: 仓库接线

Verify: registry/docs/local-ci updated.

Gate: MingLi remains optional/evaluation_only.

- [x] Evaluation registry 已更新。
- [x] data supply chain registry hash 已刷新。
- [x] local-ci quick 已接入 gate。
- [x] AGENTS 和运维文档已同步。

## TP-04.01 接入 registry、docs、AGENTS 和 quick CI

Verify: file diff and focused tests.

Gate: no production report or provider change.

- [x] Evaluation registry updated.
- [x] local-ci quick path updated.
- [x] docs and AGENTS synced.

## TP-04.02 刷新 data supply chain registry hash

Verify: data-supply-chain gate.

Gate: registry hash matches actual evaluation registry.

- [x] sha256 refreshed.
- [x] data supply chain gate passed.

## TP-05 TEST/SHIP: 回归和门禁

Verify: focused tests, quick CI and remote CI.

Gate: no local or remote failure.

- [x] 语法检查已通过。
- [x] gate smoke 已通过。
- [x] focused pytest 已通过。
- [x] data supply chain gate 已通过。
- [x] quick CI 已通过。
- [ ] 任务文档校验待执行。
- [x] commit/push/remote CI 证据由外层交付流处理，任务快照不预声明。

## TP-05.01 增加 focused regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_mingli_bench_aggregate_gate.py tests/regression/test_mingli_bench_gate.py`.

Gate: no regression failure.

- [x] Aggregate gate tests added.
- [x] Existing MingLi runner tests still pass.

## TP-05.02 运行完整验证、提交、推送和远端 CI

Verify: quick CI, task validators, git delivery, GitHub Acceptance.

Gate: all must pass before Done.

- [x] Quick CI.
- [ ] Task validators.
- [x] Commit and push handled outside committed task snapshot.
- [x] Remote GitHub Acceptance evidence handled outside committed task snapshot.
