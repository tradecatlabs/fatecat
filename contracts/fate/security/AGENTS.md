# AGENTS.md - security resources

## 目录用途

`contracts/fate/security/` 是测算基础设施安全、隐私和发布门禁的资源真相源。这里登记 token 权限、scoped RBAC、生产身份/OIDC 准入、CORS、限流、请求体限制、响应安全头、结构化 audit_event、retention policy baseline、SIEM/不可变审计存储准入、OWASP API 回归包、隐私示例扫描、source hygiene、secret scan、public release policy 和 production readiness 等 SecurityControl，只做发现、审计和接入说明，不保存真实 secret 或生产凭证。

## 目录结构

```text
security/
├── AGENTS.md
├── externalization-evidence-contract.json
├── production-security-policy.json
├── secret-scan-allowlist.json
├── registry.json
└── schemas/
    └── security-control.schema.json
```

## 职责边界

- `registry.json`：登记 SecurityControl 资源，记录控制类型、状态、环境变量、实现位置、验证命令、隐私边界和外部连通状态。
- `schemas/security-control.schema.json`：定义安全控制资源字段，覆盖 audit_log、auth、cors、rate_limit、request_limit、headers、identity、siem、owasp_api_regression、privacy、rbac、retention、source_hygiene、secret_scan、release_gate 和 production_readiness。
- `production-security-policy.json`：定义生产身份外部化、OIDC/IdP 准入、SIEM/不可变审计存储、retention 自动清理计划和 OWASP API Security Top 10 回归包策略；它是 contract，不保存真实外部配置。
- `externalization-evidence-contract.json`：定义 OIDC/SIEM/retention cleaner live evidence 的机器契约和反伪造负例；通过只表示证据结构可验证，不表示真实外部平台已接入。
- `scripts/security-smoke.sh`：本地安全 smoke 入口；验证 token/owner 边界、响应安全头、请求体限制、限流、registry metadata，并可串联 privacy/source/public-release 文件门禁。
- `scripts/production-security-gate.sh`：本地生产安全 contract gate；验证 OIDC/SIEM/retention/OWASP 策略完整性，不连接真实 OIDC、SIEM 或外部账号。
- `scripts/security-externalization-gate.sh`：本地安全外部化 evidence gate；验证 OIDC/SIEM/retention cleaner 证据契约和伪造证据拒绝，不连接真实 IdP、SIEM 或生产数据库。
- `scripts/secret-scan.sh`：本地 secret scanner 入口；扫描一线文本文件中的疑似真实 token、API key、私钥、DSN 和 webhook，只输出脱敏 finding summary。
- `secret-scan-allowlist.json`：记录已知占位符、reference repo/archive 排除边界和允许的示例片段；不得写入真实 secret。
- 这里不得保存真实 token、secret、DSN、私钥、证书、生产账号或 webhook 地址。
- scoped RBAC 仅覆盖本地记录接口的 admin/user/owner/scope 边界，不得写成 OAuth/OIDC、外部 IdP 或生产 IAM 已完成。
- 生产身份、SIEM 和 retention cleanup 控制在当前仓库内只能登记准入 contract；真实 OIDC/IdP、SIEM、不可变审计存储和按年龄自动清理必须保留为外部或后续实现验证。
- `external_connectivity_pending` 只表示需要真实域名、真实 token、Bot 或生产权限验证，不得写成已生产通过。
