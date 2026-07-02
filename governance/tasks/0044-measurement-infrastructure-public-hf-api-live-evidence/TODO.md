# Execution Checklist

[x] TP-01.01 | P0 | 执行公开 HF/API live gate | Verify: `bash scripts/live-release-gate.sh --api-url https://tradecatlabs-fatecat.hf.space --hf-space-url https://tradecatlabs-fatecat.hf.space ...` | Gate: `passed=7,pending=3,failed=0` | Parallelizable: No
[x] TP-02.01 | P0 | 记录 gate JSON 摘要 | Verify: `python3 -m json.tool /tmp/fatecat-live-release-gate-public-hf-0043.json` | Gate: JSON 可解析 | Parallelizable: No
[x] TP-03.01 | P0 | 更新 roadmap、生成 closeout 并验证任务树 | Verify: `validate_tasks_tree.py --phase auto` | Gate: 任务树有效 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
