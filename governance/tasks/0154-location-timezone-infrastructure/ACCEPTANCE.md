# Task-Level Acceptance
- 全球地点目录有固定来源 URL/version/hash、许可、输出 hash、统计和精度边界。
- 国内/海外/坐标输入均产生稳定地点事实；重名和模糊输入不静默选择。
- WGS84、IANA 时区、时间口径和 DST fold 可追溯并进入机器输入摘要。
- Web 只显示一个原生地区输入框，支持键盘、移动端候选、稳定 ID 绑定和无 JavaScript 降级，不引入 CSS/前端框架。
- Bazi API 与 Web 使用同一地点/时间规范化，时区冲突和 DST 异常显式失败。
- 旧坐标表、旧解析依赖和运行时缓存误提交入口已退役。

# Validation Plan
- `.venv/bin/python -m pytest -q tests/regression/test_location_catalog.py tests/regression/test_location.py tests/regression/test_web_html.py tests/regression/test_api_contracts.py`
- `bash scripts/data-supply-chain-gate.sh`
- clean production venv `pip install -c requirements.lock.txt -r requirements.txt` + `pip check` + timezone smoke
- `.venv/bin/python -m ruff check .` 与 `.venv/bin/python -m ruff format --check .`
- `bash scripts/check-structure.sh`
- `bash scripts/local-ci.sh --profile quick`
- governance strict、task docs strict 与 `git diff --check`

# Review Gate
- correctness：地点、时区、DST、坐标和 API/Web 语义正确。
- reliability：catalog hash 校验、原子索引替换、并发文件锁和显式错误路径。
- performance：168k 记录只在首次构建扫描；查询使用 SQLite 索引，无请求期网络调用。
- security/privacy：日志和 metrics 不保存用户地点/坐标；数据产品不含用户输入。
- architecture/contract：canonical 与 runtime 分离，所有交付面共享协议和服务端核心。
- document drift/repo hygiene：README/AGENTS/contracts/module context/ignore rules 与实现一致。

# Runtime Verification Gate
- 定向回归、数据供应链、clean-env 和 quick CI 全部通过。
- 运行时 SQLite 被 `.gitignore` 命中且可删除重建。
- `/ready` 验证地点目录可加载和记录数一致。

# Ship Readiness
- 本地实现与门禁完成后可进入版本控制交付。
- commit/push/HF 部署未在本轮授权范围内，不作为本地实现完成条件。

# Task Package Acceptance
- TP-01：数据产品、source lock、manifest、供应链和 location contract 完成。
- TP-02：resolver、runtime index、时区和时间标准化完成。
- TP-03：Web/API 接入、国内模糊搜索候选和无脚本路径完成。
- TP-04：测试、文档、依赖、治理和审查全部闭环。

# Anti-Goals
- 不复制参考站私有数据、样式或固定 GMT 表。
- 不引入在线地理编码作为生产必需依赖。
- 不保留旧 CSV fallback 或双轨解析器。
- 不把城市中心点宣称为精确出生地址。
