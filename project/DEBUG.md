# Debug Record

## Bug

- 标题：`weakStrong` 强弱口径退化为二档，导致历史样本被误判为“全部偏强”
- 症状：安装后的排盘结果里，身强弱不再输出五档（`身弱 / 中和偏弱 / 中和 / 中和偏强 / 身强`），而是只剩 `身强 / 身弱`；用户反馈实际结果明显偏向“全部身强”
- 首次发现位置 / 时间：线上安装包反馈，2026-04-20

## Environment

- 仓库 / 模块：`fatecat/project/modules/telegram`
- 关键文件：`src/bazi_calculator.py`
- 上游参照：`project/assets/vendor/github/bazi-1-master/bazi.py`

## Reproduction

1. 用 `BaziCalculator(...)._calc_wuxing_scores()` 直接计算四柱五行分数
2. 观察 `weakStrong`
3. 对 2013-01-01 09:19（北京）样本，旧实现输出 `身强`

## Observations

- O1: 当前 `_calc_wuxing_scores()` 只返回 `\"身强\" if not weak else \"身弱\"`，实现上已经不可能产出五档
- O2: `models.py` 的 `DayMaster.strength` 历史上设计为五档口径，说明展示层原本就期待细粒度强弱
- O3: 上游 `bazi-1` 同时给出 `weak` 布尔值和 `strong` 原始分数；README 明确标注“通常 >29 为强，需要参考月份、坐支等”
- O4: 历史故障样本 `2013-01-01 09:19` 的 raw `strongScore` 为 `25`，旧实现却因为存在一个 `帝` 直接落成 `身强`

## Hypotheses

### H1: （ROOT HYPOTHESIS）
- Supports: 现实现把上游原始强弱信息压扁成二档，展示层因此失去五档能力
- Conflicts: 无
- Test: 恢复上游 `strong` 原始分数，并基于上游经验线做五档归一

### H2:
- Supports: 只看 `weak` 布尔值会把边界样本误推到“身强”
- Conflicts: 无
- Test: 用 `strongScore=25` 的历史样本回归验证，修复后应落到 `中和偏弱`

## Experiments

### E1
- Hypothesis: 当前实现已经退化成二档输出
- Change: 直接检查 `project/modules/telegram/src/bazi_calculator.py`
- Expected: `weakStrong` 只会返回 `身强/身弱`
- Result: 确认存在
- Verdict: confirmed
- Revert: 无

### E2
- Hypothesis: 历史故障样本的 raw score 不支持“身强”
- Change: 用内部方法直算 2013-01-01 09:19（北京）样本
- Expected: `strongScore` 落在 29 以下
- Result: `strongScore = 25`，旧实现仍输出 `身强`
- Verdict: confirmed
- Revert: 无

### E3
- Hypothesis: 只按 `strongScore` 做五档映射，会与上游 `weak` 布尔值冲突
- Change: 抽查 2001-01-01 12:00（北京）样本
- Expected: 若 `weak=True`，标签不应落入偏强侧
- Result: 样本出现 `weak=True` 且 `strongScore = 32` 的组合，说明“只看分数”会导致标签与上游原始判定打架
- Verdict: confirmed
- Revert: 无

## Root Cause

- 根因不是用户安装问题，也不是上游 `bazi-1` 自身故障，而是 FateCat 本地胶水层把上游强弱结果退化成了二档展示：
  - 保留了 `weak` 布尔判定
  - 丢失了上游 `strong` 原始分数
  - 于是所有边界样本都会被粗暴压到 `身强/身弱`

## Fix

- 在 `_calc_wuxing_scores()` 中补回上游 `strongScore`
- 保留上游 `weak` 原始布尔值，作为原始诊断字段输出
- 五档映射改为“先尊重 `weak`，再用 `strongScore` 细分”：
  - `weak=True`: `<=20 -> 身弱`，`21-28 -> 中和偏弱`，`>=29 -> 中和`
  - `weak=False`: `<=25 -> 中和偏弱`，`26-33 -> 中和`，`34-37 -> 中和偏强`，`>=38 -> 身强`

## Regression Evidence

- 新增测试：`project/tests/test_strength_mapping.py`
- 验证点：
  - 五档阈值边界可用
  - 历史故障样本 `2013-01-01 09:19` 回归到 `中和偏弱`
  - `weak=True` 的边界样本不会被错误落到偏强侧

## Bug

- 标题：iztro 原生算法模块入口缺失
- 症状：Bot 排盘时报错 `ziwei failed: iztro原生算法执行失败`
- 首次发现位置 / 时间：`/paipan` 链路，2026-04-15

## Environment

- 仓库 / 模块：`fatecat/modules/telegram`
- 运行环境：Linux + Python `.venv` + Node `v22.12.0`
- 依赖 / 版本：`assets/vendor/github/iztro-main`
- 配置差异：Python 依赖已安装，Node vendor 依赖未安装

## Reproduction

1. 启动 Bot
2. 发送 `/paipan`
3. 进入紫微斗数分支时抛出 `Cannot find module .../iztro-main/lib/index.js`

## Observations

- O1: `assets/vendor/github/iztro-main/package.json` 存在，且 `main` 指向 `lib/index.js`
- O2: 仓库中只有 `src/index.ts`，没有 `lib/index.js`
- O3: `assets/vendor/github/iztro-main/node_modules` 不存在

## Hypotheses

### H1: （ROOT HYPOTHESIS）
- Supports: vendor 仓库只有源码快照，未执行 `npm install` / `npm run build`
- Conflicts: 无
- Test: 在 Python 集成层先检测 `node_modules` 与入口文件，不满足则自动 install/build

### H2:
- Supports: 代码把入口路径写死为 `lib/index.js`
- Conflicts: `package.json.main` 本身也是 `lib/index.js`，说明单纯改字符串不是根因
- Test: 改为统一从 `package.json.main` 解析入口

### H3:
- Supports: 即使后续有构建产物，没有 `node_modules` 仍可能在 require 时失败
- Conflicts: 无
- Test: 把“入口存在”和“依赖已安装”一起作为 ready 条件

## Experiments

### E1
- Hypothesis: 缺少 Node 依赖与构建产物是直接根因
- Change: 扫描 `iztro-main` 文件结构与 `package.json`
- Expected: 只有 `src/`，没有 `lib/`，且没有 `node_modules`
- Result: 观测符合预期
- Verdict: confirmed
- Revert: 无

## Root Cause

- FateCat 在调用 `iztro` 时默认假设 vendor 仓库已经完成 Node 依赖安装和 TypeScript 构建，但当前环境只有源码快照，缺少 `node_modules` 和 `lib/index.js`，导致运行时 `MODULE_NOT_FOUND`

## Fix

- 按 `package.json.main` 解析 `iztro` 入口，去掉硬编码字符串假设
- 在调用前自动检查 `node_modules` 与入口文件
- 缺依赖时执行 `npm install --no-fund --no-audit`
- 缺入口且存在 `build` 脚本时执行 `npm run build`
- 临时 JS 文件改用 `NamedTemporaryFile`，避免固定 `/tmp/native_iztro.js`

## Regression Evidence

- 测试：新增 `modules/telegram/tests/test_fortel_ziwei_integration.py`
- 结果：覆盖入口解析与 install/build 准备逻辑
- 备注：后续再跑一次真实 `FortelZiweiCalculator` 调用确认 Node 侧可执行

## Bug

- 标题：skill 化后生产门禁发现 pure/API/pytest 多链路契约断点
- 症状：
  - `pure-analysis` 文档样例传 `gender:"男"` 时，输出 `genderCn` 被误判为 `坤造(女)`
  - `/api/v1/bazi/calculate` 返回 `success:false`，Pydantic 响应模型与真实计算结果不匹配
  - 带 `user_id` 的 API 保存记录调用参数与 `db.save_record()` 签名不一致
  - 全量 pytest 在 `modules/telegram/tests/test_xingming.py` 收集阶段找不到 `src`
- 首次发现位置 / 时间：skill 生产化审查，2026-05-05

## Environment

- 仓库 / 模块：`fatecat/project`
- 关键入口：`scripts/preflight.sh`、`fatecat pure-analysis`、FastAPI `/api/v1/bazi/*`、pytest

## Reproduction

1. 执行 `bash scripts/preflight.sh --mode pure --bootstrap --smoke --output-file /tmp/fatecat-analysis-sample.json --pretty`
2. 观察 `/tmp/fatecat-analysis-sample.json` 中 `data.input.gender == "男"` 但 `data.meta.genderCn == "坤造(女)"`
3. 用 FastAPI TestClient 调用 `/api/v1/bazi/calculate`，返回 `success:false` 和多项模型校验错误
4. 执行 `cd project && .venv/bin/python -m pytest -q`，收集阶段出现 `ModuleNotFoundError: No module named 'src'`

## Observations

- O1: CLI 只做字段名归一，未把中文性别归一为 `male/female`
- O2: `fate_core` provider 和遗留 `BaziCalculator` 均以 `gender == "male"` 判断乾造与顺逆行
- O3: API `BaziData` 模型要求 `fiveElements.*.stems/branches` 和 `majorFortune.pillars.*.year`，但真实结果提供 `items` 和 `startYear`
- O4: `main.py` 保存记录时只传 3 个位置参数，`db.save_record()` 需要出生日期、时间、性别等必填字段
- O5: pytest 配置只加入了 `modules/telegram/src`，而 `test_xingming.py` 使用包路径 `src.xingming`

## Hypotheses

### H1: （ROOT HYPOTHESIS）
- Supports: 多个断点都来自 skill 化后公开契约与遗留源码内部约定没有统一
- Conflicts: pure-analysis 主计算本身可运行，说明不是底层 vendor 全面失效
- Test: 在用例/API 边界做输入与响应装配归一，再跑 pure smoke、API 契约测试和全量 pytest

### H2:
- Supports: API `/pure-analysis` 成功，而 `/calculate` 失败，说明 full calculate 的响应模型单独过期
- Conflicts: 无
- Test: 让 full calculate 先适配真实输出结构，避免 Pydantic 模型拒绝已存在的合法计算结果

### H3:
- Supports: 全量 pytest import 错误只出现在测试收集阶段，和业务运行无关
- Conflicts: 无
- Test: 补齐 `modules/telegram` 包根到 `sys.path`

## Experiments

### E1
- Hypothesis: `gender:"男"` 未归一导致乾坤误判
- Change: 抽查 `cli.py`、`providers/runtime.py`、`providers/base_chart.py`
- Expected: CLI 保留中文，provider 只认 `male`
- Result: 确认
- Verdict: confirmed
- Revert: 无

### E2
- Hypothesis: `/api/v1/bazi/calculate` 是响应模型与真实结果错位
- Change: 用 TestClient 调用真实 endpoint
- Expected: 出现 Pydantic 校验错误
- Result: 确认 `fiveElements`、`majorFortune`、`voidBranches` 不匹配
- Verdict: confirmed
- Revert: 无

## Root Cause

- skill 外壳已经能包装 pure-analysis，但原完整源码的 API/Bot/测试契约没有同步收敛；公开入口使用的人类友好输入、Pydantic 响应模型和遗留计算器内部结构之间缺少统一适配层。

## Fix

- 在 pure-analysis 用例边界把性别统一归一为 `male/female`
- API full calculate 响应装配时兼容真实 `fiveElements.items`、`majorFortune.startYear`、`voidInfo` 结构
- 修正 API 保存记录调用，显式传入 `db.save_record()` 所需字段
- 测试配置补充 `modules/telegram` 包根，支持 `src.*` 导入
- 增加 CLI、usecase、API 契约回归测试

## Regression Evidence

- 已通过：
  - `cd project && .venv/bin/python -m pytest -q`：24 passed
  - `bash scripts/preflight.sh --mode pure --bootstrap --smoke --output-file /tmp/fatecat-after-fix-preflight.json --pretty`：通过，`genderCn == 乾造(男)`
  - `bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-perfect`：通过，包含源码仓库 smoke、全量 pytest、delivery api smoke、导出 lite skill strict 校验与导出包 pure smoke
  - `RUFF_CACHE_DIR=/tmp/fatecat-ruff-cache project/.venv/bin/ruff check <本轮改动文件>`：通过

## Bug

- 标题：生产化复查发现发布门禁与旧脚本仍存在旁路
- 症状：
  - `scripts/acceptance.sh` 默认只验证 API delivery smoke，未把 Bot dry-run 纳入发布门禁
  - `project/scripts/setup/*`、`project/assets/deploy/pack.sh`、`project/scripts/start_all.sh` 等历史入口仍绕到 `modules/telegram/start.py` 或只装 `modules/telegram/requirements.txt`
  - `project/scripts/setup/setup_external_env.sh` 会在 vendor 目录缺少工程文件时生成 `package.json` 或执行 `cargo init`
  - `project/scripts/generate_bazi.sh` 绕过统一 CLI，且 CLI 直接参数模式在空 stdin 的非交互执行中会误解析空 JSON
- 首次发现位置 / 时间：skill 生产化复查，2026-05-05

## Root Cause

- skill 根目录已经形成统一入口，但原项目脚本仍按旧应用仓库假设运行；发布门禁没有把“API + Bot + 导出包”作为一个整体契约，导致人类安装后仍可能走到未验证路径。

## Fix

- `acceptance.sh` 默认 `--delivery-target both`，同时执行 API smoke 与 Bot dry-run，并继续验证导出后的 lite skill 包
- 项目级启动、部署、测试、排盘脚本统一改走 `pyproject.toml` 生成的 `fatecat` CLI
- vendor 下载与外部环境脚本改为显式授权/只构建既有项目，不再自动生成替代 vendor 源码
- 修复 CLI 空 stdin 误解析问题，保留 `--birth-datetime` 等直接参数模式
- 更新根 README、SKILL、commands、ops-pack 与项目脚本说明，明确生产真相源

## Regression Evidence

- 已通过：
  - `project/scripts/build_all.sh`：通过，验证 `fatecat` CLI
  - `project/scripts/generate_bazi.sh "2004-02-21" "19:30" "男" "辽宁省大连市" 121.6 38.9 "张三"`：通过，生成 JSON 后已清理临时输出
  - `project/scripts/test_all.sh`：25 passed
  - `bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-both-final`：通过，包含 strict skill 校验、pure smoke、25 项 pytest、API smoke、Bot dry-run、lite 导出包 strict 校验与导出包 pure smoke
  - `bash scripts/export-runtime.sh --output-parent /tmp/fatecat-full-export-final --mode full` + strict validate + full 导出包 pure smoke：通过
  - `RUFF_CACHE_DIR=/tmp/fatecat-ruff-cache project/.venv/bin/ruff check <本轮 Python 改动文件>`：通过

## Bug

- 标题：完美化收口发现静态门禁、架构边界与过度承诺文案未固化
- 症状：
  - 全仓 `ruff check project` 会扫描 `assets/vendor` 第三方快照，暴露 Python2 语法和外部库风格问题
  - 一方代码仍有导入排序、裸 `except`、异常链、闭包捕获循环变量等静态问题
  - `fate_core/providers` 仍直接导入 legacy `bazi_calculator` / `utils.timezone`
  - mypy 未形成可复用门禁，`fate_core` 没有 `py.typed` 标记
  - 历史报告/测试文案仍有“最完整 / 95%+ / 无任何阉割”等过度承诺
- 首次发现位置 / 时间：提交推送前完美化收口，2026-05-05

## Root Cause

- skill 化后的生产真相源已经收敛，但静态质量门禁没有固化进 acceptance；legacy 适配边界只停留在文档约束，部分 provider 仍直接接触遗留模块；历史营销文案未按“已验证能力 / legacy 兼容 / 研究素材”分层。

## Fix

- `project/pyproject.toml` 配置 ruff 排除 vendor/runtime/output，并加入 `mypy_path` 与 legacy import override
- 使用 ruff 修复并格式化一方 Python 代码，当前 `ruff check project` 与 `ruff format --check project` 均清零
- `fate_core` 增加 `py.typed`，并让 `fate_core.adapters` 成为唯一 legacy calculator 入口
- `acceptance.sh` 默认加入 ruff、format 与 `fate_core` mypy 门禁
- 历史报告和测试输出改为 legacy/当前字段口径，删除过度承诺表述

## Regression Evidence

- 已通过：
  - `bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-perfect-push`：通过，包含 strict skill、pure smoke、25 项 pytest、ruff、format、`fate_core` mypy、API smoke、Bot dry-run、lite 导出包 strict 校验与导出包 pure smoke
  - `bash scripts/export-runtime.sh --output-parent /tmp/fatecat-full-export-perfect-push --mode full` + strict validate + full 导出包 pure smoke：通过
  - `project/scripts/download_libs.sh` 默认拒绝写 vendor：通过
  - `git diff --check`：通过
