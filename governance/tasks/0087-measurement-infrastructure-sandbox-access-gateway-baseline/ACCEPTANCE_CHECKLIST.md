# Acceptance Checklist

## Global Standards

- [x] 不新增 production capability。
- [x] 不改变默认综合八字报告。
- [x] 不把本地 smoke token 写成公网 token issuer。
- [x] 不保存真实 token、secret、DSN、生产 URL、用户输入或报告正文。
- [x] 不声明 revocation service、production gateway 或外部 sandbox live 已完成。

# Task Package Checklists

## TP-01 SPEC

Verify: developer runtime access gap inspected.

Gate: no implementation before scope boundary was defined.

- [x] 0086 developer platform / portal baseline 已复核。
- [x] delivery API、rate limit、audit、metadata 已复核。

## TP-02 PLAN

Verify: gateway contract, endpoint and no-live-overclaim plan recorded.

Gate: external issuer/revocation remains out of scope.

- [x] gateway contract 边界已定义。
- [x] endpoint 兼容策略已定义。
- [x] 外部未完成项已保留为 pending。

## TP-03 BUILD

Verify: code, contracts, gate, tests and docs exist.

Gate: endpoint reuses existing executor/rate-limit/audit primitives.

- [x] sandbox gateway endpoint 已实现。
- [x] sandbox gateway contract 已新增。
- [x] developer platform / portal contracts 已更新。
- [x] gate 脚本已新增。
- [x] regression 已新增。
- [x] docs / AGENTS / roadmap / local-ci 已更新。

## TP-04 TEST

Verify: local gates and quick CI pass.

Gate: secret scan has zero findings.

- [x] sandbox gateway gate 通过。
- [x] developer platform gate 通过。
- [x] developer portal gate 通过。
- [x] focused pytest 通过。
- [x] ruff check / format check 通过。
- [x] quick CI 通过。

## TP-05 SHIP

Verify: task docs close out and delivery flow handles commit/push/remote CI.

Gate: remote CI is not pre-claimed before run exists.

- [x] 任务状态收口。
- [ ] 提交并推送。
- [ ] 远端 acceptance 对当前 commit 通过或失败日志已记录。
