# Acceptance Checklist

# Global Standards
- [x] canonical hash 不变
- [x] semantic replay error 为零
- [x] navigation 不进入 passage
- [x] passage 不跨 heading path
- [x] focused、真实 build、data gate、Quick CI 通过
- [x] deep review 无 BLOCK

# Task Package Checklists
## TP-01
- [x] v3 schema、policy structure 和 registry 完成
- Verify: JSON/schema/data gate。
- Gate: 目录范围越界或 source hash 漂移失败。

## TP-02
- [x] physical lines 无损重建为 semantic paragraphs
- [x] heading hierarchy 和 paragraphType 可追溯
- Verify: synthetic red/green + source replay。
- Gate: 不得改字、漏字或乱序。

## TP-03
- [x] navigation paragraphs 不进入 passages
- [x] heading path 变化强制 passage flush
- Verify: boundary tests + validator。
- Gate: violation count 必须为零。

## TP-04
- [x] 真实 14 本 v3 build/validate 通过
- [x] 确定性 hash、canonical hash 和质量指标通过
- Verify: two builds + data gate。
- Gate: ignored 派生正文不得入 Git。

## TP-05
- [x] deep review、Quick CI、task strict 完成
- [x] 本地提交边界干净
- Verify: review/CI/task/Git evidence。
- Gate: 无 BLOCK、无未跟踪运行产物。
