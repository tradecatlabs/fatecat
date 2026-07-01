/**
 * MCP OAuth JWT 签发与验证
 *
 * 使用 jose 库 + HS256 对称签名
 */

import { SignJWT, jwtVerify, errors as joseErrors } from 'jose';
import crypto from 'crypto';
import type { AuthInfo } from '@modelcontextprotocol/sdk/server/auth/types.js';

function getSecret(): Uint8Array {
  const raw = process.env.MCP_JWT_SECRET;
  if (!raw || raw.length < 32) {
    throw new Error('MCP_JWT_SECRET must be at least 32 characters');
  }
  return new TextEncoder().encode(raw);
}

function getIssuer(): string {
  return process.env.MCP_ISSUER_URL || 'https://mcp.mingai.fun';
}

function normalizeAudience(value: string): string | null {
  const trimmed = value.trim();
  if (!trimmed) return null;

  try {
    return new URL(trimmed).href;
  } catch {
    return trimmed;
  }
}

export function getAllowedTokenAudiences(issuerInput?: string | URL): string[] {
  const issuer = issuerInput
    ? normalizeAudience(issuerInput.toString()) ?? getIssuer()
    : getIssuer();

  const defaults: string[] = [
    issuer,
    (() => {
      try {
        return new URL('/mcp', issuer).href;
      } catch {
        return issuer;
      }
    })(),
  ];

  const envValue = process.env.MCP_ALLOWED_TOKEN_AUDIENCES;
  const candidates = envValue?.trim()
    ? [
        ...defaults,
        ...envValue.split(',').map((item) => item.trim()).filter(Boolean),
      ]
    : defaults;

  const set = new Set<string>();
  for (const candidate of candidates) {
    const normalized = normalizeAudience(candidate);
    if (normalized) set.add(normalized);
  }
  return [...set];
}

function getAccessTokenTTL(): number {
  const raw = process.env.MCP_ACCESS_TOKEN_TTL;
  if (raw) {
    const n = Number.parseInt(raw, 10);
    if (Number.isFinite(n) && n > 0) return n;
  }
  return 3600; // 1h
}

function getRefreshTokenTTL(): number {
  const raw = process.env.MCP_REFRESH_TOKEN_TTL;
  if (raw) {
    const n = Number.parseInt(raw, 10);
    if (Number.isFinite(n) && n > 0) return n;
  }
  return 2592000; // 30d
}

export async function signAccessToken(
  userId: string,
  clientId: string,
  scope: string,
  resource?: string,
): Promise<{ token: string; expiresIn: number }> {
  const ttl = getAccessTokenTTL();
  const issuer = getIssuer();
  const audience = resource
    ? normalizeAudience(resource) ?? issuer
    : issuer;

  const token = await new SignJWT({
    sub: userId,
    client_id: clientId,
    scope,
  })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuer(issuer)
    .setAudience(audience)
    .setIssuedAt()
    .setExpirationTime(`${ttl}s`)
    .sign(getSecret());

  return { token, expiresIn: ttl };
}

export async function verifyAccessToken(token: string): Promise<AuthInfo> {
  const issuer = getIssuer();
  const audiences = getAllowedTokenAudiences(issuer);
  if (audiences.length === 0) audiences.push(issuer);
  const expectedAudience = audiences.length > 1 ? audiences : audiences[0];

  try {
    const { payload } = await jwtVerify(token, getSecret(), {
      issuer,
      audience: expectedAudience,
    });

    const expiresAt = typeof payload.exp === 'number' ? payload.exp : undefined;
    const scopes = typeof payload.scope === 'string' ? payload.scope.split(' ').filter(Boolean) : [];

    return {
      token,
      clientId: (payload.client_id as string) || '',
      scopes,
      expiresAt,
      extra: { userId: payload.sub },
    };
  } catch (err) {
    if (err instanceof joseErrors.JWTExpired) {
      throw new Error('Access token expired');
    }
    throw new Error('Invalid access token');
  }
}

export function generateRefreshToken(): string {
  return crypto.randomUUID();
}

export { getRefreshTokenTTL };
