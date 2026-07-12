# Repo Evidence
- 2026-07-13 线上基线：`/`、`/robots.txt`、`/sitemap.xml` 均为 404。
- `/web` 已服务端直出，但缺 canonical、description、author、date 与 JSON-LD。
- 旧 `llms.txt` 有接口说明，但缺明确的实体、能力成熟度分层、高意图问答、来源台账与引用建议。
- GitHub README 与 HF README 未集中暴露 robots、sitemap、OpenAPI 和 capability registry。

# Constraints Matrix
| 约束 | 处理 |
|---|---|
| 零美化 Web | 只增加非视觉 head 元数据，不增加 CSS/class/layout |
| 事实准确 | 生产/planned 状态来自 capability registry |
| 隐私 | 不接入用户追踪；外部指标只定义口径 |
| 自托管 | canonical 基址由 `FATE_PUBLIC_BASE_URL` 配置 |
| 白帽 GEO | 禁止关键词堆砌、伪造内容和排名承诺 |

# Change Boundary
- 交付层公开发现模块和路由
- Web 非视觉元数据
- 根 `llms.txt`、README、HF README、GEO 文档
- GEO 审计脚本、回归、local CI 与 public release gate
- 对应 AGENTS、环境示例和任务治理文档

# Risk Matrix
| 风险 | 缓解 |
|---|---|
| canonical 指向错误域名 | 严格校验仅 scheme+host，默认 HF 正式域名 |
| planned 能力被误报 | llms 分层并用测试锁定 |
| robots 阻断真实公开资源 | 默认 Allow `/`，只限制 metrics、job 和 integration 路径 |
| JSON-LD 事实漂移 | 只写稳定身份与当前公开能力，日期和来源显式 |
| 指标伪造 | 仓库不可测项统一标记外部连通验证待执行 |

# Assumptions and Falsification
- 假设公开规范域名是 `tradecatlabs-fatecat.hf.space`；若迁移域名，通过 `FATE_PUBLIC_BASE_URL` 重新生成。
- 假设 registry 是能力生命周期真相源；若 registry 状态变化，llms 和结构数据必须同步复核。
- 若线上 GEO 审计任一 P0 项失败，则本任务不能进入 ship。

# Critical Ambiguities
- AI 平台真实索引、引用和推荐数据当前无账号/日志证据，不能在仓库内判定。
- HF 免费 Space 的 crawler 日志可见性受平台限制，需要后续边缘网关或平台 analytics 证据。

# Debug Evidence Contract
- 本任务是功能与治理增强，不是缺陷调试；基线 404 和测试失败保留为审计证据，发现真实回归时转入 `DEBUG.md`。
- 调试模式: `Optional`

# Task Package Context Map

## TP-01 GEO 基线
- 输入：固定 GEO 方法、线上公开端点、仓库内容。
- 输出：可复核缺口和不可测指标边界。

## TP-02 机器发现实现
- 输入：基线和 capability registry。
- 输出：root、robots、sitemap、canonical、JSON-LD、llms。

## TP-03 验证门禁
- 输入：公开端点契约。
- 输出：HTTP GEO audit、回归和 public release 接线。

## TP-04 交付闭环
- 输入：本地通过证据。
- 输出：文档、review、GitHub/HF 和线上 audit。
