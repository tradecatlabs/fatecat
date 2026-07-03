# Execution Checklist

[x] TP-01 | P0 | 确认 pending external occurrence 缺少 owner/凭证/关闭条件 | Verify: `/tmp/fatecat-current-audit-bundle-finalizer-0115/pending-external-validations.json` 字段检查 | Gate: 不伪造外部 live | Parallelizable: No
[x] TP-02 | P0 | 新增 external validation closure contract 和 gate | Verify: script + contract present | Gate: output blocked when pending exists | Parallelizable: No
[x] TP-03 | P0 | 接入 local-ci、tests、AGENTS 和 roadmap | Verify: rg wiring | Gate: docs and tests consistent | Parallelizable: No
[x] TP-04 | P0 | 运行验证、自审、提交推送 | Verify: acceptance commands | Gate: clean pushed branch | Parallelizable: No
