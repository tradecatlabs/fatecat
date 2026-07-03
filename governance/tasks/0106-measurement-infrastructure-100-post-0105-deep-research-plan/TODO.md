# Execution Checklist
[x] TP-01.01 | P0 | 复核官方资料版本和适用性 | Verify: `RESEARCH.md` source matrix | Gate: 只使用官方/事实标准来源 | Parallelizable: Yes
[x] TP-01.02 | P0 | 提炼 FateCat post-0105 映射原则 | Verify: `RESEARCH.md` resource maturity matrix | Gate: 每个映射有 next slice 或 pending | Parallelizable: Yes
[x] TP-02.01 | P0 | 读取主路线图和 0104/0105 任务事实 | Verify: roadmap + task status paths | Gate: 当前事实不靠记忆 | Parallelizable: Yes
[x] TP-02.02 | P0 | 识别当前 HEAD 的远端证据缺口 | Verify: `gh run list --commit HEAD` result | Gate: missing run 不写成 passed | Parallelizable: Yes
[x] TP-03.01 | P0 | 定义资源成熟度矩阵 | Verify: matrix covers release/evaluation/evidence/runtime/security/SRE/DX/audit | Gate: 不隐藏 external live pending | Parallelizable: No
[x] TP-03.02 | P0 | 定义执行波次、下一任务树和不可伪造证据 | Verify: roadmap post-0105 section | Gate: 下一 P0 可直接执行 | Parallelizable: No
[x] TP-04.01 | P0 | 更新 RESEARCH、任务包和主路线图 | Verify: git diff scoped | Gate: 不改业务代码 | Parallelizable: No
[x] TP-04.02 | P0 | 运行文档校验、占位符检查和引用检查 | Verify: validator + rg scans | Gate: 无占位符，task docs pass | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
