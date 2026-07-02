# Acceptance Checklist

# Global Standards
- [x] 文件路径具体，命令可复现。
- [x] 验证结果来自真实命令输出。
- [x] 不输出 token、secret、password、DSN 或私钥。
- [x] 文档说明 shipGate 仍 blocked。

# Task Package Checklists
## TP-01.01
- [x] HF Space/API live gate 已执行。
- Verify: `bash scripts/live-release-gate.sh --api-url https://tradecatlabs-fatecat.hf.space --hf-space-url https://tradecatlabs-fatecat.hf.space ...`。
- Gate: `passed=7,pending=3,failed=0`。

## TP-02.01
- [x] JSON evidence 可解析。
- Verify: `python3 -m json.tool /tmp/fatecat-live-release-gate-public-hf-0043.json`。
- Gate: production API 与 HF checks 为 pass。

## TP-03.01
- [x] closeout 完成。
- Verify: `validate_task_docs.py --phase closeout`。
- Gate: 任务树有效。
