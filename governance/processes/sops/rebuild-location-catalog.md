---
id: SOP-DATA-LOCATION-CATALOG
type: process
status: current
owner: fate-analysis
route_key: rebuild_location_catalog
route_aliases: ["更新出生地区库", "重建地点目录", "更新时区数据"]
created: 2026-07-24
last_reviewed: 2026-07-24
review_cycle: P60D
---

# 重建地点与时区目录

## 任务定义
从 hash 锁定的 GeoNames/行政区来源确定性构建出生地点、WGS84 坐标和 IANA 时区数据产品。

## 当前状态
生产数据产品已存在；构建器、source lock、manifest、查询和回归门禁完整。

## 适用场景
来源版本升级、行政区修订、时区数据修复或 catalog 可复现性检查；不用于单次地点查询。

## 输入要求
`sources.lock.json` 中登记的全部来源文件，或显式允许 `--download`；文件 hash 必须完全匹配。

## 前置条件
`.venv` 安装 data 依赖；网络下载获准；目标数据产品没有并发写入；变更已有评审任务。

## 默认工具链
`.venv/bin/python scripts/build-location-catalog.py`、location regression、data supply-chain gate。

## 固定路径
`domains/fate-analysis/data-products/locations/{sources.lock.json,location_catalog.ndjson.gz,manifest.json}`。

## 成熟参数
优先 `--source-dir <verified-dir>`；仅缺来源时用 `--download`；下载超时 120 秒；运行时不联网。

## 分步执行流程
1. 备份现有 manifest/hash，不复制用户 runtime index。
2. 准备 source dir 并校验 lock。
3. 执行 builder。
4. 比较记录数、来源 hash、输出 hash、国内层级和全球时区覆盖。
5. 跑 location/API/Web/data gates。

## 幂等与增量策略
相同 source lock 生成相同 gzip 内容和 manifest；来源升级必须整体重建，不增量拼接旧 catalog。

## 限速与并发规则
下载串行且每个来源只取一次；单进程构建 canonical；运行时索引由文件锁原子重建。

## 输出目录
canonical 数据产品写固定 locations 目录；下载源默认临时目录；运行时 SQLite 写 ignored local-state。

## 命名规范
canonical 文件名固定；来源文件名必须与 source lock 的 `fileName` 一致。

## 质量验收门禁
location catalog/location/Web/API tests、data supply-chain、clean production env、structure 和 Quick CI。

## 失败处理
来源缺失、hash 不符、重名静默选取、时区为空或统计异常立即停止并保留旧产品。

## 恢复与重试策略
下载失败按来源重新获取；hash 失败不得重试绕过；构建失败删除候选后从 lock 重跑。

## 安全边界
数据产品不含用户输入；日志不得记录用户地点/坐标；城市中心点不宣称精确地址。

## 临时文件清理
删除下载临时目录和 runtime index；不得删除 source lock 或已通过的 canonical 产品。

## 运行记录登记
记录来源版本/hash、输出 hash、记录数、构建时长、内存峰值和门禁。

## 明确禁止事项
- 禁止在线地理编码成为运行时必需依赖。
- 禁止忽略 source hash。
- 禁止保留旧 CSV fallback 或双轨解析器。
