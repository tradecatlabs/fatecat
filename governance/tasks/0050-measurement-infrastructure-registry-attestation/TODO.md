# Execution Checklist

[x] TP-01.01 | P0 | 复核 workflow、release gate 和 `actions/attest@v4` 官方用法 | Verify: file inspection and gh api | Gate: 不猜 action 参数 | Parallelizable: Yes
[x] TP-02.01 | P0 | 修改 container workflow，增加 GHCR digest、release artifact upload、attestation 和 verify | Verify: workflow regression test | Gate: push_image=false 不发布 | Parallelizable: No
[x] TP-03.01 | P0 | 增加测试和 public release policy 断言 | Verify: pytest + shell gate | Gate: workflow 退化时失败 | Parallelizable: No
[x] TP-03.02 | P0 | 同步 release gate、registry、AGENTS、操作文档和 roadmap | Verify: rg and targeted tests | Gate: 不把本地 baseline 写成远端证明 | Parallelizable: No
[x] TP-04.01 | P0 | 运行本地校验、提交推送并触发远端 workflow | Verify: local commands and GitHub Actions URL | Gate: 当前 commit 证据可追溯 | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`。
- 不允许出现无归属 TODO。
