# Execution Checklist

[x] TP-01 | P0 | 分析 0116 manual triage 剩余项 | Verify: jq manual path/excerpt sample | Gate: 先看证据再改 classifier | Parallelizable: No
[x] TP-02 | P0 | 扩展 closure profile 类别 | Verify: script diff and closure smoke | Gate: 不伪造 live | Parallelizable: No
[x] TP-03 | P0 | 运行 targeted 和 local-ci 验证 | Verify: pytest, smoke, ruff, secret scan, quick CI | Gate: manualTriage=1 and shipGate=blocked | Parallelizable: No
[x] TP-04 | P0 | 文档 closeout、提交、推送 | Verify: task docs validator and git status | Gate: clean pushed branch | Parallelizable: No
