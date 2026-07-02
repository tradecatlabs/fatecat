# Execution Checklist

[x] TP-01.01 | P0 | 复核现有 developer docs、sandbox fixture、OpenAPI export、local-ci 和 metadata | Verify: rg/sed | Gate: 差距明确 | Parallelizable: No
[x] TP-02.01 | P0 | 新增 developer platform contract | Verify: json tool + gate | Gate: SDK package baseline 不声明发布 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 sandbox token contract | Verify: json tool + gate | Gate: contract-only/not implemented | Parallelizable: No
[x] TP-02.03 | P0 | 新增 API changelog contract 和 human changelog | Verify: json tool + gate | Gate: 0067 entry 可追溯 | Parallelizable: No
[x] TP-03.01 | P0 | 新增 developer-platform-gate | Verify: gate CLI | Gate: summary status passed | Parallelizable: No
[x] TP-03.02 | P0 | 接入 /metadata、local-ci 和 summary artifact | Verify: API metadata test + local-ci | Gate: artifact 可发现 | Parallelizable: No
[x] TP-03.03 | P0 | 新增 developer platform 回归测试 | Verify: focused pytest | Gate: no SDK/token overclaim | Parallelizable: Yes
[x] TP-04.01 | P0 | 同步 AGENTS、developer README、API 接入文档和 roadmap | Verify: diff review | Gate: 文档不夸大 | Parallelizable: Yes
[x] TP-04.02 | P0 | 运行验证并收口本地交付证据 | Verify: quick local-ci | Gate: 本地 quick CI 通过 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
