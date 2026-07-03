# Acceptance Checklist

## Global Standards

- [x] 不新增 production capability。
- [x] 不改动报告生成业务语义。
- [x] 不保存真实 token、secret、DSN、生产 URL、真实用户数据或报告正文。
- [x] 不声明 PyPI/npm SDK 已发布。
- [x] 不声明公网 developer portal 已上线。
- [x] 不声明公网 sandbox token 服务已上线。

# Task Package Checklists

## TP-01 SPEC

Verify: existing developer platform baseline、sandbox、examples、docs smoke and roadmap inspected.

Gate: target remains local release baseline, not public release.

- [x] Existing developer-platform contract inspected.
- [x] Existing developer docs smoke inspected.
- [x] Existing sandbox fixtures inspected.
- [x] 0086 roadmap row confirmed.

## TP-01.01 复核 0067 baseline、sandbox、examples、docs smoke 和 roadmap

Verify: repo evidence collected.

Gate: no production API behavior changed.

- [x] Files inspected.

## TP-02 PLAN

Verify: portal/sdk/snapshot/no-overclaim contract boundaries recorded.

Gate: snapshot stores digest/shape only.

- [x] Portal contract boundary defined.
- [x] SDK release baseline boundary defined.
- [x] Fixed snapshot digest boundary defined.
- [x] No-overclaim summary booleans defined.

## TP-02.01 设计 portal / SDK release / snapshot / no-overclaim contract

Verify: task plan contains Future-Optimal and Ponytail boundaries.

Gate: external live items stay out of scope.

- [x] Boundary designed.

## TP-03 BUILD

Verify: contract and docs files exist.

Gate: no real token, non-Beijing real place or response body stored.

- [x] `developer-portal.json` added.
- [x] `sdk-release-baseline.json` added.
- [x] `sandbox-output-snapshot.json` added.
- [x] `PORTAL.md` added.
- [x] `SDK_RELEASE_BASELINE.md` added.

## TP-03.01 新增 developer portal、SDK release baseline、sandbox snapshot 和文档

Verify: new files exist and JSON validates.

Gate: not_published and not_implemented boundaries remain explicit.

- [x] Files added.

## TP-04 BUILD

Verify: gate script, local-ci and tests exist.

Gate: gate summary must keep external live booleans false.

- [x] `developer-portal-gate.py/.sh` added.
- [x] local-ci step added.
- [x] regression test added.
- [x] AGENTS and docs updated.
- [x] API changelog updated.

## TP-04.01 新增 `developer-portal-gate.py/.sh`

Verify: gate smoke passes.

Gate: no external calls.

- [x] Gate added.

## TP-04.02 接入 local-ci、tests、AGENTS、docs 和 changelog

Verify: quick CI includes developer portal gate and focused test.

Gate: document-drift closed.

- [x] Wiring added.

## TP-05 TEST/SHIP

Verify: syntax, gate, focused pytest, quick CI and task validators pass.

Gate: remote CI is not pre-claimed before commit exists.

- [x] Syntax validation passed.
- [x] Gate smoke passed.
- [x] Focused pytest passed.
- [x] Quick CI passed.
- [x] Task validators passed.
- [x] Commit/push/remote CI evidence recorded by outer delivery flow, not pre-claimed inside this committed task snapshot.

## TP-05.01 运行 syntax、gate、focused pytest 和 quick CI

Verify: command evidence exists in ACCEPTANCE.md.

Gate: all local checks pass.

- [x] Local validation passed.

## TP-05.02 明确提交、推送和远端 CI 由外层交付流汇报

Verify: task snapshot does not pre-claim remote CI.

Gate: remote CI conclusion will be reported after commit/push.

- [x] Remote CI boundary recorded.
