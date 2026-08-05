---
id: SOP-DEV-SECURITY-CONTROLS
type: process
status: current
owner: security
route_key: verify_security_controls
route_aliases: ["扫描密钥", "执行生产安全门禁", "检查隐私控制"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P30D
---

# 验证安全与隐私控制

## 任务定义
验证 tracked source 中的 secret、鉴权、RBAC、CORS、限流、请求体、安全头、隐私、retention 和外部化证据边界。

## 当前状态
本地 security smoke/secret scan/production gate 可用；OIDC、SIEM、Vault/KMS 和生产清理器为 staged external evidence。

## 适用场景
安全相关代码、配置、公开服务、发布或定期审计。

## 输入要求
当前 worktree、生产环境变量名称、可选脱敏 external evidence；不得提供 secret 值。

## 前置条件
确认 `.env` ignored；生产策略 contract 可读；授权范围明确。

## 默认工具链
`bash scripts/secret-scan.sh`、`security-smoke.sh`、`production-security-gate.sh`、`check-source-hygiene.sh`。

## 固定路径
`contracts/fate/security/`、`infra/environments/*/.env.example`、delivery security middleware、`.gitignore`。

## 成熟参数
请求体默认 1 MiB、超时 30 秒、每分钟 120、并发计算 2；token 只通过环境变量；external evidence 只接受 proof ref/hash。

## 分步执行流程
1. 扫描 tracked source 和 Git 状态。
2. 运行 security smoke。
3. 运行 production security和externalization gates。
4. 检查配置示例、ignore、日志脱敏和负例。
5. 对真实外部系统明确标记待执行。

## 幂等与增量策略
相同 commit/contract 结果稳定；allowlist 变更必须最小且带具体误报证据。

## 限速与并发规则
安全 smoke 串行修改测试环境；外部 IdP/SIEM/Vault 调用按各服务限速，不自动并行。

## 输出目录
`infra/runtime/local-state/exports/security/` 或 `/tmp/fatecat-security-*`。

## 命名规范
`security-gate-<short-sha>-<UTC>.json`；证据引用不得包含 URL query/token。

## 质量验收门禁
secret/source/security/production gates PASS；无高熵泄露、私钥、真实 DSN、明文密码或伪 external claim。

## 失败处理
疑似真实 secret 立即停止传播、撤销/轮换并清理历史；其他控制失败按根因阻断发布。

## 恢复与重试策略
修复后从 secret scan 开始全链重跑；外部暂缺不得用本地 token 伪造通过。

## 安全边界
扫描输出只含路径/行号/变量名/风险，不输出值；不可逆密钥轮换需授权。

## 临时文件清理
删除扫描副本、临时 env 和失败证据；保留脱敏 summary。

## 运行记录登记
登记 commit、扫描范围、control IDs、通过/失败、external pending 和修复证据。

## 明确禁止事项
- 禁止输出或提交真实 secret。
- 禁止宽泛 allowlist。
- 禁止把本地 scoped token 写成生产 OIDC。
