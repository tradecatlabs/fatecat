/**
 * TaiBu MCP Server - Online (Streamable HTTP)
 */

import { config } from 'dotenv';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

// 仅加载仓库根目录 .env，统一配置来源。
const currentFileDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(currentFileDir, '../../..');
config({ path: resolve(repoRoot, '.env'), override: false });

import crypto from 'crypto';
import express from 'express';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  isInitializeRequest,
} from '@modelcontextprotocol/sdk/types.js';
import { mcpAuthRouter } from '@modelcontextprotocol/sdk/server/auth/router.js';

import {
  executeTool,
  buildListToolsPayload,
  buildToolSuccessPayload,
  normalizeTransportDetailLevel,
} from 'taibu-core/mcp';
import { createRequire } from 'node:module';

import {
  dualAuthMiddleware,
  rateLimitMiddleware,
  oauthRateLimitMiddleware,
  originValidationMiddleware,
  hostValidationMiddleware,
  sseConnectionLimitMiddleware,
  readPositiveIntEnv,
  type McpAuthInfo,
} from './middleware.js';

import { TaiBuOAuthProvider } from './oauth/provider.js';
import { cleanupOAuthArtifactsTransactionally, saveAuthorizationCode } from './oauth/store.js';
import { renderAuthorizePage } from './oauth/authorize-page.js';
import { validateOAuthLoginRequest } from './oauth/login-validation.js';
import { getAllowedTokenAudiences } from './oauth/jwt.js';
import { isOAuthDebugEnabled, oauthError } from './oauth/logger.js';
import { getSupabaseAuthClient } from './supabase.js';
import {
  attachPlaceResolutionInfoToResult,
  attachPlaceResolutionNoteToPayload,
  decorateToolListPayloadForRuntime,
  preprocessToolArgsForRuntimePlace,
} from './place-resolution.js';
const require = createRequire(import.meta.url);
const { version } = require('../package.json') as { version: string };
// ─── 会话管理配置 ───
const MAX_TOTAL_SESSIONS = readPositiveIntEnv('MCP_MAX_SESSIONS', 1000);
const SESSION_TTL = readPositiveIntEnv('MCP_SESSION_TTL_MS', 1800000); // 30min
const SESSION_IDLE = readPositiveIntEnv('MCP_SESSION_IDLE_MS', 600000); // 10min
const IS_PRODUCTION = process.env.NODE_ENV === 'production';

// ─── OAuth Provider ───
const oauthProvider = new TaiBuOAuthProvider();
const issuerUrl = new URL(process.env.MCP_ISSUER_URL || 'https://mcp.mingai.fun');
const scopesSupported = ['mcp:tools'] as const;
const resourceName = 'TaiBu MCP Server';
const resourceServerUrl = new URL('/mcp', issuerUrl);

/**
 * OAuth AS 元数据兼容对象。
 *
 * 端点路径与 MCP SDK mcpAuthRouter (v1.25.x) 内部注册的路由一致。
 * 若 SDK 升级后路径变更，需同步更新此处。
 */
const oauthMetadataCompatibility = {
  issuer: issuerUrl.href,
  authorization_endpoint: new URL('/authorize', issuerUrl).href,
  response_types_supported: ['code'],
  code_challenge_methods_supported: ['S256'],
  token_endpoint: new URL('/token', issuerUrl).href,
  token_endpoint_auth_methods_supported: ['client_secret_post', 'none'],
  grant_types_supported: ['authorization_code', 'refresh_token'],
  scopes_supported: [...scopesSupported],
  revocation_endpoint: new URL('/revoke', issuerUrl).href,
  revocation_endpoint_auth_methods_supported: ['client_secret_post'],
  registration_endpoint: new URL('/register', issuerUrl).href,
};

const protectedResourceMetadataCompatibility = {
  resource: resourceServerUrl.href,
  authorization_servers: [issuerUrl.href],
  scopes_supported: [...scopesSupported],
  resource_name: resourceName,
};

const app = express();

// trust proxy（反向代理后需要）
if (process.env.MCP_TRUST_PROXY === 'true') {
  app.set('trust proxy', true);
}

if (isOAuthDebugEnabled()) {
  // ─── OAuth 请求日志（调试用）───
  app.use((req, _res, next) => {
    const oauthPaths = ['/register', '/token', '/authorize', '/revoke', '/.well-known/'];
    const isOAuth = oauthPaths.some((p) => req.path.startsWith(p));
    if (isOAuth) {
      console.log(`[OAuth:req] ${req.method} ${req.path}`);
    }
    next();
  });

  // ─── MCP 请求日志（调试用）───
  app.use((req, res, next) => {
    if (req.path !== '/' && req.path !== '/mcp') {
      return next();
    }

    const accept = req.headers.accept ?? 'none';
    const hasAuth = typeof req.headers.authorization === 'string' || typeof req.headers['x-api-key'] === 'string';
    const sessionId = typeof req.headers['mcp-session-id'] === 'string' ? req.headers['mcp-session-id'] as string : '';
    const protocolVersion = typeof req.headers['mcp-protocol-version'] === 'string'
      ? req.headers['mcp-protocol-version'] as string
      : '';
    const sessionMark = sessionId ? ` session=${sessionId.slice(0, 8)}...` : '';
    const protocolMark = protocolVersion ? ` proto=${protocolVersion}` : '';

    res.on('finish', () => {
      console.log(`[MCP:req] ${req.method} ${req.path} status=${res.statusCode} accept=${accept} auth=${hasAuth ? 'yes' : 'no'}${sessionMark}${protocolMark}`);
    });

    next();
  });
}

// ─── OAuth 端点限流（在 mcpAuthRouter 之前，覆盖 /register /token /revoke）───
app.use(['/register', '/token', '/revoke'], oauthRateLimitMiddleware);

// ─── OAuth 路由（必须在 app root 且在 express.json 之前）───
// mcpAuthRouter 内部自带 express.urlencoded 解析
app.use(mcpAuthRouter({
  provider: oauthProvider,
  issuerUrl,
  resourceServerUrl,
  scopesSupported: [...scopesSupported],
  resourceName,
  // 禁用 SDK 内置限流，使用我们自己的
  authorizationOptions: { rateLimit: false },
  tokenOptions: { rateLimit: false },
  clientRegistrationOptions: { rateLimit: false },
  revocationOptions: { rateLimit: false },
}));

// ─── OAuth 登录表单处理（授权页 POST 目标）───
app.post('/oauth/login', oauthRateLimitMiddleware, express.urlencoded({ extended: false }), async (req, res) => {
  const {
    email, password,
    client_id, redirect_uri, code_challenge, code_challenge_method,
    state, scope, resource,
  } = req.body as Record<string, string>;

  // 参数校验
  if (!email || !password || !client_id || !redirect_uri || !code_challenge) {
    const html = renderAuthorizePage({
      clientId: client_id || '',
      redirectUri: redirect_uri || '',
      codeChallenge: code_challenge || '',
      codeChallengeMethod: code_challenge_method || 'S256',
      state, scope, resource,
      scopes: scope ? scope.split(' ') : [],
      error: '请填写邮箱和密码',
    });
    return res.status(400).send(html);
  }

  // 验证客户端
  let client;
  try {
    client = await oauthProvider.clientsStore.getClient(client_id);
  } catch (error) {
    oauthError('OAuth client lookup failed', error);
    return res.status(500).json({ error: 'OAuth service unavailable' });
  }
  if (!client) {
    return res.status(400).json({ error: 'Invalid client_id' });
  }

  const validation = validateOAuthLoginRequest({
    client,
    redirectUri: redirect_uri,
    scope,
    resource,
    issuerUrl,
    allowedAudiences: getAllowedTokenAudiences(issuerUrl),
  });

  if (!validation.ok) {
    const errorMessageMap: Record<string, string> = {
      'Invalid redirect_uri': 'redirect_uri 非法或未注册',
      'Invalid scope': 'scope 非法或超出客户端权限',
      'Invalid resource': 'resource 非法',
    };
    const html = renderAuthorizePage({
      clientName: client.client_name,
      clientId: client_id,
      redirectUri: redirect_uri,
      codeChallenge: code_challenge,
      codeChallengeMethod: code_challenge_method || 'S256',
      state,
      scope,
      resource,
      scopes: scope ? scope.split(' ') : [],
      error: errorMessageMap[validation.error] || '授权参数非法',
    });
    return res.status(400).send(html);
  }

  const validated = validation.value;

  // 用 Supabase Auth 验证用户凭据（需要纯 anon 客户端，不能用 accessToken 模式）
  const supabase = getSupabaseAuthClient();
  const { data: authData, error: authError } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (authError || !authData.user) {
    const html = renderAuthorizePage({
      clientName: client.client_name,
      clientId: client_id,
      redirectUri: validated.redirectUri,
      codeChallenge: code_challenge,
      codeChallengeMethod: code_challenge_method || 'S256',
      state,
      scope: validated.scope,
      resource: validated.resource,
      scopes: validated.scopes,
      error: '邮箱或密码错误',
    });
    return res.status(401).send(html);
  }

  // 生成授权码
  try {
    const code = await saveAuthorizationCode({
      clientId: client_id,
      userId: authData.user.id,
      redirectUri: validated.redirectUri,
      codeChallenge: code_challenge,
      scope: validated.scope,
      resource: validated.resource,
    });

    // 重定向回客户端
    const redirectUrl = new URL(validated.redirectUri);
    redirectUrl.searchParams.set('code', code);
    if (state) redirectUrl.searchParams.set('state', state);
    res.redirect(302, redirectUrl.href);
  } catch {
    const html = renderAuthorizePage({
      clientName: client.client_name,
      clientId: client_id,
      redirectUri: validated.redirectUri,
      codeChallenge: code_challenge,
      codeChallengeMethod: code_challenge_method || 'S256',
      state,
      scope: validated.scope,
      resource: validated.resource,
      scopes: validated.scopes,
      error: '授权失败，请重试',
    });
    return res.status(500).send(html);
  }
});

app.use(express.json({ limit: '1mb' }));

// 信息端点（便于手工检查服务可用性）
app.get('/info', (_req, res) => {
  res.status(200).json({
    name: 'TaiBu MCP Server',
    status: 'ok',
    transport: 'streamable-http',
    mcp_endpoint: resourceServerUrl.pathname,
    oauth_authorization_server_metadata: '/.well-known/oauth-authorization-server',
    oauth_protected_resource_metadata: `/.well-known/oauth-protected-resource${resourceServerUrl.pathname}`,
  });
});

// 兼容 OIDC 发现探测（部分客户端会尝试 openid-configuration）
app.get('/.well-known/openid-configuration', (_req, res) => {
  res.status(200).json(oauthMetadataCompatibility);
});

// 兼容客户端对 root protected-resource metadata 的探测
app.get('/.well-known/oauth-protected-resource', (_req, res) => {
  res.status(200).json(protectedResourceMetadataCompatibility);
});

// 健康检查（不需要认证）
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 开发环境：授权页预览（无需走完整 OAuth 流程即可调试样式）
if (!IS_PRODUCTION) {
  app.get('/dev/authorize-preview', (_req, res) => {
    const html = renderAuthorizePage({
      clientName: 'ChatGPT',
      scopes: ['mcp:tools'],
      clientId: 'preview-client-id',
      redirectUri: 'https://example.com/callback',
      codeChallenge: 'preview-challenge',
      codeChallengeMethod: 'S256',
      state: 'preview-state',
      scope: 'mcp:tools',
      error: _req.query.error === '1' ? '邮箱或密码错误' : undefined,
    });
    res.send(html);
  });
}

// ─── 双模式认证中间件实例 ───
const mcpAuth = dualAuthMiddleware(oauthProvider);

type SessionContext = {
  server: McpServer;
  transport: StreamableHTTPServerTransport;
  auth: McpAuthInfo;
  createdAt: number;
  lastActivityAt: number;
};

const SEED_SCOPED_TOOLS = new Set(['liuyao', 'tarot']);

function withSeedScope(name: string, args: unknown, auth: McpAuthInfo): unknown {
  if (!SEED_SCOPED_TOOLS.has(name)) {
    return args === undefined ? {} : args;
  }
  if (args === undefined) {
    return { seedScope: auth.userId };
  }
  if (!args || typeof args !== 'object' || Array.isArray(args)) {
    return args;
  }
  return {
    ...(args as Record<string, unknown>),
    seedScope: auth.userId,
  };
}

// 存储活跃会话
const sessions = new Map<string, SessionContext>();

function getSessionIdHeader(req: express.Request): string | undefined {
  const sessionId = req.headers['mcp-session-id'];
  return typeof sessionId === 'string' ? sessionId : undefined;
}

function cleanupSession(sessionId: string) {
  const session = sessions.get(sessionId);
  if (!session) return;
  sessions.delete(sessionId);
  session.server.close().catch(() => {});
}

function isSessionOwner(session: SessionContext, auth: McpAuthInfo): boolean {
  return session.auth.userId === auth.userId;
}

// 定期清理过期/空闲会话
const sessionCleanupTimer = setInterval(() => {
  const now = Date.now();
  for (const [id, ctx] of sessions) {
    if (now - ctx.createdAt > SESSION_TTL || now - ctx.lastActivityAt > SESSION_IDLE) {
      cleanupSession(id);
    }
  }
}, 60_000);
sessionCleanupTimer.unref?.();

// 定期清理 OAuth 过期数据（每6小时）
const oauthCleanupTimer = setInterval(async () => {
  try {
    await cleanupOAuthArtifactsTransactionally();
  } catch (err) {
    console.error('[OAuth cleanup] failed:', err instanceof Error ? err.message : err);
  }
}, 6 * 60 * 60 * 1000);
oauthCleanupTimer.unref?.();

function createMcpServer(auth: McpAuthInfo) {
  const server = new McpServer(
    { name: 'taibu-mcp-online', version },
    { capabilities: { tools: {} } }
  );

  // 列出工具
  server.server.setRequestHandler(ListToolsRequestSchema, async () => decorateToolListPayloadForRuntime(buildListToolsPayload()));

  // 调用工具（错误脱敏）
  server.server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    const seedScopedArgs = withSeedScope(name, args, auth);
    const { toolArgs, placeResolutionInfo } = await preprocessToolArgsForRuntimePlace(name, seedScopedArgs);

    try {
      const rawResult = await executeTool(name, toolArgs);
      const result = attachPlaceResolutionInfoToResult(rawResult, placeResolutionInfo);
      const detailLevel = normalizeTransportDetailLevel(args?.detailLevel);
      const payload = buildToolSuccessPayload(name, result, { detailLevel }) as Record<string, unknown>;
      return attachPlaceResolutionNoteToPayload(payload, placeResolutionInfo);
    } catch (error) {
      const internalMessage = error instanceof Error ? error.message : String(error);

      const userMessage = IS_PRODUCTION
        ? 'Tool execution failed'
        : `Error: ${internalMessage}`;

      return {
        content: [{ type: 'text', text: userMessage }],
        isError: true,
      };
    }
  });

  return server;
}

async function handleStatelessRequest(
  req: express.Request,
  res: express.Response,
  auth: McpAuthInfo,
  parsedBody?: unknown,
) {
  const server = createMcpServer(auth);
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
  });

  transport.onclose = () => {
    void server.close().catch(() => {});
  };
  transport.onerror = () => {
    void server.close().catch(() => {});
  };

  let closed = false;
  try {
    await server.connect(transport);
    await transport.handleRequest(req, res, parsedBody);
  } catch (error) {
    closed = true;
    await server.close().catch(() => {});
    if (!res.headersSent) {
      return res.status(500).json({
        jsonrpc: '2.0',
        error: {
          code: -32603,
          message: 'Internal server error',
        },
        id: null,
      });
    }
    throw error;
  } finally {
    if (!closed) {
      if (req.method === 'GET') {
        // SSE 长连接：连接关闭时再清理，避免提前断开流
        res.on('close', () => { void server.close().catch(() => {}); });
      } else {
        await server.close().catch(() => {});
      }
    }
  }
}

const handleMcpPost: express.RequestHandler = async (req, res) => {
  const sessionId = getSessionIdHeader(req);
  const auth = req.mcpAuth!;

  // 已有会话：复用 transport
  if (sessionId) {
    const existing = sessions.get(sessionId);
    if (!existing) {
      return res.status(404).json({ error: 'Session not found' });
    }
    if (!isSessionOwner(existing, auth)) {
      return res.status(403).json({ error: 'Session does not belong to current user' });
    }
    existing.lastActivityAt = Date.now();
    await existing.transport.handleRequest(req, res, req.body);
    return;
  }

  // 兼容无 session-id 的 stateless 客户端（例如部分 MCP 集成实现）
  if (!isInitializeRequest(req.body)) {
    await handleStatelessRequest(req, res, auth, req.body);
    return;
  }

  // 会话上限检查
  if (sessions.size >= MAX_TOTAL_SESSIONS) {
    return res.status(503).json({ error: 'Server at capacity, try again later' });
  }

  const server = createMcpServer(auth);
  const now = Date.now();
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: () => crypto.randomUUID(),
    onsessioninitialized: (initializedSessionId) => {
      sessions.set(initializedSessionId, {
        server, transport, auth,
        createdAt: now, lastActivityAt: now,
      });
    },
    onsessionclosed: (closedSessionId) => {
      cleanupSession(closedSessionId);
    },
  });

  transport.onclose = () => {
    if (transport.sessionId) {
      cleanupSession(transport.sessionId);
    }
  };

  transport.onerror = () => {
    if (transport.sessionId) {
      cleanupSession(transport.sessionId);
    }
  };

  try {
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch (error) {
    if (transport.sessionId) {
      sessions.delete(transport.sessionId);
    }
    await server.close().catch(() => {});
    if (!res.headersSent) {
      return res.status(500).json({
        jsonrpc: '2.0',
        error: {
          code: -32603,
          message: 'Internal server error',
        },
        id: null,
      });
    }
    throw error;
  }
};

const handleMcpGet: express.RequestHandler = async (req, res) => {
  const sessionId = getSessionIdHeader(req);
  const auth = req.mcpAuth!;
  if (!sessionId) {
    await handleStatelessRequest(req, res, auth);
    return;
  }

  const session = sessions.get(sessionId);
  if (!session) {
    return res.status(404).json({ error: 'Session not found' });
  }
  if (!isSessionOwner(session, auth)) {
    return res.status(403).json({ error: 'Session does not belong to current user' });
  }
  session.lastActivityAt = Date.now();

  await session.transport.handleRequest(req, res);
};

const handleMcpDelete: express.RequestHandler = async (req, res) => {
  const sessionId = getSessionIdHeader(req);
  const auth = req.mcpAuth!;
  if (!sessionId) {
    return res.status(400).json({ error: 'Missing mcp-session-id header' });
  }

  const session = sessions.get(sessionId);
  if (!session) {
    return res.status(404).json({ error: 'Session not found' });
  }
  if (!isSessionOwner(session, auth)) {
    return res.status(403).json({ error: 'Session does not belong to current user' });
  }

  await session.transport.handleRequest(req, res, req.body);
};

// Streamable HTTP - canonical MCP path + root path compatibility alias
app.post(['/', '/mcp'], originValidationMiddleware, hostValidationMiddleware, mcpAuth, rateLimitMiddleware, handleMcpPost);
app.get(['/', '/mcp'], originValidationMiddleware, hostValidationMiddleware, mcpAuth, rateLimitMiddleware, sseConnectionLimitMiddleware, handleMcpGet);
app.delete(['/', '/mcp'], originValidationMiddleware, hostValidationMiddleware, mcpAuth, rateLimitMiddleware, handleMcpDelete);

// 启动服务器
const PORT = parseInt(process.env.PORT || '3001', 10);
const HOST = process.env.MCP_HOST || '127.0.0.1';
const httpServer = app.listen(PORT, HOST, () => {
  console.log(`TaiBu MCP Server (Streamable HTTP + OAuth 2.1) running on ${HOST}:${PORT} at /mcp`);
});

// ─── 优雅关闭 ───
function gracefulShutdown(signal: string) {
  console.log(`\n[${signal}] Shutting down MCP server...`);

  // 停止接受新连接
  httpServer.close(() => {
    console.log('HTTP server closed');
  });

  // 清理所有活跃会话
  const sessionCount = sessions.size;
  for (const [id] of sessions) {
    cleanupSession(id);
  }
  console.log(`Cleaned up ${sessionCount} sessions`);

  // 给进行中的请求一点时间完成
  setTimeout(() => {
    process.exit(0);
  }, 3000);
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));
