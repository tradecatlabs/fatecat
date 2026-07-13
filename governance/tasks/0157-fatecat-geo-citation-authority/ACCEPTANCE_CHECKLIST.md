# Acceptance Checklist

# Global Standards
- [x] 方法、事实来源、外部指标边界和最小实现已记录。
- [x] quick CI、governance strict、GitHub Actions 与 HF 线上 audit 通过。

# Task Package Checklists
## TP-01
- [x] 页面、机器文档与 GitHub 元数据差距已采集。
- Verify: public HTTP、GitHub API 与 GEO 固定方法。
- Gate: 不推断平台内部收录和排名。

## TP-02
- [x] `/about`、可见 FAQ、实时能力表与一致 JSON-LD 已实现。
- Verify: `tests/regression/test_geo_discovery.py`。
- Gate: capability 状态与 schema/body 一致。

## TP-03
- [x] Web、sitemap、README、HF README、`llms.txt`、GEO audit 与 GitHub 元数据已接入。
- Verify: GEO audit、链接断言与 GitHub API 回读。
- Gate: 无关键词堆砌、未实现能力或文档漂移。

## TP-04
- [x] 完整审查、提交、部署与线上复测已完成。
- Verify: quick CI、GitHub Actions、HF runtime SHA 与 live audit。
- Gate: 所有本地可验证项通过，外部指标保持 pending。
