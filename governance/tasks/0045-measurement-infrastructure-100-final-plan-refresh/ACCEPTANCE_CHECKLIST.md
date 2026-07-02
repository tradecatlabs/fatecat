# Acceptance Checklist

# Global Standards
- [x] 不伪造外部连通验证。
- [x] 不提交、不推送、不触发远端 CI。
- [x] 不修改业务源码。
- [x] 所有新增任务项都有明确证据类型。

# Task Package Checklists
## TP-01.01
- [x] 官方资料调研完成。
- Verify: roadmap `0.1 外部基础设施同构调研`。
- Gate: 官方资料均为一手资料链接。

## TP-02.01
- [x] 当前差距复核完成。
- Verify: roadmap `0.3 当前最短剩余路径` 与 `0.4 当前不允许宣称完成的项`。
- Gate: `passed=7,pending=3` 口径未被扩大解释。

## TP-03.01
- [x] 100% 剩余路线刷新完成。
- Verify: roadmap 0046+ 任务序列。
- Gate: 每个后续任务都有必须证据。

## TP-04.01
- [x] closeout 校验完成。
- Verify: `validate_task_docs.py --phase closeout`、`validate_tasks_tree.py --phase auto`、`git diff --check`。
- Gate: 任务容器可复核。
