# Task Overview
- Task ID: `0154`
- Slug: `location-timezone-infrastructure`
- Objective: `建立可审计、可复现的出生地点与历史时区基础设施：稳定地点契约、国内与全球地点解析、WGS84 坐标、IANA 时区、出生时间口径、原生 Web 交互和完整回归门禁。`
- Status: `Done`

## In Scope
- 建立有来源锁、hash、许可和精度边界的全球地点 canonical 数据产品。
- 统一稳定地点 ID、国内/海外/坐标三种输入模式、WGS84 和 IANA 时区。
- 处理 `local_civil`、`beijing_time`、`utc` 与 DST gap/fold。
- Web 使用一个原生地区输入框完成国内行政区模糊搜索、完整路径候选、稳定 ID 绑定、服务端校验和无 JavaScript 降级。
- Bazi API 与 Web 复用同一地点和时间标准化链路。
- 退役旧坐标表和旧依赖，补供应链、契约、文档、测试与门禁。

## Out of Scope
- 不复制问真八字视觉样式、地区数据或固定 GMT 表。
- 不实现地图、地址自动补全 SaaS、浏览器定位或第三方在线地理编码调用。
- 不修改八字/紫微领域算法与 Markdown 报告结构。
- 不执行生产部署、commit 或 push；版本交付由用户后续明确指令触发。

## Task Package Tree
- ROOT
  - TP-01：地点数据产品与供应链契约
  - TP-02：地点解析与历史时区核心
  - TP-03：Web/API 接入与降级路径
  - TP-04：测试、文档、治理与审查收口

## Requirement Alignment
- 截图与参考站点仅用于理解地区选择任务，不复制其视觉或私有数据；最终 Web 采用单输入框模糊搜索与完整路径候选。
- 实现遵守零美化语义 HTML，核心流程由服务端完成，JavaScript 只增强报告异步提交。
- 地点、坐标、时区、时间口径和精度均形成稳定字段，不默认猜测或静默替换。

## Task Package Overview
| Task Package ID | Parent | Priority | Type | Depends On | Objective |
| --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | P0 | data/contract | - | 构建可追溯全球地点数据产品与协议。 |
| TP-02 | ROOT | P0 | core | TP-01 | 实现稳定 ID、IANA 时区和时间标准化。 |
| TP-03 | ROOT | P0 | integration | TP-02 | 接入 Web/API 并保持无脚本降级。 |
| TP-04 | ROOT | P0 | verification | TP-03 | 完成质量门禁、文档与独立审查。 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
