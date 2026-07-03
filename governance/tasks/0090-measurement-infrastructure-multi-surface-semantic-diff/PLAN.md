# Planning Summary

0090 把 DeliverySurface registry 的同源声明变成可运行 gate。重点是“同一报告 profile、同一计算引擎、同一 renderer、同一隐私边界”，而不是新增命理功能。

# Lifecycle Gates

| Phase | Gate |
| --- | --- |
| SPEC | 识别 API/Web/Bot 标准 Markdown 当前是否存在实际漂移。 |
| PLAN | 定义 required surfaces、partial surfaces、external pending 和 volatile normalization。 |
| BUILD | 修复 API/Bot capability 引擎接线，新增 contract/script/local-ci/regression/docs。 |
| TEST | focused regression、脚本 smoke、ruff、secret scan、quick CI 通过。 |
| REVIEW | 证据 JSON 不保存完整 Markdown；外部 live 保持 pending。 |
| SHIP | commit/push 后远端 acceptance/container 与 current release proof 重新验证。 |

# Execution Waves

| Wave | Nodes |
| --- | --- |
| W1 | TP-01, TP-02 |
| W2 | TP-03 |
| W3 | TP-04 |
| W4 | TP-05 |

# Runtime Workflow Contract

- 命令：`bash scripts/multi-surface-semantic-diff.sh --output-json <path>`。
- 输出 kind：`fatecat.multi_surface_semantic_diff`。
- 本地 required surfaces：API direct、API HTTP、API job、Web direct、Web job、Bot dry-run canonical renderer。
- 对比策略：normalized Markdown semantic hash。
- 允许归一化字段：紫微 `运限日期` runtime `asOf`。
- 失败条件：hash 不一致、Bot static chain 断裂、证据包含报告正文或敏感标记。

# Rollback Protocol

- 移除 `scripts/multi-surface-semantic-diff.py/.sh`。
- 移除 `contracts/fate/delivery/multi-surface-semantic-diff.json` 和 registry gate。
- 从 `scripts/local-ci.sh` 和 focused regression 列表移除该 gate。
- 回滚 `main.py` / `bot.py` capability 引擎接线时必须重新评估 API/Web/Bot 标准 Markdown 是否允许分叉。

# Next Executable Leaves

| Node ID | Action |
| --- | --- |
| TP-04 | Run focused tests, ruff, secret scan and quick CI. |

# Dependency Graph

```text
TP-01 -> TP-02 -> TP-03 -> TP-04 -> TP-05
```
