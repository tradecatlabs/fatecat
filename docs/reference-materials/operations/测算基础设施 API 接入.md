# 测算基础设施 API 接入

本文是 FateCat 面向 Agent 与应用开发者的最小接入说明。当前生产默认报告只支持综合八字 `bazi`，其他生产或规划体系必须通过独立 capability 调用，不得混入默认 Markdown。

## 发现入口

| 入口 | 方法 | 用途 |
| --- | --- | --- |
| `/metadata` | GET | 服务定位、开发者入口、质量门禁、隐私口径 |
| `/openapi.json` | GET | FastAPI OpenAPI 机器契约 |
| `/docs` | GET | 本地交互式 API 文档 |
| `/capabilities` | GET | 统一 capability 注册表 |
| `/reports` | GET | 报告 profile、Markdown、异步 job 入口 |
| `/health` | GET | 存活检查 |
| `/ready` | GET | 数据库与 capability registry 就绪检查 |
| `/metrics` | GET | Prometheus 文本指标 |

## Capability 调用

```bash
curl -sS http://127.0.0.1:8001/capabilities \
  | jq '.data.capabilities[] | {capabilityId,status,defaultVisibility,maturity,testGate}'
```

```bash
curl -sS -X POST http://127.0.0.1:8001/capabilities/almanac/calculate \
  -H 'Content-Type: application/json' \
  -d '{"dateRange":{"start":"2026-05-08","end":"2026-05-08"},"eventType":"出行","place":"北京"}'
```

返回结构固定包含：

| 字段 | 含义 |
| --- | --- |
| `capabilityId` | 执行的能力 ID |
| `status` | 能力生产状态 |
| `reportProfile` | 输出 profile |
| `data` | 盘面或计算结果 |
| `evidence` | 证据字段与规则 ID |
| `risk` | 免责声明和禁止断语边界 |
| `metadata` | maturity、engine、evidencePolicy、testGate |

## 报告入口

同步 Markdown：

```bash
curl -sS -X POST http://127.0.0.1:8001/api/v1/report/markdown \
  -H 'Content-Type: application/json' \
  -d '{
    "name":"测试样本",
    "gender":"male",
    "birthDate":"1990-01-01",
    "birthTime":"08:00:00",
    "birthPlace":{"name":"北京市","longitude":116.4074,"latitude":39.9042,"timezone":"Asia/Shanghai"},
    "options":{"useTrueSolarTime":true,"daylightSaving":"auto","midnightMode":"early","calendarType":"solar"}
  }'
```

Web 异步报告：

```bash
curl -sS -X POST http://127.0.0.1:8001/api/v1/report/jobs/web \
  -H 'Content-Type: application/json' \
  -d '{"birthDate":"1990-01-01","birthTime":"08:00:00","birthPlace":"北京","gender":"male","name":"测试样本","reportSystem":"bazi"}'
```

## 准入规则

| 能力状态 | 准入要求 |
| --- | --- |
| `production` | `maturity.level` 至少 L3，`testGate.status=passing`，必须声明本地回归命令，不得使用 `planned.*` provider |
| `planned` | `maturity.level=L0`，`testGate.status=blocked`，必须使用 `planned.*` provider 和 `planned-v0` engineVersion |
| 默认 Markdown | 必须且只能是 `bazi` |

## 错误与限流

| 状态码 | 含义 |
| --- | --- |
| 400 | capability 未知、未生产化或 payload 业务字段不合法 |
| 413 | 请求体超过 `FATE_MAX_REQUEST_BYTES` |
| 422 | FastAPI/Pydantic 参数校验失败 |
| 429 | 频率限制或报告队列已满 |
| 503 | 计算并发槽耗尽或 ready 检查失败 |
| 504 | 请求处理超过 `FATE_REQUEST_TIMEOUT_SECONDS` |

## 安全与隐私

- 公开 Web 示例和用户界面不得展示北京以外的真实地区名称。
- 记录接口需要 `FATE_API_TOKEN`、`FATE_API_ADMIN_TOKEN` 或 `FATE_API_USER_TOKENS`；禁用时返回 403。
- 文档、响应样例和日志不得输出真实 token、secret、DSN、私钥或服务账号内容。
- 外部 API 域名、真实 token、Bot webhook、远程服务器和生产数据库均属于：外部连通验证待执行。

## 本地验证

```bash
.venv/bin/python -m pytest -q tests/regression/test_api_contracts.py tests/regression/test_capability_protocol.py
bash scripts/local-ci.sh --profile quick
python3 governance/tools/validate_governance_package.py --project-root . --strict
```
