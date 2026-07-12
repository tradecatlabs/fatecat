# Task-Level Acceptance
- `/` 308 到 `/web`。
- `/robots.txt` 与 `/sitemap.xml` 返回正确类型且可解析。
- `/web` 包含 canonical、description、author、date、llms/sitemap link 和合法 JSON-LD。
- `llms.txt` 明确身份、production/planned、来源、问答、引用、隐私和风险。
- `geo-audit.py` 对真实 HTTP 输出可复核 JSON，失败时非零退出。
- quick CI 包含 GEO 回归；public release 在有 `--api-url` 时执行 live GEO audit。
- GitHub 与 HF 文档暴露机器入口。

# Validation Plan
- `python3 -m pytest -q tests/regression/test_geo_discovery.py tests/regression/test_web_html.py`
- `python3 -m py_compile .../public_discovery.py scripts/geo-audit.py`
- `bash scripts/local-ci.sh --profile quick`
- `python3 scripts/geo-audit.py --base-url https://tradecatlabs-fatecat.hf.space`
- `python3 governance/tools/validate_governance_package.py --strict`

# Review Gate
- 禁止不受来源支持的产品、客户、效果、排名或引用声明。
- 禁止 Schema.org 与 llms 把 planned 能力写成 production。
- 禁止新增视觉样式或改变报告计算。

# Runtime Verification Gate
- 本地 TestClient 验证结构；部署后真实 HTTP 审计必须 100 分。
- 外部 AI 引用、索引、流量与转化保持外部连通验证待执行。

# Ship Readiness
- 本地门禁、远端 CI、HF 部署和线上审计全部通过后可 ship。

# Task Package Acceptance

## TP-01
- 改造前公开 HTTP 状态和 GEO 方法来源可追溯。

## TP-02
- 所有发现端点和实体事实只引用已验证能力。

## TP-03
- 本地结构测试与线上 HTTP 审计使用同一契约。

## TP-04
- 文档、GitHub、HF、CI 与线上证据描述同一版本。

# Anti-Goals
- 不批量制造内容，不使用隐藏文本，不操纵模型，不伪造效果。
