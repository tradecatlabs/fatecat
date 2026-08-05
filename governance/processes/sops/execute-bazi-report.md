---
id: SOP-CAP-Bazi-EXECUTE
type: process
status: current
owner: fate-analysis
route_key: execute_bazi_report
route_aliases: ["生成综合八字报告", "执行八字排盘", "计算八字 capability"]
capability_id: bazi
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 执行综合八字报告

## 任务定义
使用已准入的 `bazi` provider 生成结构化八字结果；需要 Markdown 时通过统一 delivery 报告链路生成，不在调用端拼接章节。

## 当前状态
`contracts/fate/capabilities/registry.json`：available、L4 production、`fate-core-bazi-v1`。

## 适用场景
- 单次八字排盘、Agent 调用、API 报告任务或匿名回归样本。
- 不适用于修改算法、格局规则、报告模板或专家校勘。

## 输入要求
必填 `birthDateTime`、`gender`、`longitude`、`latitude`；可选 `name`、`birthPlace`、`useTrueSolarTime`。未知时间不得猜测，输入包含个人数据时不得进入命令历史或 tracked 文件。

## 前置条件
已运行 `bash scripts/bootstrap.sh`；经纬度为 WGS84；性别和时间口径明确；输出位置可写。

## 默认工具链
结构化结果使用 `bash scripts/capability-cli.sh bazi`；纯分析兼容入口使用 `bash scripts/pure-analysis.sh`；Markdown 使用 Web/API 的 canonical renderer。

## 固定路径
- 注册表：`contracts/fate/capabilities/registry.json`
- Profile：`contracts/fate/capabilities/profiles/bazi.json`
- Provider：`domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py`
- 报告器：`domains/experience-delivery/services/fatecat-delivery/src/report_generator.py`

## 成熟参数
默认 `useTrueSolarTime=true`；CLI 使用 `--input-file` 和 `--pretty`；异步 API 使用唯一 `Idempotency-Key`；生产默认请求超时 30 秒、最大并发计算 2。

## 分步执行流程
1. 将脱敏输入写入 `/tmp/fatecat-bazi-input.json`。
2. 执行 `bash scripts/capability-cli.sh bazi --input-file /tmp/fatecat-bazi-input.json --pretty --output-file <output.json>`。
3. 需要 Markdown 时提交 `/api/v1/report/jobs`，指定 `options.reportSystem=bazi`，轮询终态。
4. 检查 capability、provider、policyGate、snapshotGate 和 evidence 引用。

## 幂等与增量策略
同一规范化输入和 engineVersion 应产生可复现结构；异步任务复用相同 `Idempotency-Key`，不得重复提交。

## 限速与并发规则
遵守 `FATE_RATE_LIMIT_PER_MINUTE=120`、`FATE_MAX_INFLIGHT_CALCULATIONS=2`、报告 worker 默认 1；批量任务串行或有界并发，不得绕过服务限流。

## 输出目录
人工导出写 `infra/runtime/local-state/exports/reports/bazi/`；临时输入写 `/tmp`；API 结果由配置的 job store 管理。

## 命名规范
`bazi-<UTC-YYYYmmddTHHMMSSZ>-<short-sha>.json`；Markdown 使用同名前缀和 `.md`。

## 质量验收门禁
运行 capability protocol、API contract、solar term golden，以及 `bash scripts/bazi-ziwei-l4-golden-smoke.sh`；公开 Markdown 必须通过 profile snapshot/policy gate。

## 失败处理
字段缺失、地点不确定、planned/unknown capability、policy 或 snapshot 失败均停止，不生成半完整报告。

## 恢复与重试策略
输入错误修正后新建运行；瞬时任务失败按服务配置的有界重试处理，默认最大尝试 1，不手工无限重放。

## 安全边界
结果仅作传统文化研究与娱乐参考；不得替代医疗、法律、金融或心理判断；真实出生信息不得提交。

## 临时文件清理
验收后删除 `/tmp/fatecat-bazi-input.json`；运行态清理由 `bash scripts/clean-runtime.sh --dry-run` 预览后执行。

## 运行记录登记
登记 commit、engineVersion、规范化输入 hash、输出 hash、命令、门禁结果和外部状态；不得登记报告正文或个人数据。

## 明确禁止事项
- 禁止前端、Bot、Skill 自行拼 Markdown。
- 禁止猜测出生时间、性别、地点或静默替换输入。
- 禁止把神煞、称骨作为格局喜忌的核心证据。
