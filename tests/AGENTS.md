# AGENTS.md - tests

## 目录用途

`tests/` 是企业仓库级测试入口，承载跨服务、契约、结构门禁和行为回归。旧兼容测试已复制到 `tests/regression/`。

## 目录结构

```text
tests/
├── AGENTS.md
└── regression/
    ├── conftest.py
    ├── fate_core/
	    ├── test_bazi_golden_coverage_matrix.py
	    ├── test_calendar_oracle_contract.py
	    ├── test_catalog_contracts.py
	    ├── test_mingli_bench_aggregate_gate.py
	    ├── test_mingli_bench_gate.py
	    ├── test_developer_portal_gate.py
	    ├── test_sandbox_access_gateway_gate.py
	    ├── test_operability_docs.py
	    ├── test_report_job_replayable_recovery_smoke.py
	    ├── test_report_job_restart_recovery_smoke.py
	    ├── test_webhook_outbox_smoke.py
	    ├── test_webhook_outbox_redelivery_smoke.py
	    ├── test_webhook_config_vault_smoke.py
	    ├── test_webhook_outbox_lease_smoke.py
	    ├── test_multi_replica_runtime_evidence_assembler.py
	    ├── test_multi_replica_runtime_gate.py
	    ├── test_otel_backend_slo_gate.py
	    ├── test_provider_drift_scanner.py
	    └── test_*.py
```

## 职责边界

- `regression/`：原项目行为回归测试，路径已切到 canonical roots。
- `regression/test_bazi_golden_coverage_matrix.py`：300+ 八字匿名结构 golden 矩阵合同、requiredTags 代表集回放，以及 `FATECAT_RUN_FULL_GOLDEN_MATRIX=1` 全量 release gate；全量可用 `FATECAT_GOLDEN_SHARD_TOTAL` / `FATECAT_GOLDEN_SHARD_INDEX` 分片。
- `regression/test_calendar_oracle_contract.py`：历法/四柱 oracle 对照测试；只服务开发门禁，不允许 oracle 库进入生产源码路径。
- `regression/test_catalog_contracts.py`：组件 catalog canonical root 与 compatibility box 退役防回潮测试。
- `regression/test_mingli_bench_aggregate_gate.py`：MingLi-Bench 离线聚合门禁合同；验证 summary 只含 stats、license/usage 和 baseline 聚合结果，不泄露题目、出生信息、标准答案或逐题结果。
- `regression/test_mingli_bench_gate.py`：MingLi-Bench 离线 predictions evaluator smoke 与 FateCat scored baseline 产物合同；准确率只作为评测输出，不宣称模型已专业。
- `regression/test_developer_portal_gate.py`：developer portal / SDK release baseline 合同；验证 SDK local smoke、fixed sandbox snapshot hash、外部未上线边界和隐私片段防护。
- `regression/test_sandbox_access_gateway_gate.py`：sandbox access gateway 合同；验证本地 gateway gate、scope enforcement、rate limit、audit 脱敏和公网 token issuer 未上线边界。
- `regression/test_operability_docs.py`：公共服务 SLO、指标、告警和 runbook 的文档合同测试。
- `regression/test_report_job_restart_recovery_smoke.py`：report job SQLite manager 重建本地 smoke 合同；验证 restart-safe failure、`job.recovered_failed`、幂等键保留和 summary 脱敏边界。
- `regression/test_report_job_replayable_recovery_smoke.py`：report job SQLite 可重建执行 smoke 合同；验证带 `task_payload` 和 factory 的 active 任务重建后重新入队成功，无 payload 任务仍安全失败。
- `regression/test_webhook_outbox_smoke.py`：report job webhook SQLite outbox 本地 smoke 合同；验证 success/failure outbox record、manager 重建可读和 summary 脱敏边界。
- `regression/test_webhook_outbox_redelivery_smoke.py`：report job webhook SQLite outbox 自动重投 smoke 合同；验证 failed outbox record 在 manager 重建后通过运行时 resolver 自动重投成功，resolver 缺失时跳过且 summary 脱敏。
- `regression/test_webhook_config_vault_smoke.py`：report job webhook encrypted config vault smoke 合同；验证 callback URL/secret Fernet 加密落库、manager 重建无 resolver 重投、成功后删除 config、key rotation 和 summary 脱敏。
- `regression/test_webhook_outbox_lease_smoke.py`：report job webhook SQLite outbox lease smoke 合同；验证 failed outbox 本地 claim/release 互斥、错误 owner release 无效、manager 重建后只重投一次和 summary 脱敏。
- `regression/test_multi_replica_runtime_evidence_assembler.py`：长期多副本 runtime evidence 装配器合同；验证 pending evidence、脱敏 live fixture、缺 ack、敏感 proof ref、raw URL 和 exactly-once overclaim 被拒绝。
- `regression/test_multi_replica_runtime_gate.py`：长期多副本 runtime evidence gate 合同；验证 evidence contract、反伪造负例、脱敏 live evidence schema、runtime registry 接线和 summary 隐私边界。
- `regression/test_otel_backend_slo_gate.py`：OTel backend/SLO staged evidence gate 合同；验证 pending summary、脱敏 live fixture、placeholder/raw URL/缺字段负例和 summary 隐私边界。
- `regression/test_provider_drift_scanner.py`：production provider drift scanner 合同；验证 provider lifecycle/dependency smoke、provider.validate/provider.calculate span、source/license/vendor refs 和 drift report 隐私边界。
- 服务私有测试可以留在服务根，但必须被根 `scripts/acceptance.sh` 覆盖。
- 不在这里写入运行态、golden 原始资料或外部 vendor 源码。

## 依赖方向

- `tests -> domains + contracts + catalog + governance`
