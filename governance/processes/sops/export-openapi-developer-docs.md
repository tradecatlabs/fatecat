---
id: SOP-DEV-OPENAPI-DOCS
type: process
status: current
owner: developer-platform
route_key: export_openapi_developer_docs
route_aliases: ["导出 OpenAPI", "校验开发者文档", "更新接口快照"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 导出 OpenAPI 与校验开发者文档

## 任务定义
从当前 FastAPI app 导出 canonical OpenAPI JSON，并验证开发者接入必备路径、示例和 sandbox 文档。

## 当前状态
导出器、developer docs smoke 和 platform gate 可用；PyPI/npm 和公网 developer portal 未由此证明。

## 适用场景
API contract、路由、schema、错误码或开发者文档变更后。

## 输入要求
可选 `--output`；当前 app 必须可导入且无需真实外部凭证启动 schema。

## 前置条件
bootstrap 完成；API tests 通过；确定是否需要 contract/changelog 同步。

## 默认工具链
`bash scripts/export-openapi.sh --output <file>`、`developer-docs-smoke.sh`、`developer-platform-gate.sh`。

## 固定路径
OpenAPI schema 来自 delivery app；developer contracts 位于 `contracts/fate/developer/`；文档位于 `docs/reference-materials/operations/`。

## 成熟参数
输出 JSON 使用确定性排序；必须包含 capability、report job、health 和资源发现必备路径。

## 分步执行流程
1. 导出到 `/tmp` 候选。
2. JSON/schema 校验并比较现有 contract。
3. 更新必要开发者文档和 changelog。
4. 运行 docs/platform/portal gates。
5. 跑 API contract 和 Quick CI。

## 幂等与增量策略
同一 app/commit 导出应稳定；只接受由真实路由/schema产生的差异，不手改生成 JSON。

## 限速与并发规则
本地导出单进程，无网络；不要与正在修改 app schema 的进程并发。

## 输出目录
候选 `/tmp/fatecat-openapi.json`；正式 artifact 由 release/developer contract 指定。

## 命名规范
`openapi-<short-sha>.json`；公开稳定入口仍为 `/openapi.json`。

## 质量验收门禁
JSON 有效、必备 paths/schema/error codes 完整、docs smoke/platform gate/API tests PASS。

## 失败处理
导入失败、路径缺失、文档/contract 漂移或 breaking change 未记录时 block。

## 恢复与重试策略
修复 app/schema 后重新导出；不得回写旧快照掩盖 breaking change。

## 安全边界
OpenAPI 不包含 token、内部路径、生产 secret 默认值或私人示例。

## 临时文件清理
删除候选 JSON 和构建缓存；保留 release 绑定 artifact/hash。

## 运行记录登记
记录 commit、schema hash、path 数、breaking diff、gates 和文档更新。

## 明确禁止事项
- 禁止手改生成 OpenAPI。
- 禁止把 docs smoke 称为公网 SDK 已发布。
- 禁止未记录 breaking change。
