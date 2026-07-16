# Task-Level Acceptance
- v3 paragraph 明确 `paragraphType` 与 `sourceLineNumbers`，每个 body 段可精确回放来源。
- 已确认目录保留在 paragraphs，但不进入 passages。
- 相邻物理换行按确定性规则重建，semantic fingerprint 与 selected source lines 一致。
- passage 不跨 heading path，且不超过 max chars。
- canonical TXT bytes/hash 不变；权限边界继续关闭。
- v2 保留为 ignored 回滚基线，默认构建切换到 v3。

# Validation Plan
```bash
.venv/bin/python -m pytest -q tests/regression/test_classics_dataset_clean.py
.venv/bin/python scripts/classics-dataset-clean.py
.venv/bin/python scripts/classics-dataset-clean.py --validate-only
bash scripts/data-supply-chain-gate.sh
bash scripts/local-ci.sh --profile quick
```

# Review Gate
- Correctness：无字词丢失、源行血缘精确、目录分流和 heading flush 正确。
- Knowledge assets：canonical 与人工书目边界不变，不把派生标题树包装成学术校勘。
- Performance：仍为 O(total source chars + output records)，无二次全库扫描放大。
- Future optimal：v3 是单一默认派生契约，不保留双轨运行代码；v2 仅作为本地旧产物。

# Runtime Verification Gate
- `semanticReplayErrorCount=0`。
- `passageHeadingBoundaryViolationCount=0`。
- `navigationPassageCount=0`。
- `lineageErrorCount=0`、`invalidUtf8Count=0`。
- 连续两次构建 dataset hash 一致，canonical 聚合 hash 不变。

# Ship Readiness
- 可提交：v3 contract、policy、owner script、门禁、测试、文档与任务证据。
- 不可提交：v2/v3 ignored 正文、raw 或外部下载资产。
- 不可声明：人工书目已完成、版权已清、可公开训练/生产。

# Task Package Acceptance
| Node | Acceptance |
| --- | --- |
| TP-01 | v3 schema、policy 和 registry fail closed |
| TP-02 | wrapped line reconstruction 与 heading hierarchy 测试通过 |
| TP-03 | navigation 零入 passage、跨 heading violation 为零 |
| TP-04 | 真实 14 本 build/validate/data gate 和 hash 证据通过 |
| TP-05 | deep review、Quick CI、task strict、Git 边界通过 |

# Anti-Goals
- 不修改 canonical TXT。
- 不让启发式规则删除正文。
- 不用 LLM 或模糊模型决定结构。
- 不为兼容 v2 保留第二套执行分支。
- 不虚构书目、版权、完整性或生产可用结论。
