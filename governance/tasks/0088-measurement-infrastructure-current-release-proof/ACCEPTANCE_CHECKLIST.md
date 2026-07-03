# Acceptance Checklist

## Global Standards

- [x] 不把本地 imageId 当 GHCR registry digest。
- [x] 不把历史 commit 的 workflow run 当当前 commit 证据。
- [x] 不输出 token、secret、DSN、报告正文或生产日志。
- [x] 不声明生产 API/HF/Bot live 已完成。

# Task Package Checklists

## TP-01 SPEC

Verify: roadmap and current remote state inspected.

Gate: no implementation before current proof gap was confirmed.

- [x] 0088 roadmap node inspected.
- [x] Current HEAD missing container workflow proof before this task.

## TP-02 PLAN

Verify: local-contract and required-current-release modes defined.

Gate: production live checks remain out of scope.

- [x] Evidence IDs and boundaries documented.
- [x] Anti-overclaim rules documented.

## TP-03 BUILD

Verify: script, contract entries, AGENTS and regression exist.

Gate: script does not print credentials and does not accept invalid digest.

- [x] `current-release-proof.py/.sh` added.
- [x] ReleaseGate and registry entries added.
- [x] Regression added.

## TP-04 TEST

Verify: focused tests, proof local mode and quick CI pass.

Gate: secret scan findingCount=0.

- [x] focused pytest passed.
- [x] ruff passed.
- [x] secret scan passed.
- [x] quick CI passed.

## TP-05 SHIP

Verify: repository contains the gate needed for final commit remote acceptance/container/current proof.

Gate: current release proof uses final HEAD after commit, not pre-commit evidence; final evidence is captured outside the same source commit.

- [x] commit and push handled by delivery flow after local closeout.
- [x] remote acceptance handled by delivery flow after local closeout.
- [x] remote container workflow handled by delivery flow after local closeout.
- [x] required current-release-proof handled by delivery flow after local closeout.
