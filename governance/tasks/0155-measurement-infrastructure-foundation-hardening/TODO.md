# Execution Checklist
[x] TP-01 | P0 | 建立可独立分发闭包 | Verify: wheel clean-room smoke + export runtime smoke + size/file-count gate | Gate: 独立安装和精简导出全部通过 | Parallelizable: No
[x] TP-02 | P0 | 统一综合八字生产引擎 | Verify: Web/API/Bot normalized semantic parity tests | Gate: 不存在默认 legacy 生产路径 | Parallelizable: No
[x] TP-03 | P0 | 隔离 Telegram 渠道就绪状态 | Verify: Telegram lifecycle/readiness/metrics tests | Gate: 核心 API 可用且渠道故障明确可见 | Parallelizable: No
[ ] TP-04 | P0 | 补齐自动 CI 与发布证明 | Verify: workflow regression + action syntax + current release proof | Gate: 最终提交拥有真实远端 quick CI 证据 | Parallelizable: No
[x] TP-05 | P1 | 加固供应链与 vendor 卫生 | Verify: vendor health before/after tests + distribution policy gate | Gate: reference repo 只读且禁止资产不进入发行物 | Parallelizable: No
[x] TP-06 | P1 | 恢复治理真相源 | Verify: governance context bundle + strict validation + document drift review | Gate: 治理路由不再 BLOCK 且事实与实现一致 | Parallelizable: No
[ ] TP-07 | P0 | 性能、质量与交付收口 | Verify: quick CI + performance baseline + task review + closeout + remote CI | Gate: 本地实现无 BLOCK；外部人工/live 门禁真实保留 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
