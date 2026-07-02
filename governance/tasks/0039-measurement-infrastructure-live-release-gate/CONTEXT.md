# Context

## Repo Evidence
- 当前 roadmap 明确 `0039-measurement-infrastructure-live-release-gate` 是 0038 后的下一步。
- 已有 `scripts/public-release-gate.sh`，但只输出文本 summary，不能给第三方审计提供结构化 release evidence。
- 已有 `scripts/production-readiness.sh` 支持真实 API `/health`、`/ready`、`/metrics` 和 live Bot，但没有把 HF Space、CI、container digest、SBOM/provenance、rollback drill 统一成一个 ship gate。
- 已有 `contracts/fate/delivery/registry.json` 登记多端交付面，但缺 ReleaseGate 资源。

## Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 无真实生产域名/token/HF/CI 权限 | 不执行 live 验证；输出 pending/blocked |
| 不能泄露 secret | gate 只记录 URL 类型、路径、commit、digest 和摘要；不输出 token 值 |
| 当前 worktree dirty | 本地合同可通过，但 clean git state 只能 pending；`--require-live` 必须失败 |
| public release 不能被本地 smoke 冒充 | 分离 `status` 和 `shipGate.status` |

## Change Boundary
- 可改：`contracts/fate/delivery/`、resource schema、delivery registry API 暴露、release/public/local-ci 脚本、regression tests、AGENTS、API 文档、roadmap、0039 任务文档。
- 禁改：真实生产配置、GitHub secret、HF secret、Bot token、远端 CI 状态、生产服务和历史任务证据。

## Risk Matrix
| Risk | Mitigation |
| --- | --- |
| 本地 gate 通过被误读为生产发布通过 | JSON 顶层 `status=passed` 只表示本地合同；`shipGate.status=blocked` 表示 live release 不可发布 |
| Gate 输出泄露 token | 敏感模式扫描与输出 redaction；测试禁止 `token=`/`secret=`/`password=` |
| `--require-live` 被漏测 | 回归测试要求缺证据时返回非零并输出 blocking items |
| API `/surfaces` 文档漂移 | API contract 测试断言 `releaseGate` 暴露 |

- 调试模式: `Optional`

# Assumptions and Falsification
- 假设：当前本轮不能取得真实外部凭证，因此 0039 的可落地切片是 release evidence contract/gate baseline。
- 反证：如果提供真实 API URL、HF Space URL、Bot token、GitHub Actions run、container digest、SBOM/provenance 和 rollback artifact，应立即使用 `--require-live` 运行真实发布门禁。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01.01 | 从现有脚本和 roadmap 盘点 release evidence 缺口 |
| TP-02.01 | ReleaseGate schema/contract 是发布证据真相源 |
| TP-02.02 | delivery/resource registry 让 ReleaseGate 可发现 |
| TP-03.01 | live-release-gate 执行器产出 JSON |
| TP-03.02 | public-release/local-ci 调用该 gate |
| TP-04.01 | 回归测试锁住 pending/blocked 语义 |
| TP-04.02 | API `/surfaces` 对外暴露 releaseGate |
| TP-05.01 | 文档同步不夸大 live 能力 |
| TP-05.02 | closeout 汇总可复核证据 |

## Critical Ambiguities
- 是否采用 GitHub release artifact、OCI registry attestation 还是第三方平台保存 SBOM/provenance，当前未指定；本轮只接受本地路径或 HTTPS artifact URL。
- rollback drill 的执行平台未指定；本轮只要求 artifact evidence path/URL。

## Debug Evidence Contract
- 本任务不是 bugfix；无需 `DEBUG.md`。
- 若 `live-release-gate.py` 失败，必须保留命令、exit code、JSON 输出和 stderr 摘要。
