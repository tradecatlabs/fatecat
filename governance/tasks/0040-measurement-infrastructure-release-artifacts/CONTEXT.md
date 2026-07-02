# Repo Evidence
- `contracts/fate/delivery/release-gate.json` 已登记 `evidence.sbom_artifact` 和 `evidence.provenance_artifact`。
- `scripts/live-release-gate.py` 已接受 `--sbom-path` 和 `--provenance-path`。
- `docs/reference-materials/roadmap/测算基础设施100%实现计划.md` 标注 SBOM/provenance 仍待后续。
- 仓库已有 `pyproject.toml`、`requirements.lock.txt`、`requirements-dev.lock.txt`、Dockerfile 和关键 contracts/scripts，可生成本地 release artifact baseline。

# Constraints Matrix
| Constraint | Decision |
| --- | --- |
| 不新增依赖 | 用 Python 标准库 `tomllib/json/hashlib/subprocess` |
| worktree dirty | 记录 dirtyCount，不阻断本地生成；真实发布仍由 live gate clean git 阻断 |
| 不伪造远端 attestation | provenance 标注 local baseline，不写远端 CI 通过 |
| 不泄露 secret | artifact 只写依赖名/版本、文件 hash、git metadata，不写环境变量值 |

# Change Boundary
- 可改：`scripts/release-artifacts.*`、`scripts/local-ci.sh`、`scripts/public-release-gate.sh`、delivery release gate/registry contract、regression tests、AGENTS、API 文档、roadmap、0040 任务文档。
- 禁改：真实生产环境、registry、GitHub secrets、HF secrets、Bot token、container image push、历史任务证据。

# Risk Matrix
| Risk | Mitigation |
| --- | --- |
| 本地 provenance 被误解为 SLSA 远端证明 | manifest limitations 和 roadmap 明确不是 remote CI attestation |
| artifact 写入敏感信息 | 生成器不读取 env；verify 扫描敏感赋值 marker |
| quick CI 变慢 | 只解析 lockfile 和少量文件 hash，不访问网络 |

# Assumptions and Falsification
- 假设：当前没有 registry/CI attestation 平台；本轮只做本地 baseline。
- 反证：如果提供 GitHub release、OCI registry、cosign/SLSA 平台，应进入远端 attestation 任务，而不是扩展本地脚本假装完成。

# Task Package Context Map
| Node | Context |
| --- | --- |
| TP-01.01 | 明确 0039 中 SBOM/provenance pending 的具体接口 |
| TP-02.01 | 生成器只用标准库和仓库文件 |
| TP-02.02 | 生成并校验三个 JSON artifact |
| TP-03.01 | public/local gate 自动生成 artifact |
| TP-03.02 | live release gate 消费 artifact path |
| TP-04.01 | pytest 锁住 artifact 结构与 gate 消费 |
| TP-04.02 | 文档不夸大为远端发布证明 |
| TP-05.01 | closeout 汇总验证证据 |

- 调试模式: `Optional`

# Critical Ambiguities
- 远端 SBOM/provenance 应存 GitHub artifact、OCI registry attestation 还是 release asset，当前未定。
- container digest 和签名仍需真实 registry 或 CI 构建证据。

# Debug Evidence Contract
- 本任务不是 bugfix；无需 `DEBUG.md`。
- 若 artifact verify 失败，必须保留输出目录、summary JSON 和错误列表。
