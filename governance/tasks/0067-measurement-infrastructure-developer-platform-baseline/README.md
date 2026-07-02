# Task Overview

- Task ID: `0067`
- Slug: `measurement-infrastructure-developer-platform-baseline`
- Objective: `执行 0061 后续任务树的 developer platform 切片：新增 SDK/package baseline、sandbox token contract、API changelog 与开发者平台 gate，并接入 docs smoke/local-ci；不把本地 docs smoke 伪装成已发布 SDK，不声明公网 sandbox token 服务已上线。`
- Status: `Done`

## In Scope

- 新增 `contracts/fate/developer/developer-platform.json`，统一登记 OpenAPI、SDK/package baseline、sandbox、API changelog 和 validation gate。
- 新增 `contracts/fate/developer/sandbox-token-contract.json`，定义未来公网 sandbox token 的 claim、scope、rate limit、revocation 和负向证据边界。
- 新增 `contracts/fate/developer/api-changelog.json` 与 `docs/reference-materials/developer/API_CHANGELOG.md`，建立 API 兼容策略和变更记录。
- 新增 `docs/reference-materials/developer/SDK_PACKAGE_BASELINE.md`，明确当前只有 installable examples 和 package metadata，不声明 PyPI/npm SDK 已发布。
- 新增 `scripts/developer-platform-gate.py` 与 shell wrapper，并接入 `scripts/local-ci.sh`。
- 更新 `/metadata` developer entries、目录级 AGENTS、developer README、API 接入文档、roadmap 和回归测试。

## Out of Scope

- 不发布 PyPI/npm SDK package。
- 不上线公网 sandbox token issuer、gateway、rate limit 或 revocation 服务。
- 不建立外部 developer portal。
- 不连接真实 token、真实账号、真实生产域名、公网 API、Bot 或第三方云服务。
- 不保存真实用户输入、非北京真实地区、报告正文、生产 URL、secret、DSN、私钥或证书。

## Requirement Alignment

- 对齐 0061 推荐任务：`0067 developer platform`，最小交付物为 SDK/package baseline、sandbox token contract、API changelog。
- 对齐基础设施目标：开发者平台必须有机器契约、版本兼容策略、可验证 gate 和明确发布边界。
- 对齐风险约束：本地 docs smoke 和 installable examples 不能被写成已发布 SDK，token contract 不能被写成公网 token 服务已上线。

## Task Package Tree

```text
TP-01 Context audit
  TP-01.01 复核现有 developer docs、sandbox fixture、OpenAPI export、local-ci 和 metadata
TP-02 Developer contracts
  TP-02.01 新增 developer platform contract
  TP-02.02 新增 sandbox token contract
  TP-02.03 新增 API changelog contract 和 human changelog
TP-03 Gate and service metadata
  TP-03.01 新增 developer-platform-gate
  TP-03.02 接入 /metadata、local-ci 和 summary artifact
  TP-03.03 新增回归测试
TP-04 Docs and closeout
  TP-04.01 同步 AGENTS、developer README、API 接入文档和 roadmap
  TP-04.02 运行验证并收口本地交付证据
```

## Task Package Overview

| Task Package ID | Parent | Priority | Type | Leaf | Depends On | Objective |
| --- | --- | --- | --- | --- | --- | --- |
| TP-01.01 | TP-01 | P0 | action | Yes | - | 明确 developer platform 已有 OpenAPI、sandbox、examples、metadata 和 local-ci 接线。 |
| TP-02.01 | TP-02 | P0 | action | Yes | TP-01.01 | 新增 developer platform contract。 |
| TP-02.02 | TP-02 | P0 | action | Yes | TP-02.01 | 新增 sandbox token contract。 |
| TP-02.03 | TP-02 | P0 | action | Yes | TP-02.02 | 新增 API changelog contract 和 human changelog。 |
| TP-03.01 | TP-03 | P0 | action | Yes | TP-02.03 | 新增 developer platform gate。 |
| TP-03.02 | TP-03 | P0 | action | Yes | TP-03.01 | 接入 `/metadata`、local-ci 和 summary artifact。 |
| TP-03.03 | TP-03 | P0 | action | Yes | TP-03.02 | 新增 developer platform 回归测试。 |
| TP-04.01 | TP-04 | P0 | action | Yes | TP-03.03 | 同步 AGENTS、developer README、API 接入文档和 roadmap。 |
| TP-04.02 | TP-04 | P0 | action | Yes | TP-04.01 | 完成验证并收口本地交付证据。 |

## Reading Order

1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md
