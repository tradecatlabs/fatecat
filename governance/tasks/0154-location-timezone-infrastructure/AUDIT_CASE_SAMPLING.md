# Audit Case Sampling Decision

- Source: governance/tasks/0154-location-timezone-infrastructure
- Fixed Problem: 旧地点实现缺少稳定地点、历史时区和可复现供应链；初版 Web 又把后端地点模式、时间口径和 DST fold 全部暴露为控件，偏离用户要求的最小地区选择交互。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: location-data-semantics-and-backend-capability-ui-leakage
- Trigger Signals: 生产地点数据无来源锁；同名地点静默选择；固定 offset 替代 IANA；后端支持能力被直接映射成默认 Web 控件；单一地区选择任务出现模式和技术参数。
- Evidence: `contracts/fate/locations/registry.json`；`domains/fate-analysis/data-products/locations/manifest.json`；`tests/regression/test_location_catalog.py`；`tests/regression/test_location.py`；`tests/regression/test_web_html.py`；移动端 Chrome 联动实测；`bash scripts/data-supply-chain-gate.sh`。
- No-Case Reason: 不新增独立案例；数据问题已由 location contract 和供应链门禁覆盖，界面范围问题已由 `ponytail-complexity` 审查维度及项目 module context、README 和回归测试覆盖。

## Reusable Audit Questions

- 生产地点数据是否具备来源版本、hash、许可、坐标系和精度边界？
- 重名、模糊地点、时区冲突、DST 缺口和重复时刻是否显式失败？
- canonical 数据与运行时索引是否分离，缓存能否删除重建且不会进入 Git？

## Evidence Required

- source lock 与 canonical output hash 对照。
- 全量记录唯一性、IANA 时区有效性和现行行政区代码检查。
- Web/API 海外时间与 DST 边界回归。

## Correction Sampling

本次最终纠正要求页面只存在一个可见地区输入框；复杂地区能力仍由 API/后端测试覆盖；模糊候选、稳定 ID 失效、零美化、无脚本和移动端回归均必须通过。
