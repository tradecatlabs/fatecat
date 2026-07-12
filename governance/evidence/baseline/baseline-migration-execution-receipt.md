---
id: BASELINE-MIGRATION-EXECUTION-RECEIPT-FATECAT
type: baseline-migration-execution-receipt
status: archived
owner: engineering
created: 2026-06-06
last_reviewed: 2026-07-13
review_cycle: P30D
---

# Baseline Migration Execution Receipt

> 历史快照：记录 canonical roots 迁移过程；当前运行路径已经是企业根。

## Executed

| Step | Evidence | Result |
| --- | --- | --- |
| 初始化 governance minimal package | `python3 /home/lenovo/.codex/skills/auto-governance/scripts/init_governance_package.py --project-root . --mode minimal` | created 37 governance files |
| 创建 canonical roots | `apps ai domains platform infra contracts catalog governance shared tools docs scripts tests` | PASS |
| 建立服务契约 | `domains/*/services/*/{README.md,AGENTS.md,service.yaml}` | PASS |
| 更新 runtime root 解析 | `scripts/common.sh` 支持 `FATECAT_RUNTIME_ROOT`、企业根和 `scripts/project` 兼容根 | PASS |
| 接入结构门禁 | `scripts/check-structure.sh` + `scripts/acceptance.sh` | PASS |
| 扩展 hygiene/privacy/export 覆盖 | `scripts/check-source-hygiene.sh`、`scripts/check-export-hygiene.sh`、`scripts/check-privacy-fixtures.sh`、`scripts/export-runtime.sh` | PASS |
| 设置仓库提交者身份 | `git config --local user.name tradecatlabs` + `git config --local user.email tradecatlabs@users.noreply.github.com` | PASS |
| 复制生产候选源码到 canonical service roots | `domains/fate-analysis/services/fate-core/src` + `domains/experience-delivery/services/fatecat-delivery/src` | PASS |
| 建立 root Python 工程元数据 | `pyproject.toml`、`requirements*.txt`、`.python-version`、`Makefile`、`.pre-commit-config.yaml` | PASS |
| 防止空企业根抢占 runtime root | `scripts/common.sh` 增加 `enterprise_runtime_ready`，root assets 未归位前继续使用兼容 runtime root | PASS |
| 完整兼容期验收 | `bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-enterprise` | PASS |
| 指定导出验收 | `bash scripts/export-runtime.sh --output-parent /tmp/fatecat-export --mode lite` + `bash scripts/check-export-hygiene.sh /tmp/fatecat-export/fatecat` | PASS |
| 复制资产到 canonical roots | `contracts/fate`、`domains/fate-analysis/data-products`、`infra/environments/local`、`infra/databases`、`infra/runtime/local-state`、`tools/reference-repos` | PASS；raw 私有资料、真实 `.env`、真实数据库和 `node_modules` 未迁入 |
| 切换服务路径常量 | `fate_core.support.paths`、delivery `_paths.py`、Node bridge、root script path helpers | PASS；health/delivery/export 均读取企业根 |
| 迁移行为回归测试入口 | `tests/regression` + `domains/*/services/*/tests` | PASS；root pytest 收集 112 tests |
| 隔离 Node vendor 构建产物 | `infra/runtime/local-state/vendor-build/` | PASS；`tools/reference-repos` 保持只读，不写入 `node_modules` |
| 企业根完整验收 | `bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-enterprise-root-2` | PASS |
| 独立导出验收 | `bash scripts/export-runtime.sh --output-parent /tmp/fatecat-export --mode lite` + `bash scripts/check-export-hygiene.sh /tmp/fatecat-export/fatecat` | PASS |

## Pending

- 清退 `scripts/project/` 兼容盒前，继续收敛历史文档、任务资产和剩余 fallback 引用。
