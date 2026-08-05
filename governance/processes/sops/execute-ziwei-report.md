---
id: SOP-CAP-ZIWEI-EXECUTE
type: process
status: current
owner: fate-analysis
route_key: execute_ziwei_report
route_aliases: ["生成紫微报告", "执行紫微斗数排盘", "计算紫微 capability"]
capability_id: ziwei
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 执行紫微斗数报告

## 任务定义
使用统一 `CapabilityExecutor` 调用已准入的 `ziwei` provider，独立生成紫微结构或 Markdown，不与综合八字混排。

## 当前状态
available、L4 production、provider `fate_core.usecases.calculate_ziwei`、engine `fate-core-ziwei-v1`。

## 适用场景
紫微十二宫、星曜、四化和运限的独立排盘；不适用于修改星曜规则、闰月口径或混合八字报告。

## 输入要求
必填 `birthDateTime`、`gender`、`longitude`、`latitude`；可选 `name`、`birthPlace`、`useTrueSolarTime`。时间未知必须拒绝。

## 前置条件
完成 bootstrap；地点解析到 WGS84/IANA 时区；明确公历输入与真太阳时选择。

## 默认工具链
`bash scripts/capability-cli.sh ziwei`；Markdown 使用 Web/API `reportSystem=ziwei`；验证使用 L4 golden smoke。

## 固定路径
- Registry：`contracts/fate/capabilities/registry.json`
- Profile：`contracts/fate/capabilities/profiles/ziwei.json`
- Use case：`domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_ziwei.py`
- Canonical renderer：`domains/experience-delivery/services/fatecat-delivery/src/report_generator.py`

## 成熟参数
默认启用真太阳时；CLI 优先 `--input-file`；异步任务携带唯一 `Idempotency-Key`；报告体系固定 `ziwei`。

## 分步执行流程
1. 校验出生时间、性别、坐标和地点时区。
2. 执行 `bash scripts/capability-cli.sh ziwei --input-file <input.json> --pretty --output-file <output.json>`。
3. Markdown 请求通过统一 report job 提交 `options.reportSystem=ziwei`。
4. 检查十二宫完整性、星曜结构、四化、运限和 evidence。

## 幂等与增量策略
相同规范化输入和 engineVersion 应稳定复现；重试异步调用时复用幂等键，规则升级后必须记录新版本。

## 限速与并发规则
沿用 delivery 的每分钟 120、并发计算 2、job worker 1 默认值；不得通过多客户端无界并发绕过。

## 输出目录
`infra/runtime/local-state/exports/reports/ziwei/`；临时输入放 `/tmp/fatecat-ziwei-*`。

## 命名规范
`ziwei-<UTC timestamp>-<short-sha>.json|md`，证据文件追加 `-evidence.json`。

## 质量验收门禁
运行 registry 中 capability/API tests、`bash scripts/bazi-ziwei-l4-golden-smoke.sh` 和 `bash scripts/multi-surface-semantic-diff.sh --report-system ziwei`。

## 失败处理
十二宫不完整、星曜/四化缺字段、policy/snapshot gate 失败或 provider 异常时停止交付并保留脱敏错误摘要。

## 恢复与重试策略
只对瞬时 I/O 或 job 状态进行有界重试；计算逻辑失败必须修复输入或 provider，不允许换入口掩盖。

## 安全边界
不作确定未来承诺；不得输出恐吓、歧视或替代专业判断的结论；输入和正文不进入 tracked evidence。

## 临时文件清理
删除 `/tmp/fatecat-ziwei-*`；长期保留仅限 hash、gate 和版本证据。

## 运行记录登记
记录 commit、provider/engineVersion、输入/输出 hash、reportSystem、gate 结果和执行入口。

## 明确禁止事项
- 禁止与 `bazi` 同一报告混排。
- 禁止前端或 Bot 重算命盘。
- 禁止把 legacy/vendor 输出直接冒充 canonical provider 结果。
