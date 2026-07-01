/**
 * Session cookie 共享工具
 *
 * 从 /api/auth/route.ts 提取，供 OAuth 回调等场景复用
 */
import { NextResponse } from 'next/server';
import type { Session, User } from '@supabase/supabase-js';

export const ACCESS_COOKIE = 'sb-access-token';
export const REFRESH_COOKIE = 'sb-refresh-token';

export type SessionResolutionError = {
  message: string;
  status: number;
  code?: string;
};

type SessionCookieWriter = {
  set: (name: string, value: string, options: {
    httpOnly: boolean;
    secure: boolean;
    sameSite: 'lax';
    path: string;
    maxAge: number;
  }) => unknown;
  delete: (name: string) => unknown;
};

export function buildSessionFromUser(
  user: User,
  accessToken: string,
  refreshToken: string,
): Session {
  const expiresAt = Math.floor(Date.now() / 1000) + 3600;
  return {
    access_token: accessToken,
    refresh_token: refreshToken,
    token_type: 'bearer',
    expires_in: 3600,
    expires_at: expiresAt,
    user,
  };
}

type AuthSessionResolverClient = {
  auth: {
    getUser: (accessToken: string) => Promise<{
      data: { user: User | null };
      error: unknown;
    }>;
    refreshSession: (tokens: { refresh_token: string }) => Promise<{
      data: { session: Session | null };
      error: unknown;
    }>;
  };
};

const AUTH_CREDENTIAL_ERROR_PATTERNS = [
  'jwt',
  'token',
  'session',
  'expired',
  'invalid',
  'refresh token',
  'user from sub claim in jwt',
  'auth session missing',
] as const;

function getErrorString(error: unknown, key: string): string | null {
  if (!error || typeof error !== 'object' || !(key in error)) {
    return null;
  }

  const value = (error as Record<string, unknown>)[key];
  return typeof value === 'string' && value.trim().length > 0 ? value : null;
}

function getErrorNumber(error: unknown, key: string): number | null {
  if (!error || typeof error !== 'object' || !(key in error)) {
    return null;
  }

  const value = (error as Record<string, unknown>)[key];
  return typeof value === 'number' && Number.isFinite(value) ? value : null;
}

export function isCredentialAuthError(error: unknown): boolean {
  const status = getErrorNumber(error, 'status') ?? getErrorNumber(error, 'statusCode');
  if (status != null && status >= 400 && status < 500) {
    return true;
  }

  const message = getErrorString(error, 'message')?.toLowerCase() ?? '';
  const code = getErrorString(error, 'code')?.toLowerCase() ?? '';
  return AUTH_CREDENTIAL_ERROR_PATTERNS.some((pattern) => message.includes(pattern) || code.includes(pattern));
}

export function normalizeSessionResolutionError(
  error: unknown,
  fallbackMessage = '认证服务异常，请稍后重试',
): SessionResolutionError {
  const message = getErrorString(error, 'message') ?? fallbackMessage;
  const code = getErrorString(error, 'code') ?? undefined;
  const rawStatus = getErrorNumber(error, 'status') ?? getErrorNumber(error, 'statusCode');
  const status = rawStatus != null && rawStatus >= 500 ? rawStatus : 503;

  return code ? { message, status, code } : { message, status };
}

export async function resolveSessionFromTokens(
  client: AuthSessionResolverClient,
  tokens: {
    accessToken?: string | null;
    refreshToken?: string | null;
  },
): Promise<{ session: Session | null; refreshed: boolean; error: SessionResolutionError | null }> {
  const accessToken = tokens.accessToken || null;
  const refreshToken = tokens.refreshToken || null;
  let resolutionError: SessionResolutionError | null = null;

  if (accessToken) {
    const { data, error } = await client.auth.getUser(accessToken);
    if (!error && data.user) {
      return {
        session: buildSessionFromUser(data.user, accessToken, refreshToken || ''),
        refreshed: false,
        error: null,
      };
    }

    if (error && !isCredentialAuthError(error)) {
      resolutionError = normalizeSessionResolutionError(error);
    }
  }

  if (refreshToken) {
    const { data, error } = await client.auth.refreshSession({
      refresh_token: refreshToken,
    });
    if (!error && data.session) {
      return {
        session: data.session,
        refreshed: true,
        error: null,
      };
    }

    if (error && !isCredentialAuthError(error)) {
      resolutionError = normalizeSessionResolutionError(error);
    }
  }

  return { session: null, refreshed: false, error: resolutionError };
}

function applySessionCookies(writer: SessionCookieWriter, session: Session | null) {
  const secure = process.env.NODE_ENV === 'production';

  if (!session) {
    writer.delete(ACCESS_COOKIE);
    writer.delete(REFRESH_COOKIE);
    return;
  }

  writer.set(ACCESS_COOKIE, session.access_token, {
    httpOnly: true,
    secure,
    sameSite: 'lax',
    path: '/',
    maxAge: Math.max(60, session.expires_in ?? 3600),
  });
  writer.set(REFRESH_COOKIE, session.refresh_token, {
    httpOnly: true,
    secure,
    sameSite: 'lax',
    path: '/',
    maxAge: 60 * 60 * 24 * 30,
  });
}

export function writeSessionCookies(cookieStore: SessionCookieWriter, session: Session | null) {
  applySessionCookies(cookieStore, session);
}

export function setSessionCookies(response: NextResponse, session: Session | null) {
  applySessionCookies(response.cookies, session);
}
