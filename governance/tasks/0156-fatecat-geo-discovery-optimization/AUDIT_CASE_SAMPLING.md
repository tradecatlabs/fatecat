# Audit Case Sampling Decision

- Source: governance/tasks/0156-fatecat-geo-discovery-optimization
- Fixed Problem: FateCat 公开根、robots 和 sitemap 缺失，Web 和 llms 又缺少统一实体、能力成熟度和引用事实结构。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: first-time-public-discovery-capability-gap
- Trigger Signals: 根入口 404；robots/sitemap 404；无 canonical/JSON-LD；机器文档无法区分 Web、production 和 planned。
- Evidence: `public_discovery.py`；`llms.txt`；`tests/regression/test_geo_discovery.py`；`scripts/geo-audit.py`。
- No-Case Reason: 本轮是首次建立机器发现能力，不是重复缺陷或 debug 根因；专项回归与公开发布门禁已直接承担防回归。

## Reusable Audit Questions
- 公开根、robots、sitemap、canonical 与机器事实文档是否形成闭环？
- production 与 planned 能力是否在所有机器入口保持一致？
- 不可从仓库验证的平台指标是否被诚实标记为外部待验证？

## Evidence Required
- 本地结构回归、quick CI、远端 CI 与部署后真实 HTTP GEO audit。
