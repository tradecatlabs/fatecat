# Repo Evidence
- 调试模式: Optional
- `contracts/fate/security/registry.json` 原先只有 source hygiene，并明确该门禁不是完整 secret scanner。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 IMP-10 把“专用 secret scanner”列为未完成。
- `.gitignore` 已忽略 `.env`、`.env.*`、运行态、raw、缓存和本地导出；scanner 不应读取 ignored 真实本地凭证。
- `scripts/check-source-hygiene.sh` 只检查 raw/运行态/个人路径误入 Git，不做密钥模式识别。
- `scripts/local-ci.sh --profile quick` 已有 source hygiene、privacy fixtures、public release policy，可新增 secret scan 步骤。

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不输出密钥原文 | finding 只写路径、行号、规则、severity、短指纹和脱敏长度。 |
| 不读取真实 `.env` | 候选文件来自 `git ls-files --cached --others --exclude-standard`，ignored 文件不进入扫描。 |
| 不误扫外部供应链 | 默认排除 `tools/reference-repos/` 和 `governance/archive/`。 |
| 不扩大生产承诺 | 文档写明本地启发式扫描不能替代云端 secret scanning 或人工凭证审计。 |
| 可复核 | scanner 输出 JSON，测试覆盖命中、占位符忽略和 CLI summary。 |

# Change Boundary
- 可改：`scripts/secret-scan.py`、`scripts/secret-scan.sh`、`contracts/fate/security/secret-scan-allowlist.json`、security schema/registry、local CI、相关 AGENTS、回归测试、API 文档、roadmap 和 0025 任务文档。
- 不改：真实 secret、生产部署配置、鉴权模型、报告算法、provider executor、外部 CI/workflow 触发方式。

# Risk Matrix
| Risk | Impact | Mitigation |
| --- | --- | --- |
| 启发式 scanner 误报 | quick CI 被阻断 | allowlist 只允许占位符和示例片段，不允许真实 secret。 |
| scanner 漏报 | 误以为安全 100% | 文档明确本地 scanner 不替代云端 secret scanning、人工复核或生产凭证审计。 |
| 输出疑似密钥原文 | 二次泄露 | 输出 fingerprint/redacted，不输出 match 原文。 |
| 扫描外部 reference repo | 第三方历史样例造成噪声 | 默认排除 reference repos 和 archive。 |

# Assumptions and Falsification
- 假设：当前 first-party worktree 不含真实 secret。反证：`bash scripts/secret-scan.sh` 返回 failed。
- 假设：scanner 只需要本地标准库即可稳定运行。反证：quick CI 的 shell/ruff/pytest 失败。
- 假设：本任务不需要真实外部凭证。反证：需求变成云端 secret scanning、GitHub Advanced Security 或生产 secret store 审计时，应另起任务。

# Critical Ambiguities
- 是否接入 gitleaks/trufflehog/GitHub secret scanning：本任务不引入外部依赖，只做本地可复现 scanner；成熟外部工具可作为后续供应链增强。
- OAuth/OIDC、RBAC、审计日志、retention、真实 live smoke 不属于本任务。

# Debug Evidence Contract
- 本任务不是 bugfix；无需 `DEBUG.md` 根因闭环。
- 若 scanner 或 quick CI 失败，失败命令、脱敏 finding 摘要和修复证据必须回填 `STATUS.md` Evidence Log。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01 | 读取 security registry、source hygiene、roadmap 和 quick CI。 |
| TP-02 | 新增 scanner/allowlist，确保不输出疑似密钥原文。 |
| TP-03 | 补 schema/registry/API tests、scanner tests、docs 和 quick CI。 |
| TP-04 | 执行 scanner、focused tests、ruff/format、quick CI、diff check 和 task validators。 |
