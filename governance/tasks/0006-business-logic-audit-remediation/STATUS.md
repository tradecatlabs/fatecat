# Task Status
- Overall Status: `Done`

# Next Executable Leaves
- 无

# Task Package Status Table
| Node ID | Parent | Depth | Depends On | Ready | Status | Recent Evidence | Blocker | Unblock Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TP-01 | ROOT | 1 | - | No | Done | Wave 1 证据复现完成；TP-01.03 基线测试 45 passed。 | - | - |
| TP-01.01 | TP-01 | 2 | - | No | Done | git status、git diff --name-status、git ls-files --others 显示当前业务源码无 dirty diff；dirty 文件全部在 governance 下，0006 为本轮任务包。 | - | - |
| TP-01.02 | TP-01 | 2 | - | No | Done | rg 复现 fate-core 到 delivery 反向依赖；API 非默认选项返回 200；useTrueSolarTime=false 核心回显冲突；location.get 接受越界坐标；入口存在 Web/API/Bot 分流。 | - | - |
| TP-01.03 | TP-01 | 2 | TP-01.01, TP-01.02 | No | Done | .venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_web_html.py：45 passed in 10.57s。 | - | - |
| TP-02 | ROOT | 1 | TP-01.03 | No | Done | TP-02.01/TP-02.02/TP-02.03 均完成；fate-core 不再反向依赖交付服务源码路径。 | - | - |
| TP-02.01 | TP-02 | 2 | TP-01.03 | No | Done | rg 命中 support paths、ziwei_iztro sys.path、bazi_calculator extension imports 和 calculate_complete 动态加载；目标迁入 fate_core.adapters 兼容模块。 | - | - |
| TP-02.02 | TP-02 | 2 | TP-01.03, TP-02.01 | No | Done | 迁移 legacy integrations 到 fate_core.adapters.legacy_integrations；边界扫描返回空；fate-core tests 3 passed；API/Web 48 passed；compileall 通过。 | - | - |
| TP-02.03 | TP-02 | 2 | TP-01.03, TP-02.02 | No | Done | 新增 `tests/regression/test_architecture_boundaries.py`；pytest 1 passed；rg 旧路径 marker 返回空。 | - | - |
| TP-03 | ROOT | 1 | TP-01.03 | No | Done | TP-03.01-TP-03.04 均完成；未实现选项显式 422，true solar 回显一致，记录保留 raw/normalized options。 | - | - |
| TP-03.01 | TP-03 | 2 | TP-01.03 | No | Done | 新增 API 测试：unsupported business options 当前 200 而期望 422；useTrueSolarTime=false 当前 input.options 回显 true。 | - | - |
| TP-03.02 | TP-03 | 2 | TP-01.03, TP-03.01 | No | Done | `_validate_supported_bazi_options` 已拒绝未实现选项；focused API 测试 2 passed；完整 API/Web 48 passed。 | - | - |
| TP-03.03 | TP-03 | 2 | TP-01.03, TP-03.01 | No | Done | BaziCalculator input.options.useTrueSolarTime 改为请求值；focused true solar 测试 2 passed；完整 API/Web 48 passed。 | - | - |
| TP-03.04 | TP-03 | 2 | TP-01.03, TP-03.02, TP-03.03 | No | Done | 记录 `biz_data.input` 原始 options 与 `biz_data.normalizedOptions`；focused API 3 passed。 | - | - |
| TP-04 | ROOT | 1 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04 | No | Done | TP-04.01-TP-04.03 均完成；Web/API/Bot 通过 calculation_service 收敛，入口字段一致性回归通过。 | - | - |
| TP-04.01 | TP-04 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04 | No | Done | CONTEXT.md 已写入 Web/API/Bot 业务流、迁移目标和兼容策略；rg 扫描确认当前分流点。 | - | - |
| TP-04.02 | TP-04 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.01 | No | Done | 新增 `calculation_service.py` 统一 Web/API/Bot 计算编排；API/Web 49 passed；delivery api/bot smoke PASS。 | - | - |
| TP-04.03 | TP-04 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.02 | No | Done | 新增 `tests/regression/test_entrypoint_consistency.py`；focused 2 passed；API/Web/architecture 50 passed。 | - | - |
| TP-05 | ROOT | 1 | TP-01.03 | No | Done | TP-05.01/TP-05.02 均完成；非法坐标明确拒绝，合法边界坐标通过。 | - | - |
| TP-05.01 | TP-05 | 2 | TP-01.03 | No | Done | 新增 tests/regression/test_location.py 和 Web coordinate 测试；当前 5 个 location 越界用例未抛错、Web 未显示错误。 | - | - |
| TP-05.02 | TP-05 | 2 | TP-01.03, TP-05.01 | No | Done | `location._validate_coordinates` 拒绝越界经纬度；location/Web coordinate focused 测试 9 passed；完整 API/Web 48 passed。 | - | - |
| TP-06 | ROOT | 1 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02 | No | Done | TP-06.01/TP-06.02/TP-06.03 均完成；本地门禁、治理门禁、任务文档校验和 git diff hygiene 均通过。 | - | - |
| TP-06.01 | TP-06 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02 | No | Done | quick CI PASS；governance strict PASS；task docs PASS；debug note PASS。 | - | - |
| TP-06.02 | TP-06 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-06.01 | No | Done | REVIEW-0001 更新为 PASS WITH RESIDUAL RISKS；F-001 到 F-005 均 CLOSED；governance strict PASS。 | - | - |
| TP-06.03 | TP-06 | 2 | TP-02.01, TP-02.02, TP-02.03, TP-03.01, TP-03.02, TP-03.03, TP-03.04, TP-04.01, TP-04.02, TP-04.03, TP-05.01, TP-05.02, TP-06.02 | No | Done | git diff --check PASS；git status 已盘点，未发现运行态、secret 或未说明格式化；交付包可交给 auto-github 进行 commit/push。 | - | - |

# Blockers
- 无

# Runtime State
- Active workflow state: 任务树已完成；以 `TASK_PACKAGE_SET.json` / `TASK_EXECUTION_WAVE_PACKET.json` 和本 STATUS closeout 证据为准。
- Approval state: 未记录即视为未授权。
- Resume rule: 继续任务前重新读取当前 packet、Recent Evidence、Blockers、Runtime State。
- Stop condition: 迁移 adapter 后基础排盘或紫微报告无法通过现有 golden/API 回归。
- Stop condition: 发现非默认业务选项已有外部契约必须支持但当前实现无法证明正确。
- Stop condition: Bot 用户命令格式需要破坏性修改。
- Stop condition: 治理索引脚本继续批量改写 archive 文件且原因不清。
- TP-01.01: status=Done; verifier_context=自审
- TP-01.02: status=Done; verifier_context=自审
- TP-01.03: status=Done; verifier_context=自审
- TP-02.01: status=Done; verifier_context=自审
- TP-02.02: status=Done; verifier_context=自审
- TP-02.03: status=Done; verifier_context=自审
- TP-03.01: status=Done; verifier_context=自审
- TP-03.02: status=Done; verifier_context=自审
- TP-03.03: status=Done; verifier_context=自审
- TP-03.04: status=Done; verifier_context=自审
- TP-04.01: status=Done; verifier_context=自审
- TP-04.02: status=Done; verifier_context=自审
- TP-04.03: status=Done; verifier_context=自审
- TP-05.01: status=Done; verifier_context=自审
- TP-05.02: status=Done; verifier_context=自审
- TP-06.01: status=Done; verifier_context=自审
- TP-06.02: status=Done; verifier_context=自审
- TP-06.03: status=Done; verifier_context=自审
