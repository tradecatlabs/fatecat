# Task Overview
- Task ID: `0100`
- Slug: `measurement-infrastructure-provider-source-license-drift-trend`
- Objective: `把单次 provider drift scanner 升级为 provider/source/license 长期趋势门禁：记录 provider/source/license/vendor 指纹、对比历史基线、拒绝 provider/source/license/vendor 证据回退或缺失，并接入 quick CI；不连接真实公网 provider、不做法律许可证结论、不保存真实用户输入或生产凭证。`
- Status: `Done`

## In Scope
- 新增 tracked provider/source/license/vendor 指纹 baseline。
- 新增 provider drift trend 契约和本地 gate。
- 复用现有 provider drift scanner，不重写 provider runtime。
- 增加负向回归测试：缺 provider、license 回退、vendor hash 漂移、scanner failed summary。
- 接入 `scripts/local-ci.sh` quick profile、AGENTS 和路线图文档。

## Out of Scope
- 不连接真实公网 provider。
- 不做许可证法律结论或人工 legal sign-off。
- 不新增或替换 bazi/ziwei/almanac/meihua provider。
- 不实现 provider compatibility matrix、外部 trace backend 或跨版本升级策略。
- 不保存真实用户输入、报告正文、出生地区、token、secret、DSN 或生产外部账号。

## Task Package Tree
```text
TP-01 SPEC: 复核 0084 provider drift scanner 和 0099 Wave A A1
  TP-01.01 读取 scanner、contract、local-ci、provider schema、operations docs
  TP-01.02 定义 trend gate 与 baseline 边界
TP-02 BUILD: 新增趋势门禁
  TP-02.01 新增 provider-drift-baseline 与 trend contract
  TP-02.02 新增 provider-drift-trend-gate 脚本
  TP-02.03 接入 local-ci、AGENTS、provider schema 与路线图文档
TP-03 TEST: 回归验证
  TP-03.01 增加 trend gate 正向和负向测试
  TP-03.02 运行 focused tests、ruff、format、task docs validator
TP-04 SHIP: 收口
  TP-04.01 回填任务文档和 closeout 状态
  TP-04.02 提交并推送当前切片
```

## Requirement Alignment
| Requirement | Implementation |
| --- | --- |
| 防止 provider/source/license 随时间漂移 | `provider-drift-baseline.json` + `provider-drift-trend-gate.py` 对比当前 scanner 输出。 |
| 不重复造 provider runtime | trend gate 只复用 `provider-drift-scanner.py` summary。 |
| 有意变更必须可审查 | provider/source/license/vendor 指纹变化必须同步更新 tracked baseline。 |
| 不伪造外部 live | summary 明确 `外部连通验证待执行`，不接公网 provider 或外部 trace backend。 |
| 可进入 quick CI | `scripts/local-ci.sh` 在 provider drift scanner 后执行 trend gate。 |

## Task Package Overview
| Node ID | Deliverable | Verify |
| --- | --- | --- |
| TP-02.01 | `contracts/fate/capabilities/provider-drift-baseline.json`、`provider-drift-trend-contract.json` | `python3 -m json.tool` |
| TP-02.02 | `scripts/provider-drift-trend-gate.py/.sh` | `bash scripts/provider-drift-trend-gate.sh --output-json <path>` |
| TP-02.03 | local-ci / AGENTS / docs 接线 | regression test wiring assertions |
| TP-03.01 | `tests/regression/test_provider_drift_trend_gate.py` | focused pytest |
| TP-04.01 | 任务文档无占位 | `validate_task_docs.py --phase decompose` |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
