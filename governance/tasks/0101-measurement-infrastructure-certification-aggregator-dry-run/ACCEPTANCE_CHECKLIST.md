# Acceptance Checklist

# Global Standards
- [x] 不残留模板占位符。
- [x] 任务包包含 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP` 生命周期门禁。
- [x] `CONTEXT.md` 声明 `调试模式: Optional`。
- [x] 聚合器不连接真实外部系统，不读取真实 `.env`、token、secret 或 DSN。
- [x] `blocked`/`pending` 不能被解释为 100% 完成。
- [x] final quick local-ci、secret scan 和 closeout validator 通过。
- [x] 版本控制状态与远端状态收口。

# Task Package Checklists
## TP-01.01
Verify: `rg -n "current audit bundle|live release gate|provider drift trend" scripts/local-ci.sh`

Gate: local-ci evidence 来源已确认。

- [x] release、audit、provider trend、core quality、security、SRE、runtime、developer 证据来源已映射。
- [x] 外部 live 未闭合时不得声明 100%。

## TP-01.02
Verify: `cat contracts/fate/audit/measurement-infrastructure-certification.json`

Gate: contract 能指导 aggregator 和审计人员复核。

- [x] required evidence files 已列出。
- [x] forbidden report fragments、privacy boundary 和 release boundary 已列出。

## TP-02.01
Verify: `bash scripts/measurement-infrastructure-certification.sh --evidence-dir /tmp/fatecat-local-ci-0100-final --output-json /tmp/fatecat-certification-0101.json`

Gate: blocked dry-run 不允许 100% 声明。

- [x] CLI/wrapper 可执行。
- [x] missing evidence 输出 failed。
- [x] 字符串型 `shipGate=blocked` 能被识别为 blocked。

## TP-02.02
Verify: `rg -n "measurement-infrastructure-certification|certification aggregator" scripts/local-ci.sh scripts/AGENTS.md contracts/fate/audit/AGENTS.md tests/AGENTS.md`

Gate: local-ci 和架构说明已同步。

- [x] local-ci 生成 certification artifact。
- [x] local-ci summary 输出 certification artifact 路径。
- [x] `AGENTS.md` 和人类文档记录入口。

## TP-03.01
Verify: `.venv/bin/python -m pytest -q tests/regression/test_measurement_infrastructure_certification.py`

Gate: 关键路径有 regression 覆盖。

- [x] blocked dry-run 覆盖。
- [x] `--require-certified` 拒绝 blocked 覆盖。
- [x] missing evidence fail 覆盖。
- [x] synthetic full pass 覆盖。

## TP-03.02
Verify: `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0101-final`

Gate: 本地发布前门禁通过。

- [x] certification smoke passed。
- [x] focused pytest passed。
- [x] ruff check/format passed。
- [x] quick local-ci passed。
- [x] secret scan passed。
- [x] diff whitespace check passed。

## TP-04.01
Verify: `python3 /home/lenovo/.codex/skills/auto-tasks/scripts/validate_task_docs.py --task-dir governance/tasks/0101-measurement-infrastructure-certification-aggregator-dry-run --phase closeout`

Gate: 任务文档 closeout 契约通过。

- [x] `README.md`、`CONTEXT.md`、`PLAN.md`、`TODO.md`、`STATUS.md`、`ACCEPTANCE.md`、`ACCEPTANCE_CHECKLIST.md` 已同步。
- [x] `governance/tasks/INDEX.md` 中 0100/0101 状态正确。
- [x] closeout validator passed。

## TP-04.02
Verify: `git status --short --branch && git ls-remote origin refs/heads/main`

Gate: 版本控制收口，不伪造远端 CI。

- [x] scoped files staged and committed。
- [x] push to `origin/main` completed。
- [x] 本地 HEAD 与 origin/main 匹配。
- [x] GitHub Actions 对当前 commit 的状态如实记录。
