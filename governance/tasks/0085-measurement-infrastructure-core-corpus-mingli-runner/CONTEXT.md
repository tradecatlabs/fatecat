# Repo Evidence
| Source | Evidence |
| --- | --- |
| `git status --short --branch` | `main...origin/main` clean before 0085 implementation |
| `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` | 0085 is Core corpus and MingLi-Bench runner |
| `contracts/fate/evaluations/core-quality-corpus.json` | 5 corpora, bazi/ziwei anonymous fixtures, release gate required |
| `scripts/run-mingli-bench.sh` | supports stats, prompt-out and predictions evaluation |
| `scripts/generate-mingli-predictions.sh` | calls FateCat pure-analysis baseline without external model API |
| `tools/reference-repos/vendor_sources.json` | MingLi-Bench is MIT/SPDX, evaluation_only, productionUseAllowed=false |
| `git ls-remote https://github.com/DestinyLinker/MingLi-Bench HEAD` | upstream HEAD observed as `b7433280fd86d7a7c27debbc47d0303c218f0bfd` |

# Constraints Matrix
| Constraint | Handling |
| --- | --- |
| 不污染生产路径 | MingLi-Bench 保持 `evaluation_only`、`releaseRequired=false` |
| 不泄露 benchmark 明细 | 新 gate 只输出聚合 summary，不输出题目、出生信息、标准答案或逐题结果 |
| 不调用外部模型 API | gate 只调用本地 FateCat baseline generator |
| 不联网更新 vendor | 上游 HEAD 只作为事实记录，不自动拉取 |
| 不伪造专业准确率 | accuracy 仅是 weak-rule baseline aggregate，不写成专家结论 |

# Change Boundary
- Allowed: `contracts/fate/evaluations/*`、`scripts/mingli-bench-gate.py/.sh`、`scripts/local-ci.sh`、`tests/regression/`、`docs/reference-materials/operations/`、`docs/reference-materials/roadmap/`、AGENTS、`governance/tasks/0085-*`。
- Read-only context: MingLi-Bench vendor snapshot、core corpus fixtures、baseline generator、run-mingli evaluator。
- Forbidden: production provider behavior、默认报告结构、外部模型 API、真实用户数据、vendor 自动更新。

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| 逐题结果误入 CI artifact | aggregate gate 不输出 `results`、`answer`、`question`、`birth_info` |
| optional benchmark 被误读为 release 必跑 | registry 保持 `gateType=optional`、`releaseRequired=false` |
| license/usage 边界漂移 | gate 校验 vendor manifest 和 data supply chain registry |
| 上游已变化但本地 snapshot 未更新 | task context 记录上游 HEAD，更新另开任务 |
| baseline accuracy 被误当专业能力 | summary boundary 和 docs 明确 weak-rule aggregate only |

# Assumptions and Falsification
- Assumption: 0085 的最小正确切片是脱敏 aggregate gate，而不是 full external model benchmark。
- Falsifier: 如果 gate summary 出现题目、出生信息、标准答案或逐题结果，本任务失败。
- Assumption: `run-mingli-bench.sh` 仍可保留为本地调试工具。
- Falsifier: 如果 CI/dashboard 需要保存逐题 `results` 才能工作，则 no-leak 设计不成立，必须重新设计 artifact 分层。

# Critical Ambiguities
- 外部模型评测、专家人工评审和上游 snapshot 更新不在本任务内。
- MingLi-Bench 包含公开 benchmark 出生信息和答案，必须保持 review_required/evaluation_only 边界。

# Debug Evidence Contract
- 调试模式: Optional

本任务是 gate hardening，不是 bugfix；若 gate、CI 或 regression 失败，则记录失败命令、根因、修复和回归证据。

# Task Package Context Map
| Node ID | Context |
| --- | --- |
| TP-01.01 | core corpus、MingLi scripts、vendor manifest、registry、upstream ls-remote |
| TP-02.01 | no-leak contract、forbidden fragments、required local sources |
| TP-03.01 | `scripts/mingli-bench-gate.py/.sh` |
| TP-04.01 | registry、docs、AGENTS、local-ci |
| TP-04.02 | data supply chain registry sha256 |
| TP-05.01 | focused MingLi tests |
| TP-05.02 | data supply chain gate、quick CI、task validators、git/CI delivery |

# Task Context

## 当前事实

- 当前分支：`main`
- 起点 commit：`466cac3 feat: add provider drift scanner`
- 0084 已完成 provider drift scanner baseline。
- `contracts/fate/evaluations/core-quality-corpus.json` 已登记 5 个八字/紫微核心 corpus，当前本地统计为 325+ cases。
- `scripts/run-mingli-bench.sh` 和 `scripts/generate-mingli-predictions.sh` 已存在，但前者在 evaluation 模式会生成逐题结果，不适合作为 CI artifact。
- `tools/reference-repos/vendor_sources.json` 中 `MingLi-Bench` 为 `evaluation_only`、`productionUseAllowed=false`、MIT/SPDX。
- 上游当前 HEAD 通过 `git ls-remote https://github.com/DestinyLinker/MingLi-Bench HEAD` 查得为 `b7433280fd86d7a7c27debbc47d0303c218f0bfd`；本地 vendor 是无 `.git` snapshot，不在本任务自动更新。

## 问题

`MingLi-Bench` 能跑，但还缺一层适合交付/审计的聚合 gate：

- 不能把逐题标准答案写入 CI artifact。
- 不能把 benchmark 出生信息或题干进入报告、dashboard、summary。
- 不能让 optional reference repo benchmark 看起来像 production release 必跑。
- 不能把 license/usage 分级和 runner 结果分散在多个脚本里让审计人员拼。

## 约束

- 只使用本地 tracked 文件和 reference repo snapshot。
- 不联网运行 gate。
- 不读取 `.env`、真实 token、secret、DSN 或生产账号。
- 不新增 production capability。
- 不改变八字/紫微 production report 结构。
