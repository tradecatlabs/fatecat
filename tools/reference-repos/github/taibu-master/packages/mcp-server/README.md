# taibu-mcp-server

TaiBu 的在线 MCP Server，基于 Streamable HTTP 运行，面向远程部署场景。

当前发布线：`2.0.x`

说明：本 README 将 `1.2.5` 之后累计的改动按功能重排为 `1.2.6 -> 1.3.0 -> 1.4.0 -> 1.5.0 -> 2.0.0`，便于按大功能分批发布 npm 版本。

## 适用场景

- 需要把 TaiBu MCP 工具部署成远程服务
- 需要 OAuth 2.1 + PKCE 接入 ChatGPT 等 MCP 客户端
- 需要继续兼容用户级 API Key 调用

## 安装

```bash
npm install taibu-mcp-server
```

## 核心特性

- 复用 `taibu-core` 的 15 个工具能力
- Streamable HTTP 入口：`/mcp`
- OAuth 2.1 + PKCE + 动态客户端注册
- `Authorization: Bearer <token>` 与 `x-api-key` 双认证链路
- 基于共享 transport 的 `structuredContent + content` 响应策略
- OAuth 授权页内置当前工具清单展示

## 输出约定

在线 MCP 响应分成两条通道：

- `content[0].text`: canonical text，适合直接阅读或继续交给 AI
- `structuredContent`: canonical JSON，并与工具公开 `outputSchema` 对齐，适合客户端按 schema 消费

注意：

- `structuredContent` 与 Web 结果页使用的是同源 canonical JSON
- `content[0].text` 只承担文本阅读，不再承载 JSON 字符串

## 最小运行方式

```bash
pnpm install
pnpm -C packages/core build
pnpm -C packages/mcp-server build
pnpm -C packages/mcp-server start
```

默认服务信息：

- `GET /health`
- `GET /info`
- `POST /mcp`
- `GET /.well-known/oauth-authorization-server`
- `GET /.well-known/oauth-protected-resource`

## 环境变量

### 基础运行

| 变量 | 说明 |
|------|------|
| `SUPABASE_URL` | Supabase 项目地址 |
| `SUPABASE_ANON_KEY` | Supabase anon key |
| `SUPABASE_SYSTEM_ADMIN_EMAIL` | 系统管理员邮箱，用于 MCP Server 受控访问数据库 |
| `SUPABASE_SYSTEM_ADMIN_PASSWORD` | 系统管理员密码 |
| `MCP_HOST` | 监听地址，默认 `127.0.0.1` |
| `PORT` | 端口，默认 `3001` |
| `MCP_ALLOWED_ORIGINS` | 浏览器 Origin 白名单 |
| `MCP_ALLOWED_HOSTS` | Host 白名单 |
| `MCP_MAX_SESSIONS` | 最大并发会话数 |
| `MCP_SESSION_TTL_MS` | 会话生命周期 |
| `MCP_SESSION_IDLE_MS` | 会话空闲超时 |
| `MCP_MAX_SSE_PER_USER` | 每用户 SSE 并发上限 |
| `MCP_TRUST_PROXY` | 反向代理后设为 `true` |
| `TAIBU_SITE_URL` | OAuth 授权页 Logo 与站点链接来源 |
| `AMAP_WEB_SERVICE_KEY` | 可选。出生地点解析服务所需的高德 Web Service Key |

### OAuth 2.1

| 变量 | 说明 |
|------|------|
| `MCP_JWT_SECRET` | JWT 签名密钥，至少 32 字符 |
| `MCP_ISSUER_URL` | OAuth issuer URL |
| `MCP_ALLOWED_TOKEN_AUDIENCES` | 额外允许的 access token audience |
| `MCP_ACCESS_TOKEN_TTL` | Access token 有效期，单位秒 |
| `MCP_REFRESH_TOKEN_TTL` | Refresh token 有效期，单位秒 |
| `MCP_OAUTH_DEBUG` | OAuth 调试日志开关 |

## MCP 客户端示例

### OAuth / Streamable HTTP

```json
{
  "mcpServers": {
    "taibu": {
      "type": "streamable-http",
      "url": "https://your-domain.example.com/mcp"
    }
  }
}
```

### API Key 调用

```json
{
  "mcpServers": {
    "taibu": {
      "type": "streamable-http",
      "url": "https://your-domain.example.com/mcp",
      "headers": {
        "x-api-key": "sk-mcp-xxxxxxxx"
      }
    }
  }
}
```

Bearer token 的优先级高于 API Key；若 Bearer token 存在但无效，不会回退到 API Key。

## 与其他包的关系

- [`taibu-core`](https://www.npmjs.com/package/taibu-core): 工具注册、算法实现、transport 适配器
- [`taibu-mcp`](https://www.npmjs.com/package/taibu-mcp): 本地 `stdio` MCP Server

注意：`taibu-core` 仍保持纯算法边界，本身不接地图服务，也不会自动把地点名换算为经度。

## License

`taibu-mcp-server` 使用 `MIT` 许可证，详见当前目录下的 `LICENSE` 文件。

## 版本批次

| 版本 | 批次说明 |
|------|----------|
| `2.0.0` | 跟随 core 切换到最终 MCP 契约：`content` 输出规范文本，`structuredContent` 输出 canonical JSON，在线服务保留 runtime `placeResolutionInfo` 扩展 |
| `1.5.0` | 统一在线服务版本号，收口共享 transport、动态授权页工具展示、会话管理与运行时契约 |
| `1.4.0` | 跟随核心接入 `daliuren` 大六壬工具 |
| `1.3.0` | 跟随核心接入 `qimen` 奇门遁甲工具 |
| `1.2.6` | 延续 `1.2.5` 做补丁发布，集中修复缓存回源、鉴权边界、结构化输出与测试覆盖 |
| `1.2.5` | `core` / `mcp` 的旧基线版本；本次将在线服务也统一收口到同一版本线 |
