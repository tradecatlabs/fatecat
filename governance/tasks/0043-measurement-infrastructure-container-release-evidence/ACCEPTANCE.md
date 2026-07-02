# Task-Level Acceptance
- `container-release-evidence.sh --output-json <path>` 生成 `kind=fatecat.container_release_evidence`、`status=passed`、`imageId=sha256:<64 hex>`、`smokeStatus=passed` 的 JSON。
- JSON 记录 image、tag、commit、repoDigests、registryDigestPresent、pushExecuted=false、limitations。
- live gate 只在 container evidence 内容可信时让 `evidence.container_digest=pass`。
- `--container-digest sha256:<64 hex>` 仍可作为真实 registry digest 输入。
- public-release 可通过显式 env 生成并传递 container evidence。

# Validation Plan
- `bash -n scripts/container-release-evidence.sh scripts/public-release-gate.sh scripts/live-release-gate.sh`
- `.venv/bin/python -m pytest -q tests/regression/test_container_release_evidence.py tests/regression/test_live_release_gate.py`
- `bash scripts/container-release-evidence.sh --image fatecat-delivery:0043 --port 8021 --output-json /tmp/fatecat-container-release-0043.json`
- `bash scripts/live-release-gate.sh --container-evidence-path /tmp/fatecat-container-release-0043.json --output-json /tmp/fatecat-live-release-gate-container-0043.json`
- `validate_task_docs.py --phase closeout`
- `validate_tasks_tree.py --phase auto`

# Review Gate
- 不接受只检查 container evidence 路径存在。
- 不接受 imageId 格式错误或 smokeStatus 非 passed。
- 不接受把本地 imageId 说成 registry RepoDigest。

# Runtime Verification Gate
- JSON 无 secret。
- Docker smoke 成功后才可 pass。
- `shipGate` 仍 blocked，除非外部 live 项和 clean git 都完成。

# Ship Readiness
本任务完成只代表本地 container release evidence baseline 可复核，不代表 GHCR/registry 发布已完成。

# Task Package Acceptance
## TP-01.01
- [x] Docker 和容器脚本已盘点。

## TP-02.01
- [ ] container evidence 生成器完成。

## TP-03.01
- [ ] live gate 内容校验完成。

## TP-04.01
- [ ] public-release 可选传递 container evidence。

## TP-05.01
- [ ] 真实容器 smoke、验证和 closeout 完成。

# Anti-Goals
- 不得 push registry
- 不得虚构证据
- 不得把本地 imageId 说成 registry digest
