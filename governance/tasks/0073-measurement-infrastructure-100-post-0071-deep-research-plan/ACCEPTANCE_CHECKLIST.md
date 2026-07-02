# Acceptance Checklist

# Global Standards

- [x] 任务边界明确：planning-only，不实现业务代码。
- [x] 证据来源明确：仓库事实、任务索引、主路线图、外部一手资料。
- [x] 外部验证项明确标记，不伪造完成。
- [x] 0072 outbox worker lease smoke 未被夸大为 job execution worker lease。

# Task Package Checklists

## TP-01 现状复核

Verify: `git status --short --branch`、任务索引和主路线图已读取。

Gate: 0071/0072 状态边界写清。

- [x] 读取 Git 状态、任务索引和主路线图。
- [x] 标记 0071 与 0072 已完成，但仍非生产完成。

## TP-02 外部同构调研

Verify: `RESEARCH.md` source matrix。

Gate: 来源是一手资料或官方资料链接。

- [x] 采集 OpenAPI、AsyncAPI、CloudEvents、Temporal、OpenTelemetry、Google SRE、OWASP、NIST、SLSA、CycloneDX、CNCF 等资料链接。
- [x] 完成同构映射。

## TP-03 FateCat 100% 计划

Verify: `RESEARCH.md` 和主路线图 `0.9`。

Gate: 资源成熟度、任务树、执行顺序和失败判定完整。

- [x] 完成资源成熟度矩阵。
- [x] 完成完整任务树和执行顺序。
- [x] 完成不可伪造证据口径。

## TP-04 文档落盘与验证

Verify: `validate_task_docs.py --phase closeout`。

Gate: 文档无占位符且任务节点可识别。

- [x] 写入 `RESEARCH.md`。
- [x] 更新主路线图 `0.9`。
- [x] 任务文档校验通过。
