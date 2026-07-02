# Execution Checklist

[x] TP-01.01 | P0 | 盘点 Docker、container build/smoke、container workflow 和 live gate 缺口 | Verify: `docker version` 与脚本阅读 | Gate: Docker daemon 可用 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 `scripts/container-release-evidence.py` 与 `.sh` | Verify: `bash scripts/container-release-evidence.sh --output-json /tmp/fatecat-container-release-0043.json` | Gate: JSON 字段完整 | Parallelizable: No
[x] TP-03.01 | P0 | live gate 校验 container evidence JSON | Verify: `.venv/bin/python -m pytest -q tests/regression/test_container_release_evidence.py tests/regression/test_live_release_gate.py` | Gate: pass/fail 分支覆盖 | Parallelizable: No
[x] TP-04.01 | P0 | public-release 可选生成并传递 container evidence | Verify: `FATECAT_PUBLIC_RELEASE_WITH_CONTAINER=1 FATECAT_PUBLIC_RELEASE_CONTAINER_SKIP_BUILD=1 ... public-release-gate.sh` | Gate: final live gate container pass | Parallelizable: No
[x] TP-05.01 | P0 | 运行真实 container smoke 并生成 closeout | Verify: `validate_task_docs.py --phase closeout` 与 `build_task_closeout.py` | Gate: 任务树有效 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
