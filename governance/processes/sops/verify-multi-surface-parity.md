---
id: SOP-DEV-MULTI-SURFACE-PARITY
type: process
status: current
owner: experience-delivery
route_key: verify_multi_surface_parity
route_aliases: ["检查多端同源", "对比 Web API Bot 报告", "验证 Markdown 一致性"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 验证多交付面语义一致性

## 任务定义
验证 API direct/job、Web direct/job、Bot dry-run、CLI 和 Skill 对 canonical 结果的语义一致性。

## 当前状态
`bazi`、`ziwei` 本地 semantic diff gate 可用；真实 Telegram/HF live 另行验证。

## 适用场景
报告模板、delivery、API、Web、Bot、CLI 或 Skill 入口变更后的回归。

## 输入要求
可选 `--report-system bazi|ziwei`；输出 JSON 路径；使用固定匿名 fixture。

## 前置条件
bootstrap 完成；canonical renderer 和各 delivery adapter 可导入；不得替换 fixture 为真实用户数据。

## 默认工具链
`bash scripts/multi-surface-semantic-diff.sh --output-json <file>`。

## 固定路径
Contract `contracts/fate/delivery/multi-surface-semantic-diff.json`；实现 `scripts/multi-surface-semantic-diff.py`；renderer `report_generator.py`。

## 成熟参数
默认同时覆盖 bazi/ziwei；比较 normalized semantic hash，不保存完整报告；CLI/Skill 作为 evidence surface。

## 分步执行流程
1. 跑目标体系 semantic diff。
2. 核对所有 surface 状态、hash 和 canonical chain。
3. 失败时定位最早分叉的 adapter/renderer。
4. 运行 surface/API/Web/Bot focused tests。
5. Quick CI 收口。

## 幂等与增量策略
同一 commit/fixture/profile 应产生相同 semantic hash；变更 profile 后旧证据 stale。

## 限速与并发规则
TestClient/job 轮询有界，默认等待 8 秒；不并发修改全局环境或 renderer。

## 输出目录
`infra/runtime/local-state/exports/multi-surface/` 或 `/tmp/fatecat-multi-surface-*`。

## 命名规范
`semantic-diff-<systems>-<short-sha>-<UTC>.json`。

## 质量验收门禁
所有受支持 surface passed、normalized hash 相同、planned capability 拒绝、正文不泄露。

## 失败处理
任何单 surface 差异都 block；不得通过从比较列表删除入口解决。

## 恢复与重试策略
修复 canonical adapter 后重跑；只有轮询瞬时超时可在相同输入下有限重试。

## 安全边界
输出只存 hash/key/status；不保存完整报告、出生信息、Bot token。

## 临时文件清理
删除 TestClient/runtime 临时状态和失败正文；保留 summary/hash。

## 运行记录登记
记录 commit、systems、surface 列表、hash、差异路径、测试和 live 未验证项。

## 明确禁止事项
- 禁止前端或 Bot 自行拼报告。
- 禁止把 dry-run 当真实 Bot/HF live。
- 禁止归一化掉真实语义差异。
