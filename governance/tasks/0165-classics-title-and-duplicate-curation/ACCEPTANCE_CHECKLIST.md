# Acceptance Checklist

# Global Standards
- [x] canonical hash、正文 fingerprint 和权限边界不变
- [x] 每 document 最多一个 document_title
- [x] duplicate relationship 和 review summaries 可重算
- [x] focused、真实 build、data gate、Quick CI 通过
- [x] deep review 无 BLOCK

# Task Package Checklists
## TP-01
- [x] contract 与 red tests 完成
- Verify: focused red/green tests。
- Gate: 多 title 与无 relationship 问题可复现。

## TP-02
- [x] 重复书名改为 heading，title 唯一
- [x] 章节边界和 source replay 通过
- Verify: 合成标题边界测试与真实统计。
- Gate: 每 document title count <=1。

## TP-03
- [x] duplicate 三类关系完成
- [x] review/duplicate summary 完成
- Verify: 明细重算与 tamper 负例。
- Gate: relationship 和 summary 不得漂移。

## TP-04
- [x] 真实 14 本构建与 tamper 负例通过
- [x] 两次构建 hash 一致
- Verify: build/validate/data gate/hash。
- Gate: canonical、权限和语义不变量保持。

## TP-05
- [x] deep review、Quick CI、task strict 完成
- [x] 本地提交边界干净
- Verify: review/CI/task/Git evidence。
- Gate: 无 BLOCK、无运行产物入 Git。
