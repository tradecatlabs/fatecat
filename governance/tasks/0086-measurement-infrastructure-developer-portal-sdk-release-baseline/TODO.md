# Execution Checklist

[x] TP-01.01 | P0 | 复核 0067 baseline、sandbox、examples、docs smoke 和 roadmap | Verify: inspected contracts/scripts/docs | Gate: target is release baseline, not public release | Parallelizable: Yes
[x] TP-02.01 | P0 | 设计 portal / SDK release / snapshot / no-overclaim contract | Verify: plan fields | Gate: no report body snapshot | Parallelizable: No
[x] TP-03.01 | P0 | 新增 developer portal、SDK release baseline、sandbox snapshot 和文档 | Verify: files exist | Gate: not_published and not_implemented boundaries | Parallelizable: No
[x] TP-04.01 | P0 | 新增 `developer-portal-gate.py/.sh` | Verify: gate smoke | Gate: externalPortalLive=false | Parallelizable: No
[x] TP-04.02 | P0 | 接入 local-ci、tests、AGENTS、docs 和 changelog | Verify: grep/tests | Gate: document-drift closed | Parallelizable: No
[x] TP-05.01 | P0 | 运行 syntax、gate、focused pytest 和 quick CI | Verify: commands pass | Gate: no local failure | Parallelizable: No
[x] TP-05.02 | P0 | 明确提交、推送和远端 CI 由外层交付流汇报 | Verify: task snapshot does not pre-claim remote CI | Gate: no remote CI overclaim before commit exists | Parallelizable: No
