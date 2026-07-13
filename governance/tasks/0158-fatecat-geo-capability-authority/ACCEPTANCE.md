# Task-Level Acceptance
- `/guides/bazi` 与 `/guides/ziwei` 返回 200，其他 guide 返回 404。
- 两页初始 HTML 包含 canonical、答案前置摘要、输入、引擎、证据、风险、来源、FAQ 和更新时间。
- 可见 FAQ 与 JSON-LD 完全一致；动态字段与 capability registry 一致。
- query set 覆盖品牌验证、能力、接入、证据、隐私和风险问题，每项具有稳定 ID、来源 URL 与预期事实边界。
- `/about`、Web、sitemap、README、HF README 和 `llms.txt` 可发现两个 guide。
- GEO audit 覆盖新页面与题集，外部效果指标保持待验证。

# Validation Plan
- `.venv/bin/python -m pytest tests/regression/test_geo_discovery.py tests/regression/test_web_html.py -q`
- `python3 scripts/geo-query-set-gate.py`
- `bash scripts/local-ci.sh --profile quick`
- `python3 scripts/geo-audit.py --base-url <local-or-live>`
- governance strict、task closeout、`git diff --check`。

# Review Gate
- 阻断：虚假能力、schema/body 漂移、planned guide 可访问、引入样式、敏感信息、Prompt 无来源或外部指标伪证。

# Runtime Verification Gate
- HF Space 运行 SHA 必须是本次部署提交。
- 两个 guide、sitemap、`llms.txt` 与线上 GEO audit 必须通过。

# Ship Readiness
- 本地门禁、GitHub Actions、HF runtime 和线上 audit 有真实证据后完成。

# Verified Evidence
- 本地独占 Quick CI：463 passed；测试后 vendor health 通过。
- GitHub Actions：`https://github.com/tradecatlabs/fatecat/actions/runs/29267472907`，精确验证实现提交 `9531d142d86589528c5779b9e0f067a8b3d00c4f`。
- HF Space：提交 `64db1a27b151c35991c6b102d22570f4a5ef1c8e`，运行状态 `RUNNING`。
- 线上 GEO audit：70/70，100%；`llms.txt` 与 query set 分别和仓库源文件哈希一致。
- 非准入能力 `almanac`、`meihua`、`liuyao` 和未知 guide 均返回 404。

# Task Package Acceptance
- TP-01：差距和最小充分方案可追溯。
- TP-02：两个旗舰能力页通过回归。
- TP-03：query set 与 gate 通过。
- TP-04：发现链、文档和审计完成。
- TP-05：部署和线上复测完成。

# Anti-Goals
- 不修改测算算法或报告结构。
- 不发布 planned capability 内容页或低质量批量内容。
- 不把技术门禁解释为 AI 平台索引、引用或推荐结果。
