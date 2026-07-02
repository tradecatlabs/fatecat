# Execution Checklist

[x] TP-01.01 | P0 | 读取发布门禁脚本并确认 local-ci evidence 缺口 | Verify: `rg -n "local_ci_summary|summary.txt" scripts tests` | Gate: 缺口来自真实文件 | Parallelizable: No
[x] TP-02.01 | P0 | 修改 `scripts/local-ci.sh`，生成 `summary.json` 并保留 `summary.txt` | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0041` | Gate: summary JSON 字段完整 | Parallelizable: No
[x] TP-03.01 | P0 | 修改 `scripts/live-release-gate.py` 并补测试，校验 local CI summary 内容 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_live_release_gate.py` | Gate: pass/fail 分支覆盖 | Parallelizable: No
[x] TP-04.01 | P0 | 修改 `scripts/public-release-gate.sh`，默认 local-ci quick 路径传递 summary JSON | Verify: `FATECAT_PUBLIC_RELEASE_SMOKE_PORT=8019 bash scripts/public-release-gate.sh --output /tmp/fatecat-public-release-0041` | Gate: final live gate `passed=3,pending=7` | Parallelizable: No
[x] TP-05.01 | P0 | 运行验证并生成 closeout | Verify: `validate_task_docs.py --phase closeout` 与 `build_task_closeout.py` | Gate: 任务树有效且 evidence 回填 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
