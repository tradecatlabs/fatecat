# Repo Evidence
- 原实现依赖单一中国坐标 CSV，缺少全球地点、稳定 ID、来源许可、IANA 时区和历史 DST 语义。
- 旧坐标数据存在质量异常，且 `china-region/addressparser/pandas` 增加运行时所有权面。
- Web 已遵守零美化语义 HTML，但旧地区输入只有自由文本/datalist，无法可靠处理全球重名地点和时间口径。
- 现有计算引擎以北京时间墙上时间为入口，因此需要在 delivery 边界完成可审计规范化。

# Constraints Matrix
- 用户要求原生 HTML，不引入 CSS、视觉类、前端框架或复制参考站样式。
- 地点不得默认猜测；重名和模糊输入必须返回候选稳定 ID。
- 坐标统一 WGS84；时区使用 IANA tzdb，不使用固定 GMT 偏移模拟历史规则。
- canonical 数据可公开分发但必须保留 MIT/CC-BY-4.0 来源归属。
- 运行时 SQLite 是可重建缓存，不得进入 Git 或成为第二真相源。

# Change Boundary
- `domains/fate-analysis/data-products/locations/` 与数据供应链契约。
- `contracts/fate/locations/` 与 capability common input fields。
- delivery 的 location/catalog/models/main/web form/service/UI。
- 依赖锁、构建脚本、测试、README/AGENTS/module context 和任务文档。

# Risk Matrix
- 高：错误时区或 DST 处理会改变四柱计算的实际时刻。
- 高：重名地点静默选中会产生不可察觉的错误命盘。
- 中：canonical 大目录和运行时 SQLite 混淆会污染仓库或导出包。
- 中：上游日更数据未锁 hash 会破坏可复现性。
- 低：首次运行构建 SQLite 有约 1-2 秒一次性成本，后续查询为毫秒级。

# Assumptions and Falsification
- 假设：现有命理计算入口继续接收北京时间墙上时间；若核心引擎改为 aware datetime，规范化边界应迁入 fate-core。
- 假设：城市/行政区中心点足够用于当前真太阳时近似；若用户需要出生医院级精度，应提交直接 WGS84 坐标。
- 证伪条件：相同 catalog hash 不能构建相同记录数/稳定 ID，或 DST golden 与 zoneinfo 不一致。

# Critical Ambiguities
- 历史行政区迁移和已撤销代码尚未作为独立版本化历史目录提供；当前协议使用现行行政区稳定代码。
- GeoNames 城市中心点与行政边界不等于精确地址，因此必须返回 `coordinatePrecision`。

# Debug Evidence Contract
- 调试模式: Optional
- 根因证据：catalog hash、manifest 统计、source lock、稳定 ID、IANA 时区和边界测试。
- 禁止以浏览器截图或本机缓存作为数据正确性的唯一证据。

# Future-Optimal / Ponytail Contract
- Target end state: 一个统一、离线、可追溯的地点事实服务，所有交付面共享稳定 ID、WGS84、IANA 时区和明确时间口径。
- Real constraints: 现有计算引擎北京时间入口、公开 API、零美化 Web、免费 HF 运行资源和许可归属。
- Inertia constraints: 旧 CSV、模糊首选、固定 Asia/Shanghai 默认、旧依赖和历史文档。
- Kill list: 旧坐标表、运行时模糊首选、固定 GMT 表、自建 DST 规则、前端私有地点数据和在线地理编码强依赖。
- Selected ladder rung: 复用 GeoNames、IANA tzdb、timezonefinder、SQLite 与原生 HTML；自研只负责数据适配和业务协议。
- Proof point: source/hash gate、全量目录质量测试、DST gap/fold、Web/API 联合回归和 clean-env dependency smoke 通过。
- Falsifier: 同名地点被静默选择、时区不一致仍计算、运行缓存进入 Git、或生产环境缺失 timezonefinder/tzdata。
- Migration slice: 一次性切换 canonical 数据和共享解析链路，删除旧资产，不维护双轨 fallback。

# Document-Driven Impact
- Operating model: 不变；仍是测算基础设施。
- Toolchain: 新增地点目录构建器与数据质量回归，quick CI 纳入测试。
- Contracts: 新增 location protocol，更新 capability common fields 和供应链资产。
- Module context/README/AGENTS: 已同步 delivery、data-products、scripts、contracts 和 Web/location context。
- ADR: 无需新增；该实现遵循既有成熟复用与单一真相源原则。

# Task Package Context Map
## TP-01
- 目标: 建立全球地点 canonical 数据产品、source lock、manifest、供应链注册和契约。
- Verify: `bash scripts/data-supply-chain-gate.sh`。

## TP-02
- 目标: 实现稳定地点 ID、SQLite 只读索引、IANA 时区和出生时间规范化。
- Verify: `pytest tests/regression/test_location.py tests/regression/test_location_catalog.py`。

## TP-03
- 目标: 接入原生 Web 候选选择和 Bazi API，共享同一解析链路。
- Verify: `pytest tests/regression/test_web_html.py tests/regression/test_api_contracts.py`。

## TP-04
- 目标: 同步文档/门禁，执行 clean-env、quick CI、governance strict 和 review。
- Verify: `bash scripts/local-ci.sh --profile quick` 与治理严格校验。
