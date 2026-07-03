# Acceptance Checklist

# Global Standards
- [x] 只使用当前 branch/worktree 事实。
- [x] 不把 local acceptance 写成远端 Acceptance。
- [x] 不把 workflow dispatch 写成 workflow success。
- [x] 不把 dry-run rollback 写成真实生产 rollback。
- [x] 不声明生产 API/HF/Bot/OIDC/SIEM/OTel/Vault/KMS live 完成。
- [x] 最终 proof 不写回 Git，避免新 HEAD 递归漂移。

# Task Package Checklists
## TP-01
- [x] `INDEX.md` 中 0108 只剩一行。
- [x] 0110 任务包完整落盘。
- [x] Verify: index row count and task docs validator.
- [x] Gate: row count equals one and validator passes.

## TP-02
- [x] 0110 文档状态提交并推送。
- [x] 最终 HEAD 干净。
- [x] Verify: git status.
- [x] Gate: origin contains final HEAD and no dirty files.

## TP-03
- [x] Acceptance workflow 已为最终 HEAD 发起。
- [x] Container workflow 已为最终 HEAD 发起，且 push_image=true。
- [x] Verify: run detail.
- [x] Acceptance 与 Container workflow 均 terminal success。
- [x] Gate: headSha equals final HEAD, status completed and conclusion success.

## TP-04
- [x] rollback dry-run evidence passed。
- [x] current-release-proof passed。
- [x] Verify: proof JSON.
- [x] Gate: production rollback remains false; pending and failed counts are zero.
