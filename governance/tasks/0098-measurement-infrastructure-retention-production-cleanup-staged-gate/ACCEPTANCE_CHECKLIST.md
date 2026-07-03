# Acceptance Checklist

# Global Standards
- 每个 leaf 必须有 Verify 和 Gate。
- 不得跳过 gate；缺验证证据时不能 closeout。
- 本任务不得声明生产 retention cleanup live passed。
- Evidence 和 summary 不得包含真实 DSN、endpoint、token、secret、用户输入、报告正文、生产日志或真实删除结果。

# Task Package Checklists

## TP-01.01 复核 baseline
Verify: `sed`/`rg` 读取 0091/0083 contracts、scripts、tests。
Gate: 不重复实现 cleanup runtime。
- [x] 已读取 retention cleanup contract。
- [x] 已读取 security externalization contract/gate。
- [x] 已读取 retention cleanup 和 production security tests。

## TP-02.01 Staged Contract
Verify: `python3 -m json.tool contracts/fate/security/retention-production-cleanup-staged.json`。
Gate: scheduler、Postgres、SIEM 三类 evidence area 存在。
- [x] contract 已新增。
- [x] negative evidence cases 已新增。
- [x] pending external validation 已登记。

## TP-02.02 Gate Script
Verify: `bash scripts/retention-production-cleanup-gate.sh --output-json /tmp/fatecat-retention-production-cleanup-0098.json`。
Gate: 默认 shipGate=blocked，liveEvidenceStatus=外部连通验证待执行。
- [x] Python gate 已新增。
- [x] Shell wrapper 已新增。
- [x] default summary blocked/pending。

## TP-03.01 Wiring
Verify: regression wiring assertions。
Gate: policy、registry、local-ci、AGENTS/docs 均指向新 gate。
- [x] production-security-policy 已同步。
- [x] security registry 已同步。
- [x] local-ci quick 已同步。
- [x] AGENTS/API/roadmap 已同步。

## TP-03.02 Regression
Verify: focused pytest。
Gate: fake raw URL、缺 Postgres smoke、production_deleted marker 均被拒绝。
- [x] default blocked/pending 测试。
- [x] redacted staged evidence 测试。
- [x] negative cases 测试。
- [x] wiring 测试。

## TP-04.01 Final Validation
Verify: secret scan、quick local-ci、task closeout validator、diff check。
Gate: no placeholders, no secret findings, quick pass。
- [x] secret scan 通过。
- [x] quick local-ci 通过。
- [x] closeout validator 通过。
- [x] git diff check 通过。
