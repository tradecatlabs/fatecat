# Task Overview

- Task ID: `0059`
- Slug: `measurement-infrastructure-webhook-encrypted-config-vault-baseline`
- Objective: `执行 MI-NEXT-03 durable runtime 二期第八个可验证切片：在 0058 SQLite webhook outbox redelivery baseline 之后，为 report job webhook callback 增加本地 SQLite encrypted delivery config vault baseline；让 failed/pending outbox record 能在 manager 重建后通过本地加密配置恢复 callback URL/secret 并完成重投，同时支持 key rotation。本任务不实现外部 Vault/KMS、external backend、分布式 worker lease、真实公网 webhook live smoke 或 exactly-once。`
- Status: `Done`

## In Scope

- 引入成熟 `cryptography` / Fernet 依赖，不自研密码学。
- 为 SQLite report job store 增加可选 encrypted webhook delivery config 表。
- 初次 webhook 投递时持久化密文 callback config；投递成功后删除密文；投递失败时保留密文供 redelivery 使用。
- Manager 重建后在没有外部 `delivery_resolver` 时，可通过 encrypted config vault 解密并重投 failed/pending outbox。
- 增加 key rotation baseline：旧 key 加密的 pending/failed config 可被新 active key 重新加密。
- 增加 smoke、回归测试、quick CI、API 文档、roadmap、scripts/tests AGENTS 和任务索引。

## Out of Scope

- 不实现外部 Vault、KMS、Secret Manager、HSM 或云平台 secret backend。
- 不实现 Redis/Postgres/Temporal/Celery adapter。
- 不实现分布式 worker lease、多副本锁、exactly-once 或真实公网 webhook live smoke。
- 不在 API、event、summary、日志或 outbox payload 中输出 webhook URL、webhook secret、密文正文、报告正文或用户输入。
- 不把本地 encrypted vault baseline 声明为生产 secret 管理最终方案。

## Task Package Tree

```text
TP-01 Secret vault 缺口复核
  TP-01.01 读取 roadmap、0056/0058、webhook/report job 源码、依赖和测试
TP-02 Encrypted config vault 实现
  TP-02.01 引入 cryptography 依赖和 Fernet codec
  TP-02.02 增加 SQLite encrypted config 存储、读取、删除和 rotation
  TP-02.03 Manager 接入 encrypted config redelivery fallback
TP-03 Smoke、测试与 CI
  TP-03.01 新增 webhook encrypted config vault smoke 与 shell wrapper
  TP-03.02 增加 regression tests，覆盖密文不含明文、重建重投、成功删除和 key rotation
  TP-03.03 接入 local-ci quick
TP-04 文档与验收
  TP-04.01 更新 API 文档、roadmap、AGENTS 和 INDEX
  TP-04.02 运行 focused tests、validators、lint/hygiene、quick local CI 和 git 交付
```

## Requirement Alignment

- 对齐 roadmap：`MI-NEXT-03` 剩余缺口中的 `持久 callback secret 加密/轮换`。
- 对齐安全边界：持久化只允许密文；明文 URL/secret 只在运行时内存中恢复用于投递。
- 对齐 0058：`delivery_resolver` 仍可作为外部配置入口；encrypted config vault 是本地可验收 fallback。

## Task Package Overview

| Task Package ID | Parent | Depth | Priority | Type | Leaf | Depends On | Wave | Ready | Parallelizable | Objective |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | P0 | package | No | - | - | No | Yes | 复核 encrypted config vault 缺口和现有边界。 |
| TP-01.01 | TP-01 | 2 | P0 | action | Yes | - | 1 | No | Yes | 读取 roadmap、任务事实、源码、依赖和测试。 |
| TP-02 | ROOT | 1 | P0 | package | No | TP-01.01 | - | No | No | 实现本地 encrypted config vault baseline。 |
| TP-02.01 | TP-02 | 2 | P0 | action | Yes | TP-01.01 | 2 | No | No | 引入 cryptography 和 Fernet codec。 |
| TP-02.02 | TP-02 | 2 | P0 | action | Yes | TP-02.01 | 2 | No | No | 增加 SQLite encrypted config 存储和 rotation。 |
| TP-02.03 | TP-02 | 2 | P0 | action | Yes | TP-02.02 | 2 | No | No | Manager 接入 encrypted config redelivery fallback。 |
| TP-03 | ROOT | 1 | P0 | package | No | TP-02.03 | - | No | No | Smoke、测试与 CI。 |
| TP-03.01 | TP-03 | 2 | P0 | action | Yes | TP-02.03 | 3 | No | No | 新增 smoke 与 shell wrapper。 |
| TP-03.02 | TP-03 | 2 | P0 | action | Yes | TP-03.01 | 3 | No | No | 增加 regression tests。 |
| TP-03.03 | TP-03 | 2 | P0 | action | Yes | TP-03.02 | 3 | No | No | 接入 local-ci quick。 |
| TP-04 | ROOT | 1 | P0 | package | No | TP-03.03 | - | No | No | 文档与验收。 |
| TP-04.01 | TP-04 | 2 | P0 | action | Yes | TP-03.03 | 4 | No | No | 更新文档、AGENTS 和 INDEX。 |
| TP-04.02 | TP-04 | 2 | P0 | action | Yes | TP-04.01 | 4 | No | No | 运行验证并提交推送。 |

## Reading Order

1. `README.md`
2. `CONTEXT.md`
3. `PLAN.md`
4. `ACCEPTANCE.md`
5. `ACCEPTANCE_CHECKLIST.md`
6. `TODO.md`
7. `STATUS.md`
