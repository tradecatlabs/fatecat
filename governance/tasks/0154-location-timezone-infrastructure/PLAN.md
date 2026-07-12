# Planning Summary
先锁定数据来源和字段契约，再实现可重建索引与时间标准化，最后把 Web/API 接到同一服务端链路；不围绕旧 CSV 建兼容层。

# Lifecycle Gates
以下阶段不得跳过 gate；失败必须回到对应阶段修复并重新验证。

- SPEC：地区交互、数据边界、时间语义和零美化限制已明确。
- PLAN：最终结构、删除项、依赖、许可、验证和回滚路径已记录。
- BUILD：canonical 数据、runtime index、resolver、Web/API 和契约同步落地。
- TEST：数据全量质量、重名、坐标、时区、DST、Web/API 和 clean-env 必须通过。
- REVIEW：检查 correctness、security、performance、architecture、contract、repo hygiene 和 document drift。
- SHIP：本地门禁通过后可进入版本控制；本轮不自动 commit/push。

# Simplest Path
使用固定提交的 `province-city-china` 作为现行行政区层级，GeoNames 作为全球地点/WGS84/IANA 时区来源，Python `zoneinfo` 解释历史偏移，`timezonefinder` 处理用户直接坐标，SQLite 提供本地索引，原生 HTML 提供搜索和候选选择。

# Split Strategy
- TP-01：数据与契约。
- TP-02：解析与时间核心。
- TP-03：交付面接入。
- TP-04：验证与治理。

# Execution Waves
- Wave 1: TP-01
- Wave 2: TP-02
- Wave 3: TP-03
- Wave 4: TP-04

# Runtime Workflow Contract
- 构建脚本只写 canonical 目标文件和 manifest；下载临时文件不进入仓库。
- 运行时只写 `infra/runtime/local-state/database/locations/`。
- 失败时依据 source hash、manifest、SQLite metadata 和边界测试定位，不放宽校验换绿。

# Next Executable Leaves
- None.

# Dependency Graph
TP-01 -> TP-02 -> TP-03 -> TP-04

# Rollback Protocol
- 回滚整个地点协议切片并恢复上一个已发布版本；不得同时运行新旧解析器。
- canonical gzip 和 runtime SQLite 均无用户数据；缓存可直接删除并由 manifest 重建。
- 若上游刷新失败，保留当前已锁 hash 的最后已知良好 catalog，不接受未经复核的新 hash。
