# Acceptance Checklist

# Global Standards
- [x] 第三阶段方法、事实来源、边界和最小实现已记录。
- [x] quick CI、governance strict、GitHub Actions 与 HF 线上 audit 通过。

# Task Package Checklists
## TP-01
- [x] 独立能力页与稳定 query set 的必要性已基于现有差距确认。
- Verify: registry、公开 HTTP 与 GEO 固定方法。
- Gate: 不推断外部平台表现。

## TP-02
- [x] `/guides/bazi`、`/guides/ziwei` 与一致 JSON-LD 已实现。
- Verify: GEO regression。
- Gate: 只有 L4/Web 能力可访问。

## TP-03
- [x] GEO query set 与机械 gate 已实现。
- Verify: `scripts/geo-query-set-gate.py`。
- Gate: 题目、事实边界和来源完整，无伪造结果。

## TP-04
- [x] 发现链、文档、测试和 audit 已完成。
- Verify: links、sitemap、llms、audit。
- Gate: 无文档漂移或低质量内容扩散。

## TP-05
- [x] 完整审查、提交、部署与线上复测已完成。
- Verify: quick CI、GitHub Actions、HF runtime SHA 与 live audit。
- Gate: 本地可验证项全通过，外部指标保持 pending。
