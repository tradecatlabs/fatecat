# Audit Case Sampling Decision

- Source: governance/tasks/0166-sop-library-and-natural-language-routing
- Fixed Problem: 稳定重复任务此前分散在 scripts、contracts、历史任务和聊天上下文中，缺少一任务一文档和自然语言唯一路由的长期流程层。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: process_knowledge_fragmentation
- Trigger Signals: 相同自然语言任务命中多个流程；操作参数依赖聊天记忆；planned 能力被误当生产能力。
- Evidence: 41 份独立 SOP、唯一路由索引、`tests/regression/test_sop_library.py` 6 项回归、governance strict/health PASS、Quick CI 538 passed。
- No-Case Reason: 本轮是首次建立长期 SOP 与机器路由能力，不是已发生缺陷的重复修复；专项回归已直接阻断章节缺失、路由冲突、路径漂移和 capability 状态误报。

## Reusable Audit Questions
- 每个稳定任务是否只对应一个 SOP 和一个 route key？
- planned capability 是否只能进入研发接入流程并 fail closed？
- 文档是否复用 tracked 工具、参数和证据，而没有制造第二套命令入口？
- 外部 live 步骤是否明确区分本地可验证与外部待执行？

## Evidence Required
- SOP 文件与索引集合一致性、route key/alias 唯一性、registry 状态对照、脚本路径解析、治理 strict/health 和项目 Quick CI。
