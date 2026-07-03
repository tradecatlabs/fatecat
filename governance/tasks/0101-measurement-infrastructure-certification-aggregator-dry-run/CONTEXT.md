# Repo Evidence
- 当前分支：`main`，0100 已提交并推送；0101 worktree 正在实现 certification aggregator dry-run。
- 直接上游计划：`docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 的 `Wave A A2`。
- 已有 local-ci 产物来源：`scripts/local-ci.sh` 会生成 release、audit、provider、core quality、security、SRE、runtime、developer 等 gate summary JSON。
- 已有反伪造边界：多个 gate 在缺少真实外部环境时输出 `外部连通验证待执行`、`blocked` 或 `pending`，不能被解释成生产完成。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 只能分析当前 worktree | 不切分支、不合并、不重写历史。 |
| 不能伪造 100% | `status=passed` 才允许 `canClaim100Percent=true`；blocked/pending 均禁止 100% 声明。 |
| 外部系统不可本地证明 | 真实 Bot/API/HF/OIDC/SIEM/OTel/Vault/KMS/多副本 live 均保留为外部连通验证待执行。 |
| 隐私和安全 | certification summary 只保存状态、计数、阻断项和路径，不复制报告正文、出生信息或 secret。 |
| 胶水原则 | 聚合现有 gate JSON，不重新实现 release/audit/security/runtime 等已有门禁。 |

# Change Boundary
允许修改：
- `contracts/fate/audit/measurement-infrastructure-certification.json`
- `scripts/measurement-infrastructure-certification.py`
- `scripts/measurement-infrastructure-certification.sh`
- `scripts/local-ci.sh`
- `tests/regression/test_measurement_infrastructure_certification.py`
- 相关 `AGENTS.md`、API 文档、roadmap 和本任务目录

禁止修改：
- 八字/紫微 provider 计算逻辑
- 真实凭证、`.env`、外部账号配置
- 历史任务目录中的业务证据，除非修复明确的任务索引漂移

# Risk Matrix
| Risk | Impact | Control |
| --- | --- | --- |
| 把 dry-run 说成 100% 完成 | 误导生产判断和审计结论 | `canClaim100Percent` 仅在所有分域 passed 时为 true；blocked/pending 默认阻断。 |
| local-ci artifact 遗漏 | 聚合结果不完整 | contract 列出 required evidence files；缺文件时分域 `failed`。 |
| gate 字段结构差异 | 阻断项漏识别 | 同时支持 dict gate 和字符串 gate，如 `shipGate=blocked`。 |
| 敏感信息泄露 | 安全事故 | forbidden fragments 与 secret scan；summary 只保存路径和状态。 |
| 任务文档漂移 | 审计人员无法复核 | closeout 前运行 task docs validator。 |

# Assumptions and Falsification
- 假设：local-ci 产物目录是 certification aggregator 的唯一输入。
  - 证伪：若某必备 gate 不在产物目录，aggregator 必须输出 failed，不允许脑补。
- 假设：当前本地环境没有真实外部 live 证据。
  - 证伪：除非存在对应 gate JSON 中的 passed live proof，否则保持 blocked/pending。
- 假设：聚合器不需要理解完整日志。
  - 证伪：如果某 gate 只在日志中体现状态而没有 JSON summary，必须先补该 gate 的机器可读输出，不在 aggregator 中解析日志。

# Critical Ambiguities
- 真实外部生产连通是否完成：本任务不解决，统一标记外部连通验证待执行。
- 第三方审计是否已通过：本任务不替代，只准备本地 dry-run 自检证据。
- “100%”是否等于预测准确率：不是。本任务只服务基础设施成熟度，不承诺预测命中率。

# Debug Evidence Contract
- 调试模式: Optional
- 当前任务是新增门禁，不是已复现缺陷修复；若 regression、local-ci 或 secret scan 失败，再升级为 Required 并维护 DEBUG.md。

# Task Package Context Map
## TP-01 certification 需求和契约边界
聚焦 0099 Wave A A2 的证据模型，把 “100% certification” 限定为 local-ci 产物聚合，不直接连外部系统。

### TP-01.01 盘点 local-ci 现有 gate evidence 与不可声明边界
读取 local-ci 产物命名、release/audit/security/runtime/developer/provider/core quality 等 gate 的 JSON 状态字段，明确 forbidden non-claims。

### TP-01.02 定义 certification contract、必备证据和分域状态
新增 contract，列出必备证据文件、输出字段、blocked gate 字段、forbidden fragments、privacy boundary 和 release boundary。

## TP-02 certification aggregator 实现与接线
聚焦最小实现：读取 JSON，按分域输出 status，不复制日志，不重算下游 gate。

### TP-02.01 实现 CLI/wrapper、分域聚合、blocked/pending/failed 语义
实现 Python CLI 与 shell wrapper；缺文件 failed、明确阻断 blocked、外部待执行 pending，合成全 passed 才能通过 `--require-certified`。

### TP-02.02 接入 local-ci summary、AGENTS、API 文档和 roadmap
把 aggregator 加入 quick local-ci，summary 输出 artifact 路径，并更新目录级架构说明和用户可复核命令。

## TP-03 验证与审查
覆盖正负路径，确保 aggregator 不泄漏敏感数据、不伪造通过。

### TP-03.01 增加 regression tests
测试 contract、blocked dry-run、require-certified 拒绝、缺文件失败和合成 full pass。

### TP-03.02 执行 gate smoke、focused tests、ruff、quick local-ci 和 secret scan
以真实命令输出作为 closeout 证据。

## TP-04 closeout 与版本控制
把任务状态、索引、验证证据和远端提交状态收口。

### TP-04.01 同步任务文档、INDEX 和验收清单
任务文档必须通过 decompose/closeout validator。

### TP-04.02 提交、推送并记录远端状态
按 auto-github 执行 commit/push，并明确远端 CI 是否覆盖当前 commit。
