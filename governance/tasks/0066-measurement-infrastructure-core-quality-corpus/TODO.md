# Execution Checklist

[x] TP-01.01 | P0 | 读取现有 fixture、registry、local-ci、L4 smoke | Verify: `rg` / `sed` / JSON summary | Gate: 当前差距明确 | Parallelizable: Yes
[x] TP-02.01 | P0 | 新增 core quality corpus manifest | Verify: JSON syntax + gate | Gate: 5 个 corpus 分片可发现 | Parallelizable: No
[x] TP-02.02 | P0 | 新增 report diff policy | Verify: JSON syntax + policy assertions | Gate: 结构、隐私和体系隔离明确 | Parallelizable: No
[x] TP-03.01 | P0 | 扩容紫微匿名 samples | Verify: L4 golden smoke | Gate: 仅北京/测试样本 | Parallelizable: No
[x] TP-03.02 | P0 | 新增 core-quality-corpus gate | Verify: gate CLI | Gate: output JSON status=passed | Parallelizable: No
[x] TP-03.03 | P0 | 接入 registry/local-ci/runner | Verify: focused API/runner tests | Gate: required run 可发现 | Parallelizable: No
[x] TP-04.01 | P0 | 更新 tests、AGENTS、README、roadmap | Verify: focused tests + diff review | Gate: 文档不夸大 | Parallelizable: No
[x] TP-04.02 | P0 | quick local-ci 和本地交付证据 | Verify: local-ci summary + task validators | Gate: 本地 quick CI 通过 | Parallelizable: No
