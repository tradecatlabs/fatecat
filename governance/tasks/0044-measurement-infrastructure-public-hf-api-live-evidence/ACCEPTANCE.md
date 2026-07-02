# Task-Level Acceptance
- Gate JSON 存在且可解析。
- `evidence.production_api_live=pass`。
- `evidence.hf_space_live=pass`。
- `summary.passed=7`、`summary.pending=3`、`summary.failed=0`。
- 剩余 pending 仅为 remote CI、Telegram Bot、clean git。

# Validation Plan
- `python3 -m json.tool /tmp/fatecat-live-release-gate-public-hf-0043.json`
- `python3` 摘要提取 gate checks。
- `validate_task_docs.py --phase closeout`
- `validate_tasks_tree.py --phase auto`

# Review Gate
- 不允许把 HF/API pass 扩大解释为全部 release ready。
- 不允许隐藏 Bot/CI/clean git pending。

# Runtime Verification Gate
- 外部 URL 只使用 `https://tradecatlabs-fatecat.hf.space`。
- 不输出 token 或用户数据。

# Ship Readiness
本任务完成后，live release gate 仍 blocked，原因是 remote CI、Telegram Bot 和 clean git 仍 pending。

# Task Package Acceptance
## TP-01.01
- [x] public HF/API live gate 已执行。

## TP-02.01
- [x] gate JSON 摘要已记录。

## TP-03.01
- [x] closeout 和任务树校验完成。

# Anti-Goals
- 不得伪造 Bot token、CI run 或 clean git
- 不得虚构证据
- 不得把当前结果写成 shipGate pass
