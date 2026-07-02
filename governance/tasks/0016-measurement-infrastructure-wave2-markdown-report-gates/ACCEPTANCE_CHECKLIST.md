# Acceptance Checklist

# Global Standards
- [x] 改动只服务 Markdown report gates 切片。
- [x] 不引入新第三方依赖。
- [x] 不改变 Markdown 正文。
- [x] 不删除旧 API 字段。
- [x] 三条用户可见 Markdown 路径均返回 gate。
- [x] 所有“通过”都有命令证据。

# Task Package Checklists
## TP-01.01 Markdown gate scope

Verify: `rg -n "Markdown.*policyGate|snapshotGate" governance/tasks/0016-measurement-infrastructure-wave2-markdown-report-gates`

Gate: scope 明确覆盖同步、标准异步、Web 异步。

- [x] 已完成：scope 覆盖同步 Markdown、标准异步 job、Web 异步 job。

## TP-01.02 report schema contract

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'policy or snapshot or report'`

Gate: schema 说明 policyGate/snapshotGate 对 Markdown 的覆盖范围。

- [x] 已通过：protocol targeted tests 4 passed；组合回归 22 passed。

## TP-02.01 Markdown policy helper

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'policy'`

Gate: 正文违规样本 fail，正常样本 pass。

- [x] 已通过：Markdown policy helper fail/pass 单测。

## TP-02.02 Markdown snapshot helper

Verify: `.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py -k 'snapshot'`

Gate: bazi/ziwei 核心 heading 缺失返回 fail。

- [x] 已通过：Markdown snapshot helper heading pass/fail 单测。

## TP-03.01 synchronous markdown API

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'markdown and gate'`

Gate: `/api/v1/report/markdown` 返回 gate。

- [x] 已通过：同步 Markdown API 返回 policyGate/snapshotGate。

## TP-03.02 standard report job

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'job and gate'`

Gate: `/api/v1/report/jobs/{job_id}` result 返回 gate。

- [x] 已通过：标准异步 job 成功 result 返回 policyGate/snapshotGate。

## TP-03.03 web report job

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k 'web and gate'`

Gate: Web job result 返回 gate。

- [x] 已通过：Web 异步 job 成功 result 返回 policyGate/snapshotGate。

## TP-04.01 regression tests

Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py -k 'policy or snapshot or report or markdown or job or web'`

Gate: 组合回归通过。

- [x] 已通过：组合回归 22 passed。

## TP-04.02 docs

Verify: `rg -n "policyGate|snapshotGate|Markdown 正文" docs/reference-materials contracts/fate/capabilities governance/tasks/0016-measurement-infrastructure-wave2-markdown-report-gates`

Gate: 文档说明本轮 gate 边界。

- [x] 已完成：API 文档、100% 计划、report schema 同步。

## TP-05.01 local gates

Verify: `bash scripts/local-ci.sh --profile quick`

Gate: quick CI、governance strict、diff check 通过。

- [x] 已通过：quick CI 68 passed，governance strict PASS，diff check PASS。

## TP-05.02 task closeout

Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0016-measurement-infrastructure-wave2-markdown-report-gates --phase closeout`

Gate: closeout 通过。

- [x] 已通过：closeout validator 和全任务树 validator 已通过。
