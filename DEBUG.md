# DEBUG.md - bootstrap build isolation network failure

## 2026-07-04 CI follow-up: runtime proof registry literal drift

### Bug

GitHub Actions Acceptance run `28680656983` failed on commit `77d39ec30d086386f0c0018e5de6efd282c0686b` in `tests/regression/test_capability_protocol.py::test_delivery_surface_schema_and_registry_define_same_source_boundaries`.

Observed failure excerpt:

```text
E   AssertionError: assert 'runtime_proof_pack_external_pending' == 'multi_replica_runtime_contract_baseline'
- multi_replica_runtime_contract_baseline
+ runtime_proof_pack_external_pending
```

Container run `28680658235` for the same commit passed, including build, smoke, GHCR push and attestation verify.

### Observations

- `contracts/fate/delivery/registry.json` intentionally changed `runtimeBackendRegistry.currentProductionEligibility` to `runtime_proof_pack_external_pending`.
- Local quick CI passed because it runs the focused regression set and does not include the full `test_capability_protocol.py` file.
- Remote Acceptance runs full pytest and caught the remaining hard-coded old registry literal.
- The runtime proof gate itself passed locally and in quick CI with `runtimeProofStatus=external_connectivity_pending` and `shipGate=blocked`.

### Hypotheses

1. The failure is a stale contract test literal, not a runtime proof implementation failure.
   - Supports: CI diff shows only expected-vs-actual literal mismatch.
   - Test: update the test expectation and rerun the failing test.
2. The registry value is wrong and should remain `multi_replica_runtime_contract_baseline`.
   - Conflicts: W2 intentionally promotes the top-level eligibility state to runtime proof pack external pending, while multi-replica remains a child gate.
   - Test: inspect `contracts/fate/delivery/registry.json` and `runtime-proof-pack.json`.
3. Quick CI is insufficient for this class of drift.
   - Supports: quick CI passed 289 focused tests; remote full pytest collected 472 and failed on a file outside the quick subset.
   - Test: run the failing full-regression test locally.

### Root Cause

The W2 runtime proof pack changed the delivery registry source-of-truth state, but the full acceptance contract test still asserted the previous multi-replica-only eligibility literal.

### Fix

Update `tests/regression/test_capability_protocol.py` to assert `runtime_proof_pack_external_pending`.

### Regression Evidence

```bash
.venv/bin/python -m pytest -q tests/regression/test_capability_protocol.py::test_delivery_surface_schema_and_registry_define_same_source_boundaries
bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-runtime-proof-fix
```

Result:

- Targeted failing test passed: `1 passed`.
- Local acceptance completed: `471 passed, 1 skipped`, ruff, mypy, API/Bot delivery smoke, lite export hygiene and exported pure preflight all passed.
- Evidence directory: `/tmp/fatecat-acceptance-runtime-proof-fix`.

## Bug

`bash scripts/acceptance.sh --with-dev --with-mingli-bench --output /tmp/fatecat-acceptance-full-test` 在 `delivery-smoke` 的 `preflight --bootstrap` 阶段失败。

## Environment

- Repo: `/home/lenovo/.projects/fatecat`
- Runtime root: `/home/lenovo/.projects/fatecat`
- Python: `.venv/bin/python`
- Failure phase: `pip install -e .` during bootstrap called by delivery preflight

## Reproduction

Command:

```bash
bash scripts/acceptance.sh --with-dev --with-mingli-bench --output /tmp/fatecat-acceptance-full-test
```

Observed failure excerpt:

```text
ERROR: Could not find a version that satisfies the requirement hatchling
ERROR: Failed to build 'file:///home/lenovo/.projects/fatecat' when installing build dependencies
```

## Observations

- `pyproject.toml` uses `build-backend = "hatchling.build"`.
- `hatchling` editable installs require `editables` when build isolation is disabled.
- The active `.venv` did not have `hatchling` installed before the failed delivery smoke bootstrap.
- `requirements.txt`, `requirements-dev.txt`, and `requirements.lock.txt` did not declare `hatchling`.
- `pip install -e .` used build isolation, so pip tried to fetch `hatchling` from PyPI inside a temporary build environment.
- Network access to PyPI returned `ReadTimeoutError` / `SSLEOFError`, making the release gate flaky.

## Principle Gate Evidence

- target end state: bootstrap installs declared build/runtime requirements before local editable install.
- real constraints: local CI/CD must work in fresh venvs and offline-prone developer networks.
- inertia constraints: older venvs can hide missing build tools and make failures look transient.
- kill list: nested build backend fetches during delivery smoke and acceptance gates.
- proof point: bootstrap plus acceptance passes from a rebuilt `.venv`.
- falsifier: a fresh venv still fetches build backends during local project install.
- migration slice: seed build tools, install dependencies normally, then install FateCat with `--no-deps`.

## Hypotheses

1. Build isolation is the root cause because editable install fetches build backend from PyPI during test execution.
   - Supports: failure is specifically inside "installing build dependencies" for `hatchling`.
   - Test: install build-system requirements in the venv first and run editable install with `--no-build-isolation`.
2. The failure is a transient PyPI outage only.
   - Supports: error includes network timeout and SSL EOF.
   - Conflicts: release gate should not require nested build dependency fetches once bootstrap has prepared the venv.
   - Test: rerun without changing bootstrap would likely be flaky rather than structurally fixed.
3. The package metadata is missing build backend declaration.
   - Conflicts: `pyproject.toml` correctly declares `hatchling`.
   - Test: inspect `pyproject.toml`.

## Root Cause

`bootstrap.sh` relied on PEP 517 build isolation for editable installs, but did not preinstall the declared build backend into the managed venv. This made delivery smoke depend on a nested online fetch of `hatchling`.

## Fix

- Install `pyproject.toml` build-system requirements into `.venv` during bootstrap.
- Use `pip install --no-build-isolation -e .` once build requirements are present.
- Add `hatchling` and `editables` to build-system/dev dependency declarations so developer environments expose the packaging backend explicitly.

## Regression Evidence

```bash
bash scripts/bootstrap.sh --with-dev
bash scripts/acceptance.sh --with-dev --with-mingli-bench --output /tmp/fatecat-acceptance-full-test
```

Result:

- `bootstrap.sh --with-dev` completed and `pip show hatchling editables` reported installed packages.
- The former failing path passed: `bash scripts/delivery-smoke.sh --target api --response-file /tmp/fatecat-delivery-api-after-build-fix.json`.
- Full acceptance with MingLi-Bench completed: `/tmp/fatecat-acceptance-full-test`.

## 2026-06-11 CI follow-up: setuptools.build_meta unavailable

### Bug

GitHub Actions run `27320894427` failed during `bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-ci-acceptance`.

Observed failure excerpt:

```text
pip._vendor.pyproject_hooks._impl.BackendUnavailable: Cannot import 'setuptools.build_meta'
```

### Observations

- The failure happened in bootstrap before tests, immediately after CI created a fresh Python 3.12 venv.
- A clean local temp venv reproduced the environment property: `importlib.util.find_spec("setuptools.build_meta")` raised `ModuleNotFoundError: No module named 'setuptools'`.
- `bootstrap.sh` installed the project with `pip install --no-build-isolation -e .`, which also makes source builds in that install invocation depend on build backends already present in the venv.
- Local acceptance did not expose this because the existing local `.venv` already had `setuptools`.

### Hypotheses

1. The root cause is that project editable install used `--no-build-isolation` while still resolving dependencies.
   - Supports: CI fresh venv lacks `setuptools`, and the failure is `setuptools.build_meta` during dependency preparation.
   - Test: install dependencies in a normal pip step first, then install only the project editable with `--no-deps --no-build-isolation`.
2. The root cause is only a transient PyPI/network issue.
   - Conflicts: the reported backend is missing locally in a clean venv; this is structural for fresh Python 3.12 environments.
3. The root cause is an invalid project build backend.
   - Conflicts: the project backend is `hatchling.build`; the missing backend is `setuptools.build_meta` from a third-party source build.

### Root Cause

`bootstrap.sh` disabled build isolation for the project editable install before separating dependency installation. In a fresh CI venv, third-party source distributions that require `setuptools.build_meta` could not build because `setuptools` was not present in the active environment.

### Fix

- Upgrade `pip`, `setuptools`, and `wheel` as bootstrap seed tooling.
- Install `requirements.txt` or `requirements-dev.txt` in a normal pip dependency step.
- Install the local project editable with `--no-build-isolation --no-deps`, limiting no-build-isolation to FateCat itself.

### Regression Evidence

Completed:

```bash
bash scripts/bootstrap.sh --with-dev
bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-ci-fix
```

Result:

- Fresh local `.venv` rebuild completed with the updated bootstrap flow.
- CI-parity acceptance passed end to end: 112 pytest tests, ruff, mypy, API/Bot smoke, export smoke, exported hygiene and strict validation.
- Evidence directory: `/tmp/fatecat-acceptance-ci-fix`.

## 2026-06-11 CI follow-up: iztro vendor hash drift

### Bug

After the bootstrap fix, local CI-parity acceptance reached `vendor-health` and failed:

```text
iztro sha256 mismatch:
expected=195f863dd4c66f3925a757ea0c23255803ac0a27aa831500bafefd87064370be
actual=3817f93a677e0c63b353a94fa7275199f21582a36397edc2f90685b58aae9325
```

### Observations

- `tools/reference-repos/github/iztro-main` had no working-tree diff after migration.
- The old manifest at `HEAD^:scripts/project/assets/vendor/vendor_sources.json` recorded `3817f93a677e0c63b353a94fa7275199f21582a36397edc2f90685b58aae9325`.
- The migration diff changed only the manifest value from `3817f93...` to `195f863...`.
- File count before and after migration was identical for the iztro snapshot: 338 files.

### Root Cause

The iztro vendor snapshot was migrated byte-for-byte, but `vendor_sources.json` regressed to an older snapshot hash during the path migration.

### Fix

Restore the iztro `snapshotSha256` to the pre-migration verified value `3817f93a677e0c63b353a94fa7275199f21582a36397edc2f90685b58aae9325`.

### Regression Evidence

Completed:

```bash
bash scripts/vendor-health.sh
bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-acceptance-ci-fix
```

Result:

- `vendor-health` passed with `required=5 optionalFutureFeatures=10 hashed=15 licenseAuditRequired=5`.
- The same CI-parity acceptance passed end to end after the manifest correction.

## 2026-06-15 production audit follow-up: false readiness claims and false-green tests

### Bug

生产级审计发现 3 类阻塞问题：

- `system_optimization.py` 声称 GraphQL、WebSocket、batch、测试覆盖率和 `readyForProduction=True`，但 `/graphql`、`/ws`、`/api/v1/batch` 实测均为 404。
- `test_all_features.py`、`test_complete_integration.py`、`test_extended.py` 捕获计算异常后 `return`，导致 `dantalion-core` 缺构建时报错仍显示 pytest passed。
- API 出生日期格式错误会在多个端点变成 500；`/api/v1/bazi/calculate` 还会以 HTTP 200 返回 `success=false`。

### Reproduction

```bash
.venv/bin/python -m pytest domains/experience-delivery/services/fatecat-delivery/tests/test_all_features.py domains/experience-delivery/services/fatecat-delivery/tests/test_complete_integration.py domains/experience-delivery/services/fatecat-delivery/tests/test_extended.py -q -s
PYTHONPATH=domains/experience-delivery/services/fatecat-delivery/src:domains/fate-analysis/services/fate-core/src .venv/bin/python - <<'PY'
from fastapi.testclient import TestClient
from main import app
payload = {
    "name": "bad",
    "gender": "male",
    "birthDate": "bad-date",
    "birthTime": "08:00:00",
    "birthPlace": {"name": "北京市", "longitude": 116.4074, "latitude": 39.9042, "timezone": "Asia/Shanghai"},
    "options": {"useTrueSolarTime": True, "daylightSaving": "auto", "midnightMode": "early", "calendarType": "solar"},
}
client = TestClient(app, raise_server_exceptions=False)
for path in ["/api/v1/bazi/simple", "/api/v1/bazi/pure-analysis", "/api/v1/bazi/calculate", "/api/v1/report/markdown"]:
    r = client.post(path, json=payload)
    print(path, r.status_code, r.json().get("success"), r.json().get("error"))
PY
```

Observed:

- 3 个 legacy 测试打印 `dantalion-core 未构建（缺少 dist/index.js）`，但 pytest 显示 `3 passed`。
- 非法日期触发：`/simple` 500、`/pure-analysis` 500、`/calculate` 200 + `success=false`、`/report/markdown` 500。

### Hypotheses

1. 形式工程声明来自 `system_optimization.py` 的硬编码报告，而非 FastAPI 路由或测试产物。
   - Supports: 诊断报告内直接硬编码 enabled 和覆盖率；真实路由 404。
2. 假绿来自测试吞异常。
   - Supports: 三个测试文件的 `except Exception: print(...); return`。
3. 500/200 错误语义来自 `BaziRequest` 没有日期时间校验，且 endpoint 直接 catch generic exception。
   - Supports: 栈在 `datetime.strptime`；`calculate_bazi` generic except 返回 `BaziResponse(success=False)`。

### Root Cause

仓库把“未来/诊断/legacy 全量链路”混进生产质量口径：未实现能力被硬编码为 enabled，测试失败被打印后吞掉，API 输入边界靠内部解析而不是公开请求模型。

### Fix

- 将 `system_optimization.py` 收缩为真实单进程诊断报告，未实现路由只列入 `plannedNotAdvertisedAsEnabled`，不再伪造覆盖率或生产 ready。
- `BaziRequest` 增加日期、时间、时区校验；`_parse_bazi_request` 增加 422 兜底；内部计算失败改为 HTTP 500。
- 假绿测试改为标准生产报告链路，失败时 `pytest.fail()`，输出文件改到 `tmp_path`。
- Bot 本地补发队列改成本地 outbox：稳定任务 ID、重复入队去重、原子保存、成功 ACK 删除。
- `/metrics` 增加 `fatecat_bot_queue_scope_info{backend="memory",scope="single_process"}`，明确单实例语义。

### Regression Evidence

Required before close:

```bash
.venv/bin/python -m pytest domains/experience-delivery/services/fatecat-delivery/tests/test_all_features.py domains/experience-delivery/services/fatecat-delivery/tests/test_complete_integration.py domains/experience-delivery/services/fatecat-delivery/tests/test_extended.py domains/experience-delivery/services/fatecat-delivery/tests/test_calculator.py domains/experience-delivery/services/fatecat-delivery/tests/test_bot_send_queue.py tests/regression/test_api_contracts.py tests/regression/test_mingli_bench_gate.py
bash scripts/local-ci.sh --profile quick
```

## 2026-06-15 CI follow-up: production env example ignored

### Bug

GitHub Actions run `27504699378` failed in `bash scripts/acceptance.sh --with-dev --output /tmp/fatecat-ci-acceptance`.

Observed failure excerpt:

```text
structure gate failed:
  - missing container release file: infra/environments/production/.env.production.example
```

### Observations

- Local `bash scripts/check-structure.sh` passed before push.
- `infra/environments/production/.env.production.example` existed locally, but was not present in the pushed commit.
- `git check-ignore -v infra/environments/production/.env.production.example` reported `.gitignore:29:.env.*`.
- `.gitignore` allowed `!.env.example` and `!*env.example`, but the latter did not unignore the dotted basename `.env.production.example`.
- The container workflow for the same commit succeeded and pushed the main GHCR image, so the failure was isolated to acceptance structure validation.

### Hypotheses

1. The production env example was ignored by `.gitignore` and therefore omitted from the commit.
   - Supports: `git check-ignore -v` points at `.env.*`.
   - Test: add an explicit unignore rule for `.env.*.example` and force the file into Git status.
2. The structure gate path is wrong.
   - Conflicts: the same path exists locally and is the intended production template path.
   - Test: keep the structure gate unchanged and make the file tracked.
3. CI checkout lost the file because of export or sparse checkout behavior.
   - Conflicts: Actions checkout is a normal repository checkout, and the file was not in the commit.
   - Test: inspect pushed tree / Git status after unignore.

### Root Cause

The production `.env.production.example` template was a required tracked template, but `.gitignore`'s `.env.*` rule ignored it. Local validation passed because the ignored file existed in the working tree; CI failed because ignored untracked files are not checked out.

### Fix

- Add explicit `.gitignore` exception `!.env.*.example`.
- Track `infra/environments/production/.env.production.example`.

### Regression Evidence

Required before close:

```bash
git check-ignore -v infra/environments/production/.env.production.example || true
git ls-files infra/environments/production/.env.production.example
bash scripts/check-structure.sh
```

## 2026-06-15 Web report follow-up: workbench contract and report order drift

### Bug

本地八字/紫微 Web 合同测试发现工作台 DOM 合同漂移：测试期望服务端输出 `<section id="bazi-workbench">` 和 `<section id="ziwei-workbench">`，实际页面只输出 `<h2 id="workbench">...工作台</h2>`。同时右上报告面板先输出工作台，再输出 Markdown 报告，和“报告区域优先展示生成结果”的页面契约不一致。

### Observations

- `/web` 生成结果页仍能正常返回 200，八字计算与 API 能力未失败。
- `tests/regression/test_bazi_ziwei_benchmark_hardening.py::test_web_workbench_is_backend_structured_and_keeps_privacy` 在 `<section id="bazi-workbench">` 断言处失败。
- `web_ui._render_report()` 将 `_render_workbench(result)` 放在 Markdown 输出前。
- `web_ui._render_bazi_workbench()` 与 `_render_ziwei_workbench()` 只保留通用 `id="workbench"` 标题，缺少体系级 section 锚点。

### Hypotheses

1. 根因是 Web 渲染函数在布局改造后丢失了体系级 workbench section。
   - Supports: 页面仍有“八字工作台/紫微工作台”文本，但没有测试要求的 `bazi-workbench/ziwei-workbench` section。
   - Test: 恢复体系级 section 包裹后重跑 Web 和 benchmark hardening 测试。
2. 根因是测试过期。
   - Conflicts: 体系级 section 是区分八字/紫微工作台的稳定合同，恢复它不会增加新视觉样式或新业务规则。
   - Test: 保持测试合同不变，修复 HTML 输出。
3. 根因是八字计算失败。
   - Conflicts: CLI/API 已能返回结构化八字结果，失败点是 HTML 字符串断言。
   - Test: 只修改 Web HTML 后重跑相关回归。

### Root Cause

Web 生产空间布局改造时保留了通用 `#workbench` 导航锚点，但删除了测试和结构化工作台合同依赖的体系级 section；同一处渲染顺序还让工作台先于 Markdown 报告输出。

### Fix

- 在八字工作台外恢复 `<section id="bazi-workbench">`。
- 在紫微工作台外恢复 `<section id="ziwei-workbench">`。
- 将 Markdown 报告输出移动到工作台之前，确保右上报告面板先展示生成结果，再展示结构化工作台。
- 增加本地 Web 回归断言，锁定 Markdown 先于工作台 section。

### Regression Evidence

Completed:

```bash
.venv/bin/python -m pytest -q tests/regression/test_web_html.py tests/regression/test_bazi_ziwei_benchmark_hardening.py
.venv/bin/python -m pytest -q tests/regression/fate_core/test_field_registry.py tests/regression/fate_core/test_pure_analysis_usecase.py tests/regression/test_capability_protocol.py tests/regression/test_fate_core_cli.py tests/regression/test_fate_policy_assets.py tests/regression/test_solar_terms_golden.py tests/regression/test_strength_mapping.py tests/regression/test_bazi_statement_golden.py tests/regression/test_bazi_ziwei_benchmark_hardening.py tests/regression/test_bazi_ziwei_rule_depth.py tests/regression/test_api_contracts.py tests/regression/test_web_html.py
.venv/bin/python -m ruff check domains/experience-delivery/services/fatecat-delivery/src/web_ui.py tests/regression/test_web_html.py
```

Result:

- Web and benchmark hardening targeted tests: 15 passed.
- 八字/能力协议/API/Web 本地核心回归：100 passed.
- Ruff targeted check: All checks passed.

## 2026-06-15 Web follow-up: TradeCat Labs branding missing from empty `/web`

### Bug

用户要求强调 FateCat 是 TradeCat Labs 实验室项目，并提供 DEX Screener、X、GitHub、Hugging Face 链接；这些链接已经进入配置和报告页脚，但打开 `/web` 空表单页时看不到。

### Observations

- `infra/environments/local/branding.json` 已包含 `dexScreenerUrl`、`xUrl`、`githubUrl`、`huggingFaceUrl`。
- `fate_core.support.branding` 已把这些字段暴露给 API payload、报告页脚和 Bot 按钮。
- `tests/regression/test_branding_support.py` 覆盖了 branding payload 和报告 Markdown。
- `web_ui.py` 只渲染字段契约、表单、结果、底部页面元信息，没有消费 `get_branding_payload()`。
- 本地 `127.0.0.1:8001` 仍在跑旧进程，返回的 HTML 还没有上一轮 CSS/nav，说明即使代码更新，运行进程也需要重启才会显示。

### Hypotheses

1. 根因是 `/web` 空表单页没有接入 branding payload。
   - Supports: 代码没有 import 或调用 `get_branding_payload()`。
   - Test: 给空表单页增加 branding panel，并断言四个链接出现在 `/web`。
2. 根因是配置没有加载。
   - Conflicts: API/report/Bot 测试已能读到相同 branding 字段。
3. 根因只是浏览器缓存或旧进程。
   - Supports: 当前 8001 进程返回旧 HTML。
   - Conflicts: 即使新代码启动，空表单页原本也不会显示四个链接。

### Root Cause

TradeCat Labs 口径已进入统一 branding 数据源和报告输出，但 `/web` 空表单页没有消费该数据源；同时本地服务进程未重启导致页面继续显示旧 HTML。

### Fix

- `web_ui.py` 在标题下方渲染 `project-brand` 区块，直接使用 `get_branding_payload()` 显示 TradeCat Labs 说明和 DEX/X/GitHub/Hugging Face 链接。
- 页面导航增加“项目”锚点。
- `test_web_html.py` 增加空表单页品牌区块和四个外链断言。

### Regression Evidence

Completed:

```bash
.venv/bin/python -m pytest -q tests/regression/test_web_html.py tests/regression/test_branding_support.py
curl -fsS http://127.0.0.1:8001/web | rg 'TradeCat Labs|dexscreener|x.com/tradecatlabs|github.com/tradecatlabs|huggingface.co/tradecatlabs'
```

Result:

- `17 passed in 4.74s`
- `/web` 空表单页返回 `project-brand` 区块，包含 TradeCat Labs 标题、实验室项目说明、DEX Screener、X、GitHub、Hugging Face 链接。
- 本地 8001 服务已重启，当前后台进程为 `start.py api` + `src/main.py`，`/health` 和 `/web` 返回 200。

## 2026-06-15 Web bug: generate Markdown button appeared inactive

### Bug

用户点击 `/web` 页面“生成 Markdown 报告”后看起来没有反应，尤其是空表单或未填完必填字段时没有看到服务端错误反馈。

### Observations

- 表单字段使用 HTML5 `required` 属性，浏览器会在请求到达 FastAPI 之前拦截空值或未填完的提交。
- 服务端只在 `form.has_input()` 为真时生成报告或错误；空表单提交和首次打开 `/web` 在服务端状态上不可区分。
- `/web` 原本没有显式提交标记，所以点击按钮但所有业务字段为空时，服务端仍渲染初始页。
- 本地 8001 旧进程曾继续返回旧 HTML；重启后新代码才对 curl 验证生效。

### Hypotheses

1. 浏览器原生 `required` 校验阻止请求进入服务端。
   - Supports: HTML 中存在 `required`；空表单点击不会触发服务端错误页。
   - Test: 移除 `required` 后提交空表单必须由服务端返回“缺少必填字段”。
2. 空表单提交缺少显式提交标记。
   - Supports: `has_input()` 对空字段返回 false；首次打开和空提交路径相同。
   - Test: 增加 `submitted=1` hidden input 后，`/web?submitted=1` 必须返回错误块。
3. 只是运行进程没有更新。
   - Supports: 重启前 curl 仍看到旧 required HTML。
   - Conflicts: 即使进程更新，缺少 `submitted` 标记仍会让空提交走初始页。

### Root Cause

`/web` 表单把必填校验交给浏览器原生 `required`，导致请求可能根本不到服务端；同时服务端没有提交状态标记，无法区分“首次打开页面”和“用户点击生成但没有填字段”。两者叠加后，按钮在用户视角表现为“没反应”。

### Fix

- 表单增加 `<input type="hidden" name="submitted" value="1">`，服务端接收 `submitted` 查询参数。
- `WebReportForm` 增加 `submitted` 状态，`render_web_report_page()` 在 `submitted` 或存在输入时都进入报告/错误生成路径。
- 移除表单字段的 HTML5 `required` 属性，让必填错误由服务端统一写入页面。
- 增加回归测试，断言空提交返回服务端错误块，并禁止页面重新引入 `required`。

### Regression Evidence

Completed:

```bash
.venv/bin/python -m ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py domains/experience-delivery/services/fatecat-delivery/src/web_ui.py tests/regression/test_web_html.py
.venv/bin/python -m pytest -q tests/regression/test_web_html.py
curl -fsS 'http://127.0.0.1:8001/web?submitted=1' > /tmp/fatecat-web-empty-submit.html
curl -fsS 'http://127.0.0.1:8001/web?submitted=1&birthDate=1990-01-01&birthTime=08:00&birthPlace=%E5%8C%97%E4%BA%AC&gender=male&name=%E6%B5%8B%E8%AF%95' > /tmp/fatecat-web-full-submit.html
```

Result:

- `ruff check` passed.
- `pytest` passed with `9 passed in 1.97s`.
- Empty submit returns `<h2 id="errors">错误</h2>` and `缺少必填字段: 出生日期、出生时间、出生地区、性别`.
- Full submit returns `Markdown 输出` / `report-markdown` and no missing-field error.
- `/web` HTML remains zero-beauty: no `<style>`、`style=`、`class=`、`@media` or `required` attributes.

## 2026-06-15 Web bug: golden layout copied as ratio but not workbench

> 历史记录：该布局授权已由用户于 2026-07-12 撤销。以下内容仅说明当时的故障与修复，不再代表当前 Web 设计契约；当前规则以 `/home/lenovo/.codex/Design.md`、`GATE-0001` 和 `assert_zero_beauty_semantic_html` 为准。

### Bug

用户要求把 `D:\.projects\pdf` 的 Web 生产空间三块黄金分割布局引用到 FateCat `/web`，但第一版只复制了比例和三个语义区块，没有复制目标工作台的全屏结构。用户截图对比后确认当前 FateCat 页面仍像普通文档流，不像目标工作台。

### Observations

- FateCat 第一版仍在三块 grid 之前显示外部 `h1` 和页面导航，导致第一屏先出现普通页面标题和列表。
- 三块 grid 被放在普通文档流下方，没有成为页面本体。
- 目标 pdf 工作台第一屏没有外部 `h1`；`<body>` 内直接是全屏三窗口工作台。
- 目标 pdf 工作台使用 `html/body height: 100%`、`body overflow: hidden`、`form` 高度占满视口、面板边界、深色工作台背景和顶部 61.8034% / 底部 38.1966% 网格。
- FateCat 第一版禁止了背景、边界和字体等外壳 CSS，结果丢掉了目标工作台可见结构。

### Hypotheses

1. 根因是只复制比例，没有复制“页面即工作台”的外壳契约。
   - Supports: FateCat 页面截图顶部存在大标题和导航，目标工作台没有。
   - Test: `<body>` 必须直接进入 `<form class="web-production-grid">`，且 `h1` 不在 body 中。
2. 根因是治理例外过窄，错误禁止了 pdf 工作台外壳 CSS。
   - Supports: 第一版测试禁止 `background:`、`color:`、`font-family`，与目标工作台源码冲突。
   - Test: 测试应允许工作台外壳 CSS，但继续禁止阴影、渐变、动画、卡片等装饰。
3. 根因是三块区域职责放错。
   - Conflicts: 第一版已经是左上项目、右上报告、底部参数，职责方向正确。
   - Test: 只调整外壳与面板结构，不改变报告生成链路。

### Root Cause

我把用户要求的“复用 pdf Web 生产空间”错误降级成“在普通语义页面里放一个黄金比例 grid”。真实目标不是普通页面布局，而是全屏工作台外壳：三块面板就是第一屏主体，外部标题和导航不能占用第四个视觉块。

### Fix

- 移除 `/web` body 外部 `h1` 和外部导航；页面标题只保留在 `<title>`。
- 让 `<body>` 直接进入 `<form class="web-production-grid">`。
- 复刻 pdf 工作台外壳：全屏 `html/body`、深色背景、面板边界、黄金比例 grid、`gap: 0`、面板滚动和窄屏自然堆叠。
- 右上报告面板增加标题行和提交按钮，贴近目标工作台右上主操作结构。
- 底部参数区改为控件网格，页面导航和页面元信息收到底部区域内。
- 更新治理例外：允许复刻 pdf 工作台外壳 CSS；继续禁止圆角、阴影、动画、图标、卡片和营销视觉。

### Regression Evidence

Completed:

```bash
.venv/bin/python -m pytest -q tests/regression/test_web_html.py
bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-golden-web-layout-v2
curl -fsS http://127.0.0.1:8001/web > /tmp/fatecat-web-workbench-v2.html
curl -fsS 'http://127.0.0.1:8001/web?submitted=1&birthDate=1990-01-01&birthTime=08:00&birthPlace=%E5%8C%97%E4%BA%AC&gender=male&name=%E6%B5%8B%E8%AF%95' > /tmp/fatecat-web-report-v2.html
google-chrome --headless --no-sandbox --disable-gpu --window-size=2048,1180 --screenshot=/tmp/fatecat-web-workbench-v2.png http://127.0.0.1:8001/web
```

Result:

- `tests/regression/test_web_html.py` passed with `9 passed`.
- `scripts/local-ci.sh --profile quick` passed with `42 passed`.
- `/web` DOM now starts with `<body>` then `<form class="web-production-grid" method="get" action="/web">`; body no longer renders `<h1>FateCat Web Markdown 报告</h1>`.
- `/web` contains `web-production-report-header` and the right-top `生成 Markdown 报告` submit button.
- Full submit still renders `Markdown 输出` / `report-markdown` and keeps `当前输入` in the bottom parameter panel.
- Headless Chrome screenshot written to `/tmp/fatecat-web-workbench-v2.png`; visible first screen is three workbench panels matching the pdf workbench structure.

## 2026-06-15 production audit follow-up: false readiness claims and false-green tests

### Bug

生产级审计发现仓库存在声明、测试和协议语义不一致：

- `system_optimization.py` 声称 GraphQL、WebSocket、batch 等能力已启用，但真实路由不存在。
- 旧 smoke 测试捕获异常后直接返回，依赖或实现失败时仍可能 pytest passed。
- 八字 API 输入错误可能被打成 500；部分内部失败可能以 HTTP 200 + `success=false` 返回。
- 单实例自托管口径下，限流、Bot 补发、监控、timeout 和 capability 暴露边界需要明确进入代码和测试。

### Root Cause

仓库此前把“未来能力”和“当前真实启用能力”混在一个优化报告里，同时部分测试承担的是人工 smoke 角色，不是严格回归门禁。API 层也缺少统一输入校验和错误状态码边界，导致客户端无法可靠区分输入错误、资源繁忙和服务端故障。

### Fix

- `system_optimization.py` 改为只报告当前进程真实实现能力；未实现的 `/graphql`、`/ws`、`/api/v1/batch` 进入 planned-not-enabled 列表，不再声明 ready for production。
- `test_all_features.py`、`test_complete_integration.py`、`test_extended.py`、`test_calculator.py` 捕获异常后改为 `pytest.fail()`，输出文件进入 `tmp_path`。
- `models.py` 增加日期、时间和 IANA timezone 校验；`main.py` 统一非法输入 422，内部异常 500，资源背压 503。
- `main.py` 增加 `FATE_MAX_INFLIGHT_CALCULATIONS` 同步计算槽位，指标暴露 `fatecat_calculation_slots_in_use` / `fatecat_calculation_slots_max`，避免 timeout 后底层同步计算无限堆积。
- Bot 本地补发队列增加稳定幂等键、去重、原子写入和 ACK 删除；指标显式声明 `backend="memory",scope="single_process"`。
- capability registry 增加 `markdownDefault` 和 surfaces，区分 capability API、Markdown report 和 Web form 暴露面。
- MingLi-Bench 接入预测文件 gate；八字 300+ golden matrix 默认跑 requiredTags representative，完整矩阵由 `FATECAT_RUN_FULL_GOLDEN_MATRIX=1` 显式开启。
- 项目 classifier 从 Alpha 调整为 Beta，保持不声明 Production/Stable。

### Regression Evidence

Completed:

```bash
.venv/bin/python -m pytest tests/regression/test_api_contracts.py tests/regression/test_operability_docs.py -q
.venv/bin/python -m ruff check domains/experience-delivery/services/fatecat-delivery/src/main.py tests/regression/test_api_contracts.py tests/regression/test_operability_docs.py
bash scripts/local-ci.sh --profile all
```

Result:

- Targeted regression: `30 passed in 4.04s`.
- Ruff targeted check: `All checks passed!`.
- Full local CI: `profile=all` completed with evidence at `/tmp/fatecat-local-ci-20260615235920`.
- Full acceptance pytest: `168 passed, 1 skipped in 232.48s`.
- Docker container smoke: `ok image=fatecat-delivery:local url=http://127.0.0.1:8002/web`.
- Production-readiness static gate passed; live API URL and live Telegram Bot verification intentionally skipped because no real `--api-url` / `--require-live-bot` input was provided.

## 2026-06-16 local-ci follow-up: topic profile mypy narrowing failure

### Bug

`bash scripts/local-ci.sh --profile quick` 在 `mypy fate_core` 阶段失败。

Observed failure excerpt:

```text
domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py:886: error: Generator has incompatible item type "int"; expected "bool"  [misc]
domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py:886: error: Value of type "Collection[str]" is not indexable  [index]
domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_pure_analysis.py:886: error: "Collection[str]" has no attribute "get"  [attr-defined]
```

### Observations

- 失败行在 `_build_topic_profiles()` 的 `topic_specs` 遍历里。
- `topic_specs` 是混合 dict 列表，字段包含 `topic`、`basis`、`scoreBasis`、`evidenceFields`、`riskBoundary`。
- 未显式标注时，mypy 把 `spec["scoreBasis"]` 推断成过窄的集合类型，导致 generator 中的 `item.get()` 被判为非 dict。

### Hypotheses

1. 根因是 `topic_specs` 缺少显式类型，mypy 对异构 dict list 推断失真。
   - Supports: 错误集中在 `spec["scoreBasis"]` 的 item 类型。
   - Test: 给 `topic_specs` / `profiles` 加 `list[dict[str, Any]]`，并显式收窄 score item。
2. 根因是运行时 `scoreBasis` 结构不一致。
   - Conflicts: API/Web/topic profile 回归此前通过，运行时输出结构稳定。
3. 根因是 mypy 版本或配置变化。
   - Conflicts: 代码本身依赖 mypy 对异构 literal 的推断，不应让门禁靠版本偶然通过。

### Root Cause

`_build_topic_profiles()` 在异构 dict list 上依赖隐式类型推断，mypy 将 `scoreBasis` 迭代项推断成非 dict 类型，导致 quick gate 静态检查失败。

### Fix

- 显式标注 `topic_specs: list[dict[str, Any]]` 和 `profiles: list[dict[str, Any]]`。
- 将 score generator 改成显式循环，并在读取 `value` 前确认 score item 是 dict。

### Regression Evidence

Completed:

```bash
bash scripts/local-ci.sh --profile quick
.venv/bin/python -m pytest tests/regression/test_bazi_ziwei_rule_depth.py -q
```

Result:

- `local-ci quick` passed with evidence at `/tmp/fatecat-local-ci-20260616173830`.
- Focused regression tests passed: `49 passed in 9.74s`.
- `mypy fate_core` passed: `Success: no issues found in 39 source files`.
- 八字 rule-depth regression passed: `30 passed in 62.50s`.

## 2026-06-16 Web follow-up: submitted birth place hidden in report

### Bug

用户提交非北京出生地区后，Web/Markdown 报告显示：

```text
| 出生地区 | 已填写（非北京地区已隐藏） |
```

用户当前要求是展示已填写出生地区。

### Observations

- `git status --short --branch` 显示 `main...origin/main [ahead 27]`，本地提交未推送远端。
- 旧隐藏策略来自活跃 helper：
  - `domains/experience-delivery/services/fatecat-delivery/src/report_generator.py::public_birth_place`
  - `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_ziwei.py::_public_place`
  - `domains/fate-analysis/services/fate-core/src/fate_core/usecases/calculate_almanac.py::_public_place`
- 一线 README / docs 仍写着非北京地区展示层隐藏，和当前产品口径冲突。

### Hypotheses

1. 根因是旧隐私展示策略硬编码，而不是页面没拿到 birthPlace。
   - Supports: helper 直接返回 `已填写（非北京地区已隐藏）`。
   - Test: 去掉 helper 脱敏后，Web 和 Markdown 都应显示 `上海` / `上海市`。
2. 根因是 location 解析失败。
   - Conflicts: 合法上海 payload 的 API 可以生成完整 Markdown，只是展示字段被替换。
3. 根因是 Web 前端未渲染该字段。
   - Conflicts: Markdown 里已有 `出生地区` 行，只是值被脱敏。

### Root Cause

历史隐私策略把“非北京出生地区不得展示”写进生产 helper 和回归测试，导致合法用户输入在报告层被替换为隐藏文案。

### Fix

- `public_birth_place()`、紫微 `_public_place()`、黄历 `_public_place()` 改为返回用户提交地区的规范化文本。
- Web、Markdown、紫微、黄历 capability 回归改为断言真实提交地区会展示。
- README 和一线 reference docs 改为当前口径：展示层回显出生地区，经纬度继续用于解析和真太阳时计算。

### Regression Evidence

Completed:

```bash
.venv/bin/python -m pytest tests/regression/test_web_html.py tests/regression/test_api_contracts.py tests/regression/test_bazi_ziwei_benchmark_hardening.py tests/regression/test_capability_protocol.py -q
bash scripts/check-privacy-fixtures.sh
bash scripts/local-ci.sh --profile quick
```

Result:

- Targeted regression passed: `56 passed in 8.87s`.
- Privacy fixtures gate passed.
- `local-ci quick` passed with evidence `/tmp/fatecat-local-ci-20260616175059`.
- Direct TestClient smoke:
  - `/web` with `birthPlace=上海`: `web_has_shanghai=True`, `web_has_hidden=False`
  - `/api/v1/report/markdown` with `birthPlace.name=上海市`: `birth_place_line | 出生地区 | 上海市 |`

## 2026-06-17 HF Space Web submit timeout and no-feedback state

### Bug

用户在 HF Space Web 工作台点击“生成 Markdown 报告”后，页面看起来没有反应。

### Observations

- 远端空表单 `/web` 能正常返回，页面存在 1 个原生 form 和 1 个 submit button。
- 远端提交态 `/web?...submitted=1` 一度稳定返回应用层 `504 请求处理超时`，每次约 31 秒。
- 远端 `/metrics` 记录 `GET /web` 多次 `504 timeout`，而 `POST /api/v1/report/markdown` 曾在约 1.27 秒内返回 200。
- 本地同一路径 `TestClient GET /web?...submitted=1` 约 0.58 秒返回完整 HTML。
- HF 免费 CPU 新实例复测后，中文北京输入约 8 秒、经纬度输入约 4.8 秒生成 Markdown，说明按钮提交链路存在，但免费环境冷启动/排队会触发默认 30 秒保护超时。

### Root Cause

Web 表单使用原生 GET 提交，服务端在 HF 免费 CPU/单实例构建或冷启动窗口内可能超过默认 `FATE_REQUEST_TIMEOUT_SECONDS=30`。页面提交后没有即时状态反馈，用户看到的是“点击后无响应”；一旦超过后端保护超时，返回 JSON 504 而不是 Web 报告页。

### Fix

- Web form 增加稳定 `id="web-report-form"`，提交按钮显式绑定 `form="web-report-form"`。
- 页面提交事件只做状态提示：按钮文案切换为“生成中...”，报告区显示“正在生成 Markdown 报告...”；不拦截原生 GET，不改布局。
- HF Space Docker 模板设置 `FATE_REQUEST_TIMEOUT_SECONDS=120`，只放宽免费托管环境的请求保护窗口。

### Regression Evidence

Completed:

```bash
PYTHONPATH=... .venv/bin/python -m pytest tests/regression/test_web_html.py -q
bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-web-submit-fix
FATECAT_HF_COMMIT_MESSAGE='fix web submit feedback and HF timeout' bash scripts/hf-space-deploy.sh --space tradecatlabs/fatecat --prune-remote
```

Result:

- Focused Web regression passed: `10 passed in 1.96s`.
- Local quick CI passed: `50 passed in 8.61s`, evidence `/tmp/fatecat-local-ci-web-submit-fix`.
- HF upload CLI ended with `httpx.ReadTimeout` during commit response, but remote files were pulled back and confirmed updated:
  - `Dockerfile` includes `FATE_REQUEST_TIMEOUT_SECONDS=120`.
  - `web_ui.py` includes `web-report-form`, `form="web-report-form"` and `正在生成 Markdown 报告...`.
- HF runtime rebuilt to SHA `8e45ab3fb9177ce00d1421fdec796c0718194ea8`.
- Remote direct submit passed:
  - URL: `https://tradecatlabs-fatecat.hf.space/web?...submitted=1`
  - `HTTP 200`, about `6.96s`, contains `Markdown 输出`, `报告已生成。`, and `# 命理排盘报告：远端验收`.
  - Does not contain `请求处理超时` or `<h2 id="errors">错误</h2>`.
- Remote Playwright click passed:
  - submit button click returned `HTTP 200`.
  - final page contains `Markdown 输出` and `命理排盘报告：浏览器验收`.
  - final page does not contain `请求处理超时`.

## 2026-06-17 HF Space connection refused report

### Bug

用户浏览器提示 `tradecatlabs-fatecat.hf.space 拒绝了我们的连接请求`。

### Observations

- `hf spaces info tradecatlabs/fatecat --expand runtime` 返回 `stage=RUNNING`、`domain=READY`、`hardware=cpu-basic`、`replicas.current=1`。
- `curl -I https://tradecatlabs-fatecat.hf.space/web` 已连到服务端，返回 `HTTP/2 405` 且 `allow: GET`，说明域名和容器可达，但 `/web` 不支持 HEAD。
- `curl -L https://tradecatlabs-fatecat.hf.space/web` 返回 `HTTP 200`，页面包含 `FateCat Web Markdown 报告`、`web-report-form`、`生成 Markdown 报告`。
- `curl -L https://tradecatlabs-fatecat.hf.space/health` 返回 `HTTP 200` 和 `status=ok`。
- 本地 Playwright 浏览器工具未能复核，因为当前环境缺少 Playwright Chromium 二进制。

### Current Conclusion

当前远端不是持续性崩溃或端口未监听。用户看到的拒绝连接更可能发生在 HF Space 刚部署、重启、冷启动、平台路由切换或浏览器/网络缓存旧失败状态的短窗口内。

### User-Facing Recovery

- 使用完整 HTTPS 地址：`https://tradecatlabs-fatecat.hf.space/web`。
- 强制刷新或换无痕窗口。
- 如果复现，先打开 `https://tradecatlabs-fatecat.hf.space/health` 判断是整站不可达还是仅页面路径问题。

## 2026-06-17 production-readiness metrics pipefail false negative

### Bug

`scripts/public-release-gate.sh --api-url https://tradecatlabs-fatecat.hf.space` 在 live `/metrics` 阶段失败：

```text
curl: (23) Failure writing output to destination
```

### Root Cause

`scripts/production-readiness.sh` 使用 `curl -fsS "$url/metrics" | grep -q 'fatecat_requests_total'`。在 `set -o pipefail` 下，`grep -q` 命中后提前关闭管道，`curl` 可能收到写入失败并返回 23，导致已可用的 `/metrics` 被误判失败。

### Fix

- 先用 `curl -fsS "$url/metrics" -o "$metrics_file"` 写入临时文件。
- 再用 `grep -q 'fatecat_requests_total' "$metrics_file"` 检查指标内容。

### Regression Evidence

```bash
bash scripts/public-release-gate.sh --api-url https://tradecatlabs-fatecat.hf.space --output /tmp/fatecat-public-release-20260617-rerun
bash scripts/public-release-gate.sh --api-url https://tradecatlabs-fatecat.hf.space --skip-delivery-smoke --output /tmp/fatecat-public-release-20260617-final
```

Result:

- 本地 quick CI 通过。
- public release policy 通过。
- 本地 delivery smoke 通过。
- HF `/health`、`/ready`、`/metrics` live 验证通过。
