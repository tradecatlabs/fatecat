# Acceptance Checklist

# Global Standards
- [x] 成熟复用：GeoNames、IANA tzdb、timezonefinder、SQLite、原生 HTML。
- [x] 无默认猜测：重名、模糊、时间口径和 DST fold 均有显式边界。
- [x] 数据供应链有固定版本/hash/许可和输出 manifest。
- [x] canonical 数据、运行时索引和用户输入职责分离。
- [x] quick CI、governance strict 和最终 review 完成。

# Task Package Checklists
## TP-01
- Verify: `bash scripts/data-supply-chain-gate.sh`
- Gate: canonical catalog、manifest、source lock 和供应链注册 hash 一致。
- [x] 新增 `locations/` canonical 数据产品与构建脚本。
- [x] 新增 location protocol 和供应链资产。
- [x] 删除旧坐标 CSV 与旧运行依赖。
- [x] 数据供应链门禁通过。

## TP-02
- Verify: `.venv/bin/python -m pytest -q tests/regression/test_location.py tests/regression/test_location_catalog.py`
- Gate: 稳定 ID、全量记录、IANA 时区、DST 和 runtime index 边界通过。
- [x] 稳定 ID、国内/海外/坐标解析完成。
- [x] IANA 时区、DST gap/fold 和三种 time basis 完成。
- [x] SQLite 索引使用文件锁和原子替换。
- [x] 全量 catalog 质量测试与边界测试通过。

## TP-03
- Verify: `.venv/bin/python -m pytest -q tests/regression/test_web_html.py tests/regression/test_api_contracts.py`
- Gate: Web/API 使用同源解析，原生无脚本路径和海外时间语义通过。
- [x] Web 只显示一个原生地区输入框，模糊候选选择后提交稳定地点 ID。
- [x] 地区搜索从第一个非空字符开始请求候选，不存在前端自行增加的两字门槛。
- [x] 地区输入过程不显示动态状态文字，未选候选仅在提交时触发浏览器原生校验。
- [x] 无 JavaScript 时唯一完整地区名称的服务端解析/生成路径保留。
- [x] 地点搜索/detail API 完成。
- [x] Bazi API 复用地点/时间标准化。

## TP-04
- Verify: `bash scripts/local-ci.sh --profile quick`、governance strict、task docs strict 与 review。
- Gate: 所有本地门禁通过且无未处理 BLOCK。
- [x] README/AGENTS/contracts/module context/ignore rules 同步。
- [x] clean production dependency smoke 通过。
- [x] 定向回归、lint/format、structure 与 diff check 通过。
- [x] quick CI、governance strict、task docs strict 和 review 通过。
