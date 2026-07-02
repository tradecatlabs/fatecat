# Repo Evidence
- `contracts/fate/security/registry.json` 已有 record token、scoped RBAC、CORS、rate limit、headers、audit_event、retention policy、secret scan、public release 和 production readiness controls。
- `scripts/security-smoke.py` 已验证 token/owner、headers、request body limit、rate limit 和 registry metadata。
- `scripts/production-readiness.sh` 已验证 CORS、真实 token 口径、限流、job store、webhook、HSTS、live API/Bot skip/required 逻辑。
- Roadmap D8 明确缺 OAuth/OIDC、外部 SIEM、不可变审计存储、retention 自动清理和 OWASP API regression pack。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 外部系统 | 不连接真实 OIDC、SIEM、云日志、WORM 或生产账号；只登记 contract 和本地 gate。 |
| 隐私 | 只输出变量名、控制 ID、检查摘要；不得输出 token、secret、DSN、endpoint、payload 或报告正文。 |
| 兼容性 | 不改变已有 API 返回结构，只扩展 `/security` registry 内容和 production-readiness 静态检查。 |
| Retention | 不删除真实数据；保留当前显式删除 baseline，按年龄清理只作为后续实现准入。 |

# Change Boundary
- Allowed: security contracts、production-security gate、production-readiness static checks、local-ci hook、tests、docs、AGENTS、task docs。
- Not allowed: 真实 OIDC/SIEM 接入、用户数据删除、记录存储迁移、WAF/网关策略真实配置、第三方安全平台账号操作。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 把 contract 误报为真实生产 IAM/SIEM | 审计误判生产成熟度 | registry 控制项设为 manual/external pending；文档写明外部连通验证待执行。 |
| retention 清理误删真实数据 | 数据风险 | 本轮不实现删除器，只增加准入 contract 和静态检查。 |
| gate 泄露敏感配置 | 安全风险 | gate output 不打印真实 env 值；策略文件只列变量名。 |
| production-readiness 破坏本地 public-service smoke | 交付回归 | 新检查仅在显式启用公网多租户、SIEM 或 retention days 时阻断；默认通过并输出 warning。 |

# Assumptions and Falsification
- Assumption: 先把 OIDC/SIEM/retention/OWASP 合同化，是进入真实生产安全实现前的最小可验证切片。
  Falsifier: 生产环境已提供真实 OIDC/SIEM 账号并要求立即做 live integration。
- Assumption: retention 自动清理必须单独实现并有审计事件，不能在本轮用脚本直接删除。
  Falsifier: 用户明确要求并提供可恢复测试数据库和删除策略。
- Assumption: OWASP API Top 10 映射作为 regression pack baseline，不能替代第三方渗透测试。
  Falsifier: 审计要求每项都必须有真实攻击流量或 DAST 证据。

# Critical Ambiguities
- 真实 IdP 类型未定：OIDC provider、企业 SSO、GitHub OAuth、Cloudflare Access 或自建 IAM 待生产阶段选择。
- 真实 SIEM/不可变存储未定：云日志、WORM bucket、第三方 SIEM 或企业平台待生产阶段选择。
- retention 删除语义未定：tombstone_then_purge 或 hard_delete 需要产品与合规确认。

# Debug Evidence Contract
- 调试模式: `Optional`
- 本任务不是 bugfix；无需 `DEBUG.md`。
- 如果 gate、production-readiness 或 quick CI 失败，必须记录失败命令、失败检查项、根因和回归验证。

# Task Package Context Map
| Package | Required Context |
| --- | --- |
| TP-01 | D8 roadmap、security registry、security smoke、production-readiness。 |
| TP-02 | SecurityControl schema、registry、production security policy。 |
| TP-03 | production-security gate、production-readiness、privacy boundary。 |
| TP-04 | local CI、regression tests、env examples、docs/AGENTS。 |
| TP-05 | validation evidence、task docs、closeout packet。 |
