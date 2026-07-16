# Audit Case Sampling Decision

- Source: governance/tasks/0163-classics-curation-policy
- Fixed Problem: 新增典籍整理专项测试最初只在独立命令中执行，未接入 `scripts/local-ci.sh --profile quick` 的固定测试清单；现已完成接线，并增加回归断言防止该门禁再次脱落。
- Decision: no-case
- Case ID: N/A
- Case Path: N/A
- Root Cause Class: new_test_not_wired_into_default_ci_gate
- Trigger Signals: 专项测试已通过；默认 CI 使用显式测试文件清单；新增测试文件未被默认门禁收集；完成声明依赖默认门禁证据。
- Evidence: `scripts/local-ci.sh` 已包含 `tests/regression/test_classics_dataset_clean.py`；`tests/regression/test_classics_dataset_clean.py` 包含 CI 接线断言；Quick CI 收集 526 项并通过该文件 12 项测试。
- No-Case Reason: 现有完成验证与测试质量案例已覆盖“专项验证未进入默认门禁”的通用模式；本轮通过仓库级回归断言加强机械防护，无需新增重复案例。

## Reusable Audit Questions

- 新增测试是否只在开发者手工命令中运行，而没有进入默认 CI 或 acceptance 门禁？
- 默认 CI 使用显式文件清单时，是否存在新测试文件静默遗漏风险？
- 完成声明引用的验证命令是否真实收集并执行了新增测试？

## Evidence Required

- 默认 CI 测试清单、CI 接线回归断言、实际 collected 数量和完整通过日志。
