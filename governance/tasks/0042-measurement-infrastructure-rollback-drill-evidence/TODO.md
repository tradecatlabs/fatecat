# Execution Checklist

[x] TP-01.01 | P0 | 盘点 rollback gate 与现有脚本/文档 | Verify: `rg -n "rollback/回滚"` | Gate: 缺口来自真实文件 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 `scripts/rollback-drill.py` 与 `.sh` | Verify: `bash scripts/rollback-drill.sh --output-json /tmp/fatecat-rollback-drill-0042.json` | Gate: JSON 字段完整 | Parallelizable: No
[x] TP-03.01 | P0 | live gate 校验 rollback drill JSON | Verify: `.venv/bin/python -m pytest -q tests/regression/test_live_release_gate.py tests/regression/test_rollback_drill.py` | Gate: pass/fail 分支覆盖 | Parallelizable: No
[x] TP-04.01 | P0 | public-release 默认路径生成并传递 rollback evidence | Verify: `FATECAT_PUBLIC_RELEASE_SMOKE_PORT=8020 bash scripts/public-release-gate.sh --output /tmp/fatecat-public-release-0042` | Gate: final live gate rollback pass | Parallelizable: No
[x] TP-05.01 | P0 | 运行验证并生成 closeout | Verify: `validate_task_docs.py --phase closeout` 与 `build_task_closeout.py` | Gate: 任务树有效 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
