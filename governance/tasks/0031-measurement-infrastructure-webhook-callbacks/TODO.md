# Execution Checklist
[x] TP-01.01 | P0 | 盘点 report job 状态机、API、registry、roadmap 缺口 | Verify: `rg -n "report/jobs|CalculationJob|webhook" docs contracts governance scripts tests domains/experience-delivery/services/fatecat-delivery/src` | Gate: MI-03.03 缺口明确 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 webhook payload、HMAC 签名、URL 校验和可注入 dispatcher | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k webhook` | Gate: payload 不含报告正文和 secret | Parallelizable: No
[x] TP-02.02 | P0 | 接入 report job succeeded/failed/cancelled 终态 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k webhook` | Gate: terminal callback 在锁外执行且失败不破坏任务状态 | Parallelizable: No
[x] TP-02.03 | P0 | 接入 API headers 和默认关闭保护 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py -k webhook` | Gate: 默认关闭返回 403，启用后响应/audit 不回显 secret | Parallelizable: No
[x] TP-03.01 | P0 | 新增本地 webhook smoke simulator | Verify: `bash scripts/webhook-smoke.sh --output-json /tmp/fatecat-webhook-smoke.json` | Gate: 不访问公网，输出 passed JSON | Parallelizable: No
[x] TP-03.02 | P0 | 新增 smoke 回归测试 | Verify: `.venv/bin/python -m pytest -q tests/regression/test_webhook_smoke.py` | Gate: smoke CLI 和 run_smoke 均通过 | Parallelizable: No
[x] TP-03.03 | P0 | 接入 quick local-ci 并运行 | Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-webhook` | Gate: quick CI 通过 | Parallelizable: No
[x] TP-04.01 | P1 | 更新 contracts/env/docs/AGENTS/roadmap | Verify: `python3 -m json.tool contracts/fate/security/registry.json` | Gate: 文档不夸大真实公网 webhook 或 retry 能力 | Parallelizable: Yes
[x] TP-04.02 | P0 | 生成任务 closeout packet | Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0031-measurement-infrastructure-webhook-callbacks --phase closeout` | Gate: closeout packet 写入任务目录 | Parallelizable: No

说明：
- 每一行绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
