# Acceptance Checklist

# Global Standards
- [x] 文件路径具体，命令可复现。
- [x] 测试结果来自真实执行输出。
- [x] 不输出 token、secret、password、DSN 或生产私密路径。
- [x] 文档说明本任务不覆盖外部 live release。

# Task Package Checklists

## TP-01.01
- [x] 确认现有缺口：local-ci 已有文本 summary，live gate 只检查 local-ci-summary 路径存在。
- Verify: `rg -n "local_ci_summary|summary.txt" scripts tests`。
- Gate: 缺口来自真实文件。

## TP-02.01
- [x] local-ci 成功/失败都写机器可读 summary JSON。
- Verify: `bash scripts/local-ci.sh --profile quick --output <dir>`。
- Gate: summary JSON 字段完整。

## TP-03.01
- [x] live gate 校验 profile/status/commit/artifact。
- Verify: `.venv/bin/python -m pytest -q tests/regression/test_live_release_gate.py`。
- Gate: pass/fail 分支覆盖。

## TP-04.01
- [x] public-release 默认路径传递 summary JSON，skip 路径不伪造。
- Verify: `rg -n "local-ci-summary" scripts/public-release-gate.sh`。
- Gate: skip-local-ci 不伪造 pass。

## TP-05.01
- [x] targeted tests、shell syntax、live gate smoke、task tree validation、closeout 全部完成。
- Verify: `validate_task_docs.py --phase closeout` 与 `build_task_closeout.py`。
- Gate: 任务树有效且 evidence 回填。
