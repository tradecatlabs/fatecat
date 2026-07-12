# Acceptance Checklist

# Global Standards
- [x] 需求、方法来源、约束、外部证据边界和存在性判断已记录。
- [x] quick CI、governance strict、远端 CI 和线上 GEO audit 通过。

# Task Package Checklists

## TP-01
- [x] 改造前线上根、robots、sitemap 状态已采集。
- Verify: 公开 HTTP 证据与 GEO 方法文件。
- Gate: 基线事实可追溯且不推断平台内部排名。

## TP-02
- [x] root、robots、sitemap、canonical、JSON-LD 和 llms 已实现。
- Verify: `tests/regression/test_geo_discovery.py`。
- Gate: production/planned 分层准确，无视觉和计算回归。

## TP-03
- [x] GEO 审计脚本、回归与 public release 接线已实现。
- Verify: `python3 scripts/geo-audit.py --help` 与专项测试。
- Gate: 失败返回非零，外部指标不伪造。

## TP-04
- [x] 完整门禁、review、部署与线上 audit 已完成。
- Verify: quick CI、governance strict、GitHub Actions、HF live audit。
- Gate: 所有本地可验证项通过，外部平台指标保持 pending。
