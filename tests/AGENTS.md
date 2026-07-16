# AGENTS.md - tests

## 目录用途

`tests/` 是企业仓库级测试入口，承载跨服务、契约、结构门禁和行为回归。旧兼容测试已复制到 `tests/regression/`。

## 目录结构

```text
tests/
├── AGENTS.md
└── regression/
    ├── conftest.py
    ├── test_classics_dataset_clean.py
    ├── test_suanzhun_corpus_crawl.py
    ├── fate_core/
	    ├── test_bazi_golden_coverage_matrix.py
	    ├── test_calendar_oracle_contract.py
	    ├── test_catalog_contracts.py
	    ├── test_mingli_bench_aggregate_gate.py
	    ├── test_core_quality_corpus_gate.py
	    ├── test_core_quality_human_review_bundle_template.py
	    ├── test_core_quality_human_review_gate.py
	    ├── test_mingli_bench_gate.py
	    ├── test_multi_surface_semantic_diff.py
	    ├── test_capability_cli_smoke.py
	    ├── test_developer_portal_gate.py
	    ├── test_sandbox_access_gateway_gate.py
	    ├── test_current_audit_bundle.py
	    ├── test_external_validation_closure_evidence_summary.py
	    ├── test_external_validation_closure_gate.py
	    ├── test_external_validation_closure_work_queue.py
	    ├── test_external_validation_issue_export.py
	    ├── test_external_validation_tracker_import_package.py
	    ├── test_external_validation_live_proof_gate.py
	    ├── test_external_validation_operator_execution_packet.py
	    ├── test_external_validation_closure_trend_dashboard.py
	    ├── test_external_evidence_submission_readiness_audit.py
	    ├── test_production_live_operator_execution_packet.py
	    ├── test_independent_audit_result_gate.py
	    ├── test_measurement_infrastructure_certification.py
	    ├── test_third_party_audit_rehearsal.py
	    ├── test_current_release_proof.py
	    ├── test_operability_docs.py
	    ├── test_report_job_replayable_recovery_smoke.py
	    ├── test_report_job_restart_recovery_smoke.py
	    ├── test_retention_cleanup.py
	    ├── test_webhook_outbox_smoke.py
	    ├── test_webhook_outbox_redelivery_smoke.py
	    ├── test_webhook_config_vault_smoke.py
	    ├── test_webhook_outbox_lease_smoke.py
	    ├── test_multi_replica_runtime_evidence_assembler.py
	    ├── test_multi_replica_runtime_gate.py
	    ├── test_otel_backend_slo_gate.py
	    ├── test_provider_drift_scanner.py
	    ├── test_provider_drift_trend_gate.py
	    ├── test_evidence_coverage_trend_gate.py
	    └── test_*.py
```

## 职责边界

- `regression/`：原项目行为回归测试，路径已切到 canonical roots。
- `regression/test_classics_dataset_clean.py`：典籍内部派生数据集离线合同；覆盖确定性构建、无损规范化、来源追溯、版权边界、重复只标记不删除、非法编码/控制字符拒绝、路径隔离和输出篡改检测，不读取私有 raw 或公网资源。
- `regression/test_suanzhun_corpus_crawl.py`：算准网抓取器离线合同；覆盖 URL 规范化、当前/旧详情续页、隐藏中间页推导、物理页到逻辑文章聚合、v1 原位迁移、元数据隔离、缺页与共因失明门禁、正文去噪和 Windows 安全路径，不访问公网。
- `regression/test_bazi_golden_coverage_matrix.py`：300+ 八字匿名结构 golden 矩阵合同、requiredTags 代表集回放，以及 `FATECAT_RUN_FULL_GOLDEN_MATRIX=1` 全量 release gate；全量可用 `FATECAT_GOLDEN_SHARD_TOTAL` / `FATECAT_GOLDEN_SHARD_INDEX` 分片。
- `regression/test_calendar_oracle_contract.py`：历法/四柱 oracle 对照测试；只服务开发门禁，不允许 oracle 库进入生产源码路径。
- `regression/test_catalog_contracts.py`：组件 catalog canonical root 与 compatibility box 退役防回潮测试。
- `regression/test_mingli_bench_aggregate_gate.py`：MingLi-Bench 离线聚合门禁合同；验证 summary 只含 stats、license/usage 和 baseline 聚合结果，不泄露题目、出生信息、标准答案或逐题结果。
- `regression/test_core_quality_corpus_gate.py`：八字/紫微 core quality corpus 合同；验证 evaluation manifest、紫微匿名样本数量、覆盖标签、summary-only report diff 策略、registry 接线和隐私边界。
- `regression/test_core_quality_human_review_bundle_template.py`：八字/紫微 core quality 人审 evidence bundle 模板合同；验证模板契约、rubric dimension skeleton、hash/no-leak/operator checklist、CLI 输出、local-ci/registry/AGENTS 接线，并证明模板直接喂给 intake gate 会被拒绝。
- `regression/test_core_quality_human_review_gate.py`：八字/紫微外部专家评审 intake 合同；验证默认 pending、脱敏专家评审/benchmark/no-leak bundle accepted、raw URL/敏感片段/commit mismatch/缺 rubric dimension 拒绝，以及 local-ci、registry、certification、AGENTS 和 roadmap 接线。
- `regression/test_public_report_visibility.py`：公开 Markdown 标题、表头和元数据字段白名单，以及机器证据只保留在结构化结果的隔离门禁。
- `regression/test_public_client_distribution.py`：公开 Python HTTP 客户端与受限服务端运行时的许可证边界、归档 allowlist 和零服务端 import 门禁。
- `regression/test_mingli_bench_gate.py`：MingLi-Bench 离线 predictions evaluator smoke 与 FateCat scored baseline 产物合同；准确率只作为评测输出，不宣称模型已专业。
- `regression/test_multi_surface_semantic_diff.py`：多交付面语义一致性 gate 合同；验证 API/Web/Bot dry-run normalized hash 同源、CLI capability smoke、Skill 命令链证据、证据不保存报告正文、registry/local-ci/AGENTS wiring 和 capability 引擎接线。
- `regression/test_capability_cli_smoke.py`：capability CLI 交付面合同；验证根级 CLI wrapper、production capability smoke、planned capability 拒绝、delivery registry 和 local-ci/AGENTS 接线。
- `regression/test_developer_portal_gate.py`：developer portal / SDK release baseline 合同；验证 SDK local smoke、fixed sandbox snapshot hash、外部未上线边界和隐私片段防护。
- `regression/test_sandbox_access_gateway_gate.py`：sandbox access gateway 合同；验证本地 gateway gate、scope enforcement、rate limit、audit 脱敏和公网 token issuer 未上线边界。
- `regression/test_current_audit_bundle.py`：current audit bundle 合同；验证当前 commit 审计包能聚合 audit handoff、dry-run、release artifacts、rollback drill、current release proof、evidence index、risk register 和 pending external validations，且 required 模式不接受 local-contract 伪证。
- `regression/test_external_validation_closure_gate.py`：external validation closure gate 合同；验证 pending external validations 被转换为 owner、凭证依赖、required evidence、复核命令和关闭条件，不输出敏感赋值形态，也不把关闭计划伪装成 live 通过。
- `regression/test_external_validation_closure_work_queue.py`：external validation closure work queue 合同；验证 closure plan 按 owner/category 聚合成 pending work item，补齐 assignee/proofRef/stale/close 字段，summary 不输出 pending excerpt 或敏感赋值形态。
- `regression/test_external_validation_proof_ref_gate.py`：external validation proof-ref gate 合同；验证 proof-ref schema、脱敏 evidence bundle、raw URL/placeholder 拒绝、local-ci 接线，以及 schema accepted 仍不等于 production live passed。
- `regression/test_external_validation_category_runbooks.py`：external validation category runbook 合同；验证 22 个 category 均有 operator runbook、未知 category 拒绝、raw URL/敏感片段防护、local-ci/certification 接线，以及 runbook ready 仍不等于 production live passed。
- `regression/test_external_validation_closure_evidence_summary.py`：external validation closure evidence summary 合同；验证 22 类外部验证的 domain/category/owner/work item 聚合、operator packet 绑定、proof-ref/live pending 阻断、敏感片段拒绝和 local-ci/certification 接线。
- `regression/test_external_validation_issue_export.py`：external validation issue export 合同；验证 22 类 pending work item 可转成脱敏 issue 模板、CLI 输出 JSON/Markdown、敏感赋值拒绝和 local-ci/AGENTS/roadmap 接线，不创建真实 issue。
- `regression/test_external_validation_tracker_import_package.py`：external validation tracker import package 合同；验证 issue export 可转成独立 issue body files、manifest 和 tracker CLI command text，敏感赋值/raw URL 拒绝和 local-ci/AGENTS/roadmap 接线，不创建真实 issue、不执行 `gh`。
- `regression/test_external_validation_tracker_issue_evidence_template.py`：external validation tracker issue evidence template 合同；验证 tracker import package 可转成可填写 evidence bundle skeleton，填入 sanitized issue ref/hash 后可被 issue evidence gate 接受，并保持 template 本身不声明 issue created 或 live passed。
- `regression/test_external_validation_tracker_issue_evidence_gate.py`：external validation tracker issue evidence gate 合同；验证 operator 脱敏 issue evidence bundle 与 tracker import package 的 workItemId、issueTemplateId、body hash 和 sanitized issue ref 绑定，raw URL/敏感占位拒绝，并保持 shipGate blocked。
- `regression/test_external_validation_live_proof_gate.py`：external validation live proof gate 合同；验证 live evidence bundle 与 work queue、proof-ref gate、category runbook 和 current commit 绑定，拒绝未接受 proof-ref、raw URL、placeholder 和敏感片段；live proof 接受后仍保留审计/certification 阻断。
- `regression/test_external_validation_operator_execution_packet.py`：external validation operator execution packet 合同；验证 22 类外部验证 operator packet、domain 分组、proof-ref 模板、CLI 输出、敏感赋值拒绝和 local-ci/AGENTS/roadmap 接线，不执行真实外部请求。
- `regression/test_production_live_operator_execution_packet.py`：production live operator execution packet 合同；验证执行包 contract、脱敏 operator steps、proof-ref bundle 模板、CLI 输出、敏感赋值拒绝和 local-ci/AGENTS/roadmap 接线，不执行真实外部请求。
- `regression/test_production_live_delivery_evidence_bundle.py`：production live delivery evidence bundle 合同；验证 API/HF/Bot/webhook/parity 脱敏 summary 可转换为 live proof bundle，默认无真实 summary 只 pending，敏感输入拒绝，输出不复制 raw URL，并可被 external validation live proof gate 接受。
- `regression/test_external_validation_closure_trend_dashboard.py`：external validation closure trend dashboard 合同；验证 closure plan/work queue/proof-ref/category runbook/live proof gate 聚合、owner/category/status 趋势、stale alert、缺 runbook 拒绝、local-ci/certification 接线，以及 alert 不等于 live evidence closure。
- `regression/test_external_evidence_submission_readiness_audit.py`：external evidence submission readiness audit 合同；验证 proof-ref、live proof、operator packet、core quality human review、third-party audit rehearsal 和 certification 聚合为提交准备度矩阵，默认阻断不被伪造通过，合成全绿可通过，CLI/Markdown 输出和敏感值/raw URL 拒绝。
- `regression/test_measurement_infrastructure_certification.py`：100% 测算基础设施 certification aggregator dry-run 合同；验证 local-ci 产物聚合、external validation tracker import/template/gate 审计桥接、blocked dry-run、require-certified 拒绝、缺证据失败和合成全绿通过。
- `regression/test_independent_audit_result_gate.py`：独立第三方审计结果 intake gate 合同；验证默认 pending、脱敏 signed result bundle accepted、审计 rejected、commit mismatch、raw URL/敏感片段/占位证据拒绝和 CLI 输出。
- `regression/test_third_party_audit_rehearsal.py`：第三方审计预演包合同；验证 current audit bundle、audit dry-run、release proof、certification、closure evidence summary、tracker import package、tracker issue evidence template、tracker issue evidence gate 和 independent audit result gate 能聚合成审计 checklist，且外部 pending/tracker issue evidence/独立审计 gate 未通过时 rehearsalGate 仍 blocked。
- `regression/test_current_release_proof.py`：current release proof 合同；验证当前 commit 发布证据聚合 gate 的 local-contract/required 模式、ReleaseGate 登记和敏感值防护。
- `regression/test_operability_docs.py`：公共服务 SLO、指标、告警和 runbook 的文档合同测试。
- `regression/test_report_job_restart_recovery_smoke.py`：report job SQLite manager 重建本地 smoke 合同；验证 restart-safe failure、`job.recovered_failed`、幂等键保留和 summary 脱敏边界。
- `regression/test_report_job_replayable_recovery_smoke.py`：report job SQLite 可重建执行 smoke 合同；验证带 `task_payload` 和 factory 的 active 任务重建后重新入队成功，无 payload 任务仍安全失败。
- `regression/test_retention_cleanup.py`：retention cleanup 本地合同测试；验证 SQLite records/report jobs dry-run/execute 合成 smoke、CLI 缺库安全跳过、contract/registry/local-ci/AGENTS 接线和 summary 脱敏边界。
- `regression/test_retention_production_cleanup_gate.py`：retention production cleanup staged gate 合同；验证 scheduler、Postgres cleanup、SIEM/log retention evidence contract、blocked/pending 默认状态、脱敏 live fixture、反伪造负例和 local-ci/AGENTS 接线。
- `regression/test_event_contract_gate.py`：异步事件 contract gate 测试；验证 CloudEvents/AsyncAPI registry、producer/consumer compatibility、replay/DLQ 策略、脱敏 replay 示例和缺 required consumer / producer path 的负向拒绝。
- `regression/test_webhook_outbox_smoke.py`：report job webhook SQLite outbox 本地 smoke 合同；验证 success/failure outbox record、manager 重建可读和 summary 脱敏边界。
- `regression/test_webhook_outbox_redelivery_smoke.py`：report job webhook SQLite outbox 自动重投 smoke 合同；验证 failed outbox record 在 manager 重建后通过运行时 resolver 自动重投成功，resolver 缺失时跳过且 summary 脱敏。
- `regression/test_webhook_config_vault_smoke.py`：report job webhook encrypted config vault smoke 合同；验证 callback URL/secret Fernet 加密落库、manager 重建无 resolver 重投、成功后删除 config、key rotation 和 summary 脱敏。
- `regression/test_webhook_outbox_lease_smoke.py`：report job webhook SQLite outbox lease smoke 合同；验证 failed outbox 本地 claim/release 互斥、错误 owner release 无效、manager 重建后只重投一次和 summary 脱敏。
- `regression/test_multi_replica_runtime_evidence_assembler.py`：长期多副本 runtime evidence 装配器合同；验证 pending evidence、脱敏 live fixture、缺 ack、敏感 proof ref、raw URL 和 exactly-once overclaim 被拒绝。
- `regression/test_multi_replica_runtime_gate.py`：长期多副本 runtime evidence gate 合同；验证 evidence contract、反伪造负例、脱敏 live evidence schema、runtime registry 接线和 summary 隐私边界。
- `regression/test_otel_backend_slo_gate.py`：OTel backend/SLO staged evidence gate 合同；验证 pending summary、脱敏 live fixture、placeholder/raw URL/缺字段负例和 summary 隐私边界。
- `regression/test_provider_drift_scanner.py`：production provider drift scanner 合同；验证 provider lifecycle/dependency smoke、provider.validate/provider.calculate span、source/license/vendor refs 和 drift report 隐私边界。
- `regression/test_provider_drift_trend_gate.py`：provider/source/license 长期趋势门禁合同；验证 tracked baseline 指纹、当前 scanner 对比、缺 provider、license 回退、vendor hash 漂移和 scanner failed summary 的负向拒绝。
- `regression/test_evidence_coverage_trend_gate.py`：八字/紫微 evidence coverage trend 门禁合同；验证 tracked baseline、规则索引断链拒绝、analysisEvidence 和 Report evidenceRefs 完整度、冲突解释/反证字段以及 CLI summary 输出。
- 服务私有测试可以留在服务根，但必须被根 `scripts/acceptance.sh` 覆盖。
- 不在这里写入运行态、golden 原始资料或外部 vendor 源码。

## 依赖方向

- `tests -> domains + contracts + catalog + governance`
