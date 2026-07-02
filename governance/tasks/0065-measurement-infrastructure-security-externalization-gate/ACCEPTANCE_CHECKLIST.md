# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 security externalization contract baseline、gate、tests、docs 和任务文档。
- [x] 不连接真实 OIDC/IdP、SIEM、不可变审计平台或生产数据库。
- [x] 不保存真实 token、secret、DSN、用户输入、出生地区、报告正文、生产日志或 audit payload。
- [x] focused tests、validators、ruff、secret scan 和 quick local CI 通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 读取 0061/0064、security registry、production-security-gate、local-ci 和 API 文档。
Verify: `git status` / `rg` / `sed`。
Gate: 当前事实和 0065 边界明确。

## TP-02.01

- [x] 新增 security externalization evidence contract。
- [x] contract 不包含真实 endpoint、token、secret、DSN、payload 或用户数据。
Verify: JSON syntax + gate。
Gate: evidence contract 可机器读取。

## TP-02.02

- [x] security schema 链接 externalization evidence。
- [x] security registry 链接 evidence contract 和 gate。
- [x] security AGENTS 说明职责边界。
Verify: focused tests / docs diff。
Gate: registry/schema/AGENTS 链接一致。

## TP-03.01

- [x] 新增 security-externalization-gate Python 脚本。
- [x] 新增 shell wrapper。
Verify: gate CLI。
Gate: 无外部账号依赖。

## TP-03.02

- [x] regression tests 覆盖 gate summary。
- [x] regression tests 覆盖 CLI 输出。
- [x] regression tests 覆盖 fake identity/SIEM/retention evidence negative cases。
Verify: focused pytest。
Gate: 边界断言通过。

## TP-03.03

- [x] quick local CI 运行 security externalization gate。
- [x] quick local CI summary 包含 `securityExternalizationGate` artifact。
Verify: local-ci summary artifact。
Gate: quick CI 运行新 gate。

## TP-04.01

- [x] API 文档写入 security externalization evidence contract。
- [x] roadmap 标记 0065 contract/gate baseline。
- [x] scripts AGENTS 和 INDEX 同步。
Verify: docs diff + rg。
Gate: 文档不夸大。

## TP-04.02

- [x] validators 通过。
- [x] focused tests 通过。
- [x] ruff/format/secret scan 通过。
- [x] quick local CI 通过。
Verify: validation evidence。
Gate: 全部通过。
