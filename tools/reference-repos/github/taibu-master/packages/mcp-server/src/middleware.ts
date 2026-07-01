/**
 * MCP Server 中间件
 *
 * 挂载顺序：
 * express.json({ limit: '1mb' })
 *   → originValidationMiddleware
 *   → dualAuthMiddleware（OAuth JWT 优先，API Key fallback）
 *   → rateLimitMiddleware（userId 复合键）
 *   → sseConnectionLimitMiddleware（仅 GET）
 */

import type { Request, Response, NextFunction } from 'express';
import type { OAuthTokenVerifier } from '@modelcontextprotocol/sdk/server/auth/provider.js';
import { getSupabaseClient } from './supabase.js';
import { getCachedKey, invalidateCachedKey, setCachedKey } from './key-cache.js';

// 扩展 Express Request 类型
export interface McpAuthInfo {
  userId: string;
  keyId: string;
}

declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Express {
    interface Request {
      mcpAuth?: McpAuthInfo;
    }
  }
}

// ─── Origin 校验中间件（P0 — DNS rebinding 防护）───

export function originValidationMiddleware(req: Request, res: Response, next: NextFunction) {
  const origin = req.headers.origin;

  // 无 Origin 的非浏览器客户端正常放行
  if (!origin) return next();

  const allowedRaw = process.env.MCP_ALLOWED_ORIGINS;
  if (!allowedRaw) {
    return res.status(403).json({ error: 'Origin allowlist not configured' });
  }

  const allowed = allowedRaw.split(',').map((s) => s.trim()).filter(Boolean);
  if (allowed.length === 0) {
    return res.status(403).json({ error: 'Origin allowlist not configured' });
  }

  if (allowed.includes('*')) {
    return next();
  }

  if (!allowed.includes(origin)) {
    return res.status(403).json({ error: 'Origin not allowed' });
  }

  next();
}

// ─── Host 校验中间件（P0 — DNS rebinding 辅助防护）───

export function hostValidationMiddleware(req: Request, res: Response, next: NextFunction) {
  const host = req.headers.host;
  const allowedRaw = process.env.MCP_ALLOWED_HOSTS;

  if (!allowedRaw) return next();

  const allowed = allowedRaw.split(',').map((s) => s.trim()).filter(Boolean);
  if (allowed.length === 0) return next();

  if (!host || !allowed.includes(host)) {
    return res.status(403).json({ error: 'Host not allowed' });
  }

  next();
}

// ─── Auth 中间件（per-user key 验证）───

export function readPositiveIntEnv(name: string, fallback: number): number {
  const raw = process.env[name];
  if (!raw) return fallback;
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) return fallback;
  return parsed;
}

function extractApiKey(req: Request): string | undefined {
  // x-api-key header
  const headerKey = req.headers['x-api-key'];
  if (typeof headerKey === 'string' && headerKey) return headerKey;

  // Authorization: Bearer <key>
  const authHeader = req.headers.authorization;
  if (typeof authHeader === 'string') {
    const match = authHeader.match(/^Bearer\s+(.+)$/i);
    if (match?.[1]) {
      return match[1].trim() || undefined;
    }
  }

  return undefined;
}

async function queryActiveKey(apiKey: string): Promise<{ id: string; user_id: string } | null> {
  const supabase = getSupabaseClient();
  const { data, error } = await supabase.rpc('mcp_verify_api_key', { p_key_code: apiKey });

  if (error || !Array.isArray(data) || data.length === 0) return null;
  const first = data[0] as { key_id: string; user_id: string };
  if (!first?.key_id || !first?.user_id) return null;
  return { id: first.key_id, user_id: first.user_id };
}

async function touchLastUsedAt(keyId: string): Promise<void> {
  try {
    const supabase = getSupabaseClient();
    await supabase.rpc('mcp_touch_key_last_used', { p_key_id: keyId });
  } catch {
    // 审计字段更新失败不影响主流程
  }
}

async function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const apiKey = extractApiKey(req);

  if (!apiKey) {
    return res.status(401).json({ error: 'Missing API key' });
  }

  // Stale-while-revalidate: 缓存命中时立即放行，后台异步回源验证。
  // 若回源发现 key 已撤销，下次请求将被拒绝。
  const cached = getCachedKey(apiKey);

  try {
    if (cached) {
      // 快速路径：信任缓存，立即放行
      req.mcpAuth = { userId: cached.userId, keyId: cached.keyId };
      void touchLastUsedAt(cached.keyId);

      // 后台异步回源验证（不阻塞当前请求）
      void queryActiveKey(apiKey).then(activeKey => {
        if (!activeKey) {
          invalidateCachedKey(apiKey);
        } else if (activeKey.user_id !== cached.userId || activeKey.id !== cached.keyId) {
          // key 关联的用户变了，更新缓存
          setCachedKey(apiKey, { userId: activeKey.user_id, keyId: activeKey.id });
        }
      }).catch(() => {
        // 回源失败不影响当前请求，下次重试
      });

      return next();
    }

    // 缓存未命中：同步查询 DB
    const activeKey = await queryActiveKey(apiKey);

    if (!activeKey) {
      return res.status(401).json({ error: 'Invalid API key' });
    }

    setCachedKey(apiKey, { userId: activeKey.user_id, keyId: activeKey.id });
    req.mcpAuth = { userId: activeKey.user_id, keyId: activeKey.id };

    // 非阻塞更新 last_used_at
    void touchLastUsedAt(activeKey.id);

    next();
  } catch {
    return res.status(500).json({ error: 'Authentication service error' });
  }
}

// ─── 限流中间件（userId:ip:method 复合键）───

const rateLimitMap = new Map<string, { count: number; resetTime: number }>();
const RATE_LIMIT = 120; // 认证用户 120 次/分钟
const RATE_WINDOW = 60 * 1000;
const CLEANUP_INTERVAL = 5 * 60 * 1000;
const MAX_RATE_LIMIT_ENTRIES = 50_000;

let lastCleanup = Date.now();
function cleanupExpiredRecords() {
  const now = Date.now();
  if (now - lastCleanup < CLEANUP_INTERVAL) return;
  lastCleanup = now;
  for (const [key, record] of rateLimitMap) {
    if (now > record.resetTime) {
      rateLimitMap.delete(key);
    }
  }
}

export function rateLimitMiddleware(req: Request, res: Response, next: NextFunction) {
  cleanupExpiredRecords();

  const ip = req.ip || req.socket.remoteAddress || 'unknown';
  const userId = req.mcpAuth?.userId || 'anon';
  const method = req.method;
  // 不含 path：/ 和 /mcp 是同一服务的别名，共享配额
  const compositeKey = `${userId}:${ip}:${method}`;
  const now = Date.now();

  const record = rateLimitMap.get(compositeKey);

  if (!record || now > record.resetTime) {
    // 防止 Map 无限增长
    if (rateLimitMap.size >= MAX_RATE_LIMIT_ENTRIES) {
      cleanupExpiredRecords();
    }
    rateLimitMap.set(compositeKey, { count: 1, resetTime: now + RATE_WINDOW });
    return next();
  }

  if (record.count >= RATE_LIMIT) {
    return res.status(429).json({ error: 'Too many requests' });
  }

  record.count++;
  next();
}

// ─── SSE 并发限制中间件 ───

const sseConnections = new Map<string, number>();
const MAX_SSE_PER_USER = readPositiveIntEnv('MCP_MAX_SSE_PER_USER', 3);

export function sseConnectionLimitMiddleware(req: Request, res: Response, next: NextFunction) {
  // 仅限制 GET 请求（SSE）
  if (req.method !== 'GET') return next();

  const userId = req.mcpAuth?.userId;
  if (!userId) return next();

  const current = sseConnections.get(userId) || 0;
  if (current >= MAX_SSE_PER_USER) {
    return res.status(429).json({ error: 'Too many SSE connections' });
  }

  sseConnections.set(userId, current + 1);

  res.on('close', () => {
    const count = sseConnections.get(userId) || 1;
    if (count <= 1) {
      sseConnections.delete(userId);
    } else {
      sseConnections.set(userId, count - 1);
    }
  });

  next();
}

// ─── OAuth 端点限流（IP 维度，防暴力破解与注册滥用）───

const oauthRateLimitMap = new Map<string, { count: number; resetTime: number }>();
const OAUTH_RATE_LIMIT = 10; // 10 次/分钟（per IP per path）
const OAUTH_RATE_WINDOW = 60 * 1000;

export function oauthRateLimitMiddleware(req: Request, res: Response, next: NextFunction) {
  const ip = req.ip || req.socket.remoteAddress || 'unknown';
  const key = `oauth:${ip}:${req.path}`;
  const now = Date.now();

  const record = oauthRateLimitMap.get(key);

  if (!record || now > record.resetTime) {
    oauthRateLimitMap.set(key, { count: 1, resetTime: now + OAUTH_RATE_WINDOW });
    return next();
  }

  if (record.count >= OAUTH_RATE_LIMIT) {
    return res.status(429).json({ error: 'Too many requests, try again later' });
  }

  record.count++;
  next();
}

// 复用主限流的清理周期，顺带清理 OAuth 限流记录
const oauthCleanupTimer = setInterval(() => {
  const now = Date.now();
  for (const [key, record] of oauthRateLimitMap) {
    if (now > record.resetTime) {
      oauthRateLimitMap.delete(key);
    }
  }
}, CLEANUP_INTERVAL);
oauthCleanupTimer.unref?.();

// ─── 双模式认证中间件（OAuth JWT 优先，API Key fallback）───

export function dualAuthMiddleware(verifier: OAuthTokenVerifier) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;
    const apiKeyHeader = req.headers['x-api-key'];

    // 优先：Bearer token → JWT 验证
    if (typeof authHeader === 'string') {
      const bearerMatch = authHeader.match(/^Bearer\s+(.+)$/i);
      const token = bearerMatch?.[1]?.trim();
      if (token) {
        try {
          const authInfo = await verifier.verifyAccessToken(token);
          const userId = authInfo.extra?.userId as string | undefined;
          if (!userId) {
            return res.status(401).json({ error: 'Invalid token: missing user' });
          }
          req.mcpAuth = { userId, keyId: `oauth:${authInfo.clientId}` };
          return next();
        } catch {
          // Bearer token 存在但无效 → 不 fallback，直接拒绝
          return res.status(401).json({ error: 'Invalid or expired access token' });
        }
      }
    }

    // Fallback：x-api-key header → 旧 API Key 验证
    if (typeof apiKeyHeader === 'string' && apiKeyHeader) {
      return authMiddleware(req, res, next);
    }

    // 无认证信息
    return res.status(401).json({ error: 'Missing authentication' });
  };
}
