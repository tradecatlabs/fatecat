# Acceptance Checklist

# Global Standards

- [x] 变更边界限定在 developer contracts/docs、gate、metadata、local-ci、tests、AGENTS/roadmap 和任务文档。
- [x] 不连接真实 token、真实账号、生产域名、公网 API、Bot 或外部 developer portal。
- [x] 不保存真实 secret、DSN、私钥、证书、报告正文、生产路径或非北京真实地区样例。
- [x] focused tests、ruff、developer platform gate、developer docs smoke 和 quick local-ci 已通过。
- [x] 任务状态与真实 worktree 一致。

# Task Package Checklists

## TP-01.01

- [x] 复核现有 developer docs、sandbox fixture、OpenAPI export、local-ci 和 metadata。
Verify: `rg` / `sed`。
Gate: 当前差距明确。

## TP-02.01

- [x] 新增 developer platform contract。
Verify: JSON syntax + gate。
Gate: SDK/package baseline 不声明已发布。

## TP-02.02

- [x] 新增 sandbox token contract。
Verify: JSON syntax + gate。
Gate: token 服务状态为 contract-only/not implemented。

## TP-02.03

- [x] 新增 API changelog contract 和 human changelog。
Verify: JSON syntax + gate。
Gate: 0067 changelog entry 可追溯。

## TP-03.01

- [x] 新增 `developer-platform-gate`。
Verify: gate CLI。
Gate: output JSON status=passed。

## TP-03.02

- [x] 接入 `/metadata`、local-ci 和 summary artifact。
Verify: API metadata test + local-ci summary。
Gate: developerPlatformGate artifact 可发现。

## TP-03.03

- [x] 新增 developer platform 回归测试。
Verify: focused pytest。
Gate: publishedSdkPackages=0, liveSandboxTokenService=false。

## TP-04.01

- [x] 同步 AGENTS、developer README、API 接入文档和 roadmap。
Verify: diff review。
Gate: 文档不夸大。

## TP-04.02

- [x] 运行验证并记录本地交付证据。
Verify: local-ci summary。
Gate: 本地 quick CI 通过。

## Evidence Checklist

- [x] `python3 -m json.tool contracts/fate/developer/developer-platform.json`
- [x] `bash scripts/developer-platform-gate.sh --output-json /tmp/fatecat-developer-platform-gate.json`
- [x] `bash scripts/developer-docs-smoke.sh --output-json /tmp/fatecat-developer-docs-smoke-0067.json --openapi-json /tmp/fatecat-openapi-0067.json`
- [x] `.venv/bin/python -m pytest -q tests/regression/test_developer_platform_gate.py tests/regression/test_developer_docs_smoke.py tests/regression/test_api_contracts.py::test_measurement_infrastructure_metadata_and_reports_are_available`
- [x] `ruff check` / `ruff format --check` focused files
- [x] `bash scripts/local-ci.sh --profile quick --output /tmp/fatecat-local-ci-0067`
- [x] task validators
