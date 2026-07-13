# Task-Level Acceptance
- `/about` 返回 200、初始 HTML 含 canonical、答案前置摘要、能力表、来源、FAQ 和风险边界。
- FAQ 可见正文与 JSON-LD 完全一致。
- sitemap、Web、README、HF README 和 `llms.txt` 均能发现 `/about`。
- GitHub description、homepage、topics 回读符合真实项目能力。
- GEO audit 对新页面执行机械检查，外部指标继续标记待验证。

# Validation Plan
- `.venv/bin/python -m pytest tests/regression/test_geo_discovery.py tests/regression/test_web_html.py -q`
- `bash scripts/local-ci.sh --profile quick`
- `python3 scripts/geo-audit.py --base-url <local-or-live>`
- governance strict、task closeout、`git diff --check`。

# Review Gate
- 阻断：虚假能力、schema/body 漂移、planned 被写成可执行、引入视觉样式、敏感数据或外部指标伪证。

# Runtime Verification Gate
- HF Space 运行 SHA 必须是本次部署提交。
- 线上 `/about` 与 sitemap 必须通过 GEO audit。

# Ship Readiness
- 本地门禁、GitHub Actions、HF runtime 与线上 audit 全部有真实证据后完成。

# Task Package Acceptance
- TP-01：差距基线可追溯。
- TP-02：公开权威页和实体结构通过回归。
- TP-03：发现链与 GitHub 元数据完成。
- TP-04：部署和线上复测完成。

# Anti-Goals
- 不修改测算算法或报告结构。
- 不制造关键词页、低质量批量内容、虚假案例、评价或引用数据。
- 不把技术 GEO 分数解释为 AI 平台收录或推荐结果。
