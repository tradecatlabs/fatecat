# Acceptance Checklist

# Global Standards
- [x] 没有输出真实 token。
- [x] 没有使用 placeholder/smoke token。
- [x] 已运行 `scripts/live-bot-smoke.sh` 取得真实失败证据。
- [x] task docs validation 通过。
- [x] tasks tree validation 通过。
- [x] git diff check 通过。

# Task Package Checklists
## TP-01.01
- [x] 脚本和门禁已复核。
- Verify: `scripts/live-bot-smoke.sh`、`scripts/live-release-gate.py`、`scripts/production-readiness.sh`。
- Gate: token 状态只记录 set/unset。

## TP-02.01
- [ ] 真实 Bot live smoke 通过。
- Verify: `FATE_BOT_TOKEN=<real-token> bash scripts/live-bot-smoke.sh`。
- Gate: 输出 `live bot smoke ok`。
- Blocker: 当前缺少真实 `FATE_BOT_TOKEN`。

## TP-03.01
- [x] blocked 状态、解除条件和校验证据已落盘。
- Verify: task docs validation、tasks tree validation、git diff check。
- Gate: 状态保持 Blocked，直到真实 Bot live 通过。
