# Acceptance Checklist

# Global Standards
- [x] 14/14 policy 与 source hash 对账
- [x] canonical TXT hash 不变
- [x] 推广/envelope 不进入 passages
- [x] observed/reviewed 书目字段不混用
- [x] focused tests、data gate、Quick CI 通过
- [x] deep review 无 BLOCK

# Task Package Checklists
## TP-01
- [x] 污染、缺卷、截断、高 overlap 和元数据混写已定位
- Verify: 文件/行号、manifest 和一期 overlap 报告。
- Gate: 不把候选书目信息写成核实事实。

## TP-02
- [x] policy schema、14 项策略、registry 接线完成
- [x] 每项 source hash 和内容选择原因完整
- Verify: JSON parse、14/14 coverage、source hash 对账。
- Gate: policy 缺失、hash 漂移和行范围越界必须失败。

## TP-03
- [x] 清洗器消费 policy 并 fail closed
- [x] review queue 和 excluded line 证据生成
- Verify: focused synthetic fixture tests。
- Gate: 正文与元数据必须语义分离且可追溯。

## TP-04
- [x] 专项负向测试通过
- [x] 真实 14 本 build/validate-only 通过
- Verify: 真实 build、validate-only、noise zero-hit 和 data gate。
- Gate: canonical hash 不变且 lineage error 为零。

## TP-05
- [x] deep review 与原则门禁通过
- [x] Quick CI、task closeout 和 Git 边界通过
- Verify: review、Quick CI、task strict、git status/diff。
- Gate: 无 BLOCK、无 ignored 正文进入提交。
