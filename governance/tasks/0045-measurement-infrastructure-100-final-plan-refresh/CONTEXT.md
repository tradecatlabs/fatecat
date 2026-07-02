# Repo Evidence
- 当前目录：`/home/lenovo/.projects/fatecat`。
- 当前分支：`main...origin/main`，工作树存在大量未提交改动，不能把本地计划当作已发布事实。
- 已有路线图：`docs/reference-materials/roadmap/测算基础设施100%实现计划.md`。
- 已有需求文档：`docs/reference-materials/roadmap/测算基础设施需求文档.md`。
- 已有任务链：`governance/tasks/0009` 到 `0044` 覆盖基础设施规划、资源、job、provider、report、evaluation、observability、security、delivery、release evidence。
- 已有 live release gate：`contracts/fate/delivery/release-gate.json` 要求 local CI、远端 CI、生产 API、HF Space、Bot、container、SBOM/provenance、rollback、clean git。
- 0044 记录公开 HF/API live gate 已通过：`passed=7,pending=3,failed=0`；剩余 pending 为远端 CI 当前 commit、Telegram Bot live、clean git。

# Constraints Matrix
| 约束 | 处理 |
| --- | --- |
| 用户要求深度调研并制作完整计划 | 执行外部一手资料调研，刷新本地 roadmap |
| 当前任务只做计划 | 不改业务代码，不提交，不推送 |
| 不能伪造生产证据 | 所有外部项保持 pending 或“外部连通验证待执行” |
| 仓库已有大量任务 | 不重建体系，复用现有 0009-0044 资产 |
| 文档驱动 | roadmap 和任务包同步更新 |

# Change Boundary
- 允许修改：
  - `governance/tasks/0045-measurement-infrastructure-100-final-plan-refresh/*`
  - `governance/tasks/INDEX.md`
  - `docs/reference-materials/roadmap/测算基础设施100%实现计划.md`
- 禁止修改：
  - 业务源码
  - provider 计算逻辑
  - API 行为
  - Git 历史或远端状态

# Risk Matrix
| 风险 | 等级 | 控制 |
| --- | --- | --- |
| 把规划写成已完成 | 高 | 每个外部项显式标注待验证 |
| 重复 0027 旧计划而不反映 0044 状态 | 中 | roadmap 增加当前 live gate 现状和 0046+ 路线 |
| 外部资料引用不清 | 中 | 只使用官方/一手资料链接 |
| 规划过大不可执行 | 中 | 拆成 release closure、runtime、provider、eval、security、developer platform 六组任务 |

# Assumptions and Falsification
- 假设：FateCat 的最高定位是测算基础设施，而非单一排盘工具。
- 假设：100% 的定义是基础设施交付闭环，不是术数功能无限堆叠。
- 可证伪条件：如果后续目标改为纯内容站或单一八字工具，则本计划的多 provider、developer platform、SRE/security 投入需要降级。
- 可证伪条件：如果生产环境不提供真实 token、Bot、OIDC、SIEM 或远端 CI 权限，则对应 live evidence 不能完成，只能保持外部验证待执行。
- 调试模式: `Optional`

# Critical Ambiguities
- 真实生产身份系统、SIEM、监控平台、Bot token 和 GitHub Actions 权限是否可用：当前无法在仓库内证明。
- 是否需要真实 registry push 和签名：当前只有本地 container imageId baseline，不等于发布 registry digest。
- 是否要把 `100%` 定义为“公开可商用生产”还是“本地可审计基础设施 baseline”：本计划按公开生产基础设施口径设计。

# Debug Evidence Contract
Not Required。本任务是规划和文档刷新，不处理具体 bug。

# Task Package Context Map
- TP-01.01 使用官方资料建立同构映射。
- TP-02.01 使用当前任务链、registry、release gate 和 roadmap 复核事实。
- TP-03.01 将剩余路线收敛到 0046+ 任务序列。
- TP-04.01 运行任务文档和 markdown 校验。
