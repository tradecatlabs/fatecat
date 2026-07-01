/**
 * MCP OAuth 数据存储层
 *
 * 实现 OAuthRegisteredClientsStore 接口 + 授权码/Token CRUD
 */

import crypto from 'crypto';
import type { OAuthClientInformationFull } from '@modelcontextprotocol/sdk/shared/auth.js';
import type { OAuthRegisteredClientsStore } from '@modelcontextprotocol/sdk/server/auth/clients.js';
import { getSupabaseClient } from '../supabase.js';
import { getRefreshTokenTTL } from './jwt.js';
import { oauthDebug, oauthError, oauthWarn } from './logger.js';

// ─── Client Store（SDK 接口）───

export class TaiBuClientsStore implements OAuthRegisteredClientsStore {
  async getClient(clientId: string): Promise<OAuthClientInformationFull | undefined> {
    let data: Record<string, unknown> | null = null;
    let error: { message?: string; code?: string } | null = null;

    try {
      const supabase = getSupabaseClient();
      const result = await supabase
        .from('mcp_oauth_clients')
        .select('*')
        .eq('client_id', clientId)
        .maybeSingle();
      data = result.data as Record<string, unknown> | null;
      error = result.error;
    } catch (cause) {
      throw new Error(`Failed to query OAuth client store: ${cause instanceof Error ? cause.message : String(cause)}`);
    }

    if (error) {
      throw new Error(`Failed to query OAuth client store: ${error.message ?? 'unknown error'} (${error.code ?? 'n/a'})`);
    }
    if (!data) {
      oauthWarn('getClient: no client found');
      return undefined;
    }

    return {
      client_id: data.client_id as string,
      client_secret: (data.client_secret as string | null) ?? undefined,
      client_id_issued_at: (data.client_id_issued_at as number | null) ?? undefined,
      client_secret_expires_at: (data.client_secret_expires_at as number | null) ?? undefined,
      redirect_uris: data.redirect_uris as string[],
      grant_types: (data.grant_types as string[] | null) ?? undefined,
      response_types: (data.response_types as string[] | null) ?? undefined,
      token_endpoint_auth_method: (data.token_endpoint_auth_method as string | null) ?? undefined,
      client_name: (data.client_name as string | null) ?? undefined,
      client_uri: (data.client_uri as string | null) ?? undefined,
      logo_uri: (data.logo_uri as string | null) ?? undefined,
      scope: (data.scope as string | null) ?? undefined,
    } as OAuthClientInformationFull;
  }

  async registerClient(
    clientData: OAuthClientInformationFull,
  ): Promise<OAuthClientInformationFull> {
    const supabase = getSupabaseClient();
    // SDK 会预先生成 client_id，优先使用；仅在缺失时自行生成
    const clientId = clientData.client_id || crypto.randomUUID();
    const issuedAt = clientData.client_id_issued_at || Math.floor(Date.now() / 1000);

    const row = {
      client_id: clientId,
      client_secret: clientData.client_secret ?? null,
      client_secret_expires_at: clientData.client_secret_expires_at ?? null,
      client_id_issued_at: issuedAt,
      redirect_uris: clientData.redirect_uris as string[],
      grant_types: clientData.grant_types ?? ['authorization_code', 'refresh_token'],
      response_types: clientData.response_types ?? ['code'],
      token_endpoint_auth_method: clientData.token_endpoint_auth_method ?? 'none',
      client_name: clientData.client_name ?? null,
      client_uri: clientData.client_uri ?? null,
      logo_uri: clientData.logo_uri ?? null,
      scope: clientData.scope ?? null,
    };

    oauthDebug('registerClient called');

    const { error } = await supabase.from('mcp_oauth_clients').insert(row);
    if (error) {
      oauthError(`registerClient failed (${error.code ?? 'n/a'})`, error.message);
      throw new Error(`Failed to register client: ${error.message}`);
    }

    oauthDebug('registerClient succeeded');

    return {
      ...clientData,
      client_id: clientId,
      client_id_issued_at: issuedAt,
    } as OAuthClientInformationFull;
  }
}

// ─── Authorization Code 存储 ───

export interface StoredAuthCode {
  code: string;
  clientId: string;
  userId: string;
  redirectUri: string;
  codeChallenge: string;
  codeChallengeMethod: string;
  scope: string | null;
  resource: string | null;
  expiresAt: Date;
}

export interface StoredRefreshToken {
  userId: string;
  clientId: string;
  scope: string | null;
  resource: string | null;
}

type SupabaseFromOnly = Pick<ReturnType<typeof getSupabaseClient>, 'from'>;
type SupabaseRpcOnly = Pick<ReturnType<typeof getSupabaseClient>, 'rpc'>;

type TransactionalAuthorizationCodeExchangeStatus = 'ok' | 'invalid_code';
type TransactionalRefreshRotationStatus = 'ok' | 'invalid_refresh_token';

export async function saveAuthorizationCode(params: {
  clientId: string;
  userId: string;
  redirectUri: string;
  codeChallenge: string;
  scope?: string;
  resource?: string;
}): Promise<string> {
  const supabase = getSupabaseClient();
  const code = crypto.randomUUID();
  const expiresAt = new Date(Date.now() + 10 * 60 * 1000); // 10 分钟

  oauthDebug('saveAuthorizationCode called');

  const { error } = await supabase.from('mcp_oauth_codes').insert({
    code,
    client_id: params.clientId,
    user_id: params.userId,
    redirect_uri: params.redirectUri,
    code_challenge: params.codeChallenge,
    code_challenge_method: 'S256',
    scope: params.scope ?? null,
    resource: params.resource ?? null,
    expires_at: expiresAt.toISOString(),
  });

  if (error) {
    oauthError(`saveAuthorizationCode failed (${error.code ?? 'n/a'})`, error.message);
    throw new Error(`Failed to save auth code: ${error.message}`);
  }
  oauthDebug('saveAuthorizationCode succeeded');
  return code;
}

function toStoredAuthCode(data: {
  code: string;
  client_id: string;
  user_id: string;
  redirect_uri: string;
  code_challenge: string;
  code_challenge_method: string;
  scope: string | null;
  resource: string | null;
  expires_at: string;
}): StoredAuthCode {
  return {
    code: data.code,
    clientId: data.client_id,
    userId: data.user_id,
    redirectUri: data.redirect_uri,
    codeChallenge: data.code_challenge,
    codeChallengeMethod: data.code_challenge_method,
    scope: data.scope,
    resource: data.resource,
    expiresAt: new Date(data.expires_at),
  };
}

export async function getAuthorizationCode(
  code: string,
  supabase: SupabaseFromOnly = getSupabaseClient(),
): Promise<StoredAuthCode | null> {
  oauthDebug('getAuthorizationCode called');
  const { data, error } = await supabase
    .from('mcp_oauth_codes')
    .select('*')
    .eq('code', code)
    .eq('used', false)
    .gt('expires_at', new Date().toISOString())
    .maybeSingle();

  if (error) {
    oauthError(`getAuthorizationCode query failed (${error.code ?? 'n/a'})`, error.message);
    return null;
  }
  if (!data) {
    oauthWarn('getAuthorizationCode: no matching code');
    return null;
  }
  oauthDebug('getAuthorizationCode succeeded');
  return toStoredAuthCode(data);
}

function getRefreshTokenExpiresAt(): string {
  const ttlMs = getRefreshTokenTTL() * 1000;
  return new Date(Date.now() + ttlMs).toISOString();
}

/**
 * 查询授权码对应的 code_challenge（不消费 code）。
 *
 * SDK 流程：先调 challengeForAuthorizationCode 做 PKCE 校验，再调
 * exchangeAuthorizationCode。真正的 code 消费和 refresh token 落库
 * 由 mcp_exchange_authorization_code RPC 在数据库事务里完成。
 */
export async function getCodeChallenge(code: string): Promise<string | null> {
  const supabase = getSupabaseClient();
  const { data, error } = await supabase
    .from('mcp_oauth_codes')
    .select('code_challenge')
    .eq('code', code)
    .eq('used', false)
    .gt('expires_at', new Date().toISOString())
    .maybeSingle();

  if (error || !data) return null;
  return data.code_challenge;
}

// ─── Refresh Token 存储 ───

export async function exchangeAuthorizationCodeTransactionally(params: {
  authorizationCode: string;
  refreshToken: string;
}, supabase: SupabaseRpcOnly = getSupabaseClient()): Promise<TransactionalAuthorizationCodeExchangeStatus> {
  const { data, error } = await supabase.rpc('mcp_exchange_authorization_code', {
    p_code: params.authorizationCode,
    p_refresh_token: params.refreshToken,
    p_expires_at: getRefreshTokenExpiresAt(),
  });

  if (error) {
    throw new Error(`Failed to exchange authorization code transactionally: ${error.message}`);
  }

  const status = (data as { status?: string } | null)?.status;
  if (status === 'ok' || status === 'invalid_code') {
    return status;
  }

  throw new Error('Unexpected response from mcp_exchange_authorization_code');
}

export async function getActiveRefreshToken(
  refreshToken: string,
  supabase: SupabaseFromOnly = getSupabaseClient(),
): Promise<StoredRefreshToken | null> {
  const { data, error } = await supabase
    .from('mcp_oauth_tokens')
    .select('user_id, client_id, scope, resource')
    .eq('refresh_token', refreshToken)
    .eq('revoked', false)
    .gt('expires_at', new Date().toISOString())
    .maybeSingle();

  if (error || !data) return null;
  return {
    userId: data.user_id,
    clientId: data.client_id,
    scope: data.scope,
    resource: data.resource,
  };
}

export async function revokeRefreshToken(refreshToken: string): Promise<void> {
  const supabase = getSupabaseClient();
  await supabase
    .from('mcp_oauth_tokens')
    .update({ revoked: true })
    .eq('refresh_token', refreshToken);
}

export async function cleanupOAuthArtifactsTransactionally(
  nowIso: string = new Date().toISOString(),
  supabase: SupabaseRpcOnly = getSupabaseClient(),
): Promise<{
  deleted_codes: number;
  deleted_tokens: number;
  deleted_clients: number;
  orphan_clients: number;
  total_clients: number;
}> {
  const { data, error } = await supabase.rpc('mcp_cleanup_oauth_artifacts', {
    p_now: nowIso,
  });

  if (error) {
    throw new Error(`Failed to cleanup oauth artifacts transactionally: ${error.message}`);
  }

  const result = data as {
    status?: string;
    deleted_codes?: number;
    deleted_tokens?: number;
    deleted_clients?: number;
    orphan_clients?: number;
    total_clients?: number;
  } | null;

  if (result?.status !== 'ok') {
    throw new Error('Unexpected response from mcp_cleanup_oauth_artifacts');
  }

  return {
    deleted_codes: result.deleted_codes ?? 0,
    deleted_tokens: result.deleted_tokens ?? 0,
    deleted_clients: result.deleted_clients ?? 0,
    orphan_clients: result.orphan_clients ?? 0,
    total_clients: result.total_clients ?? 0,
  };
}

export async function rotateRefreshTokenTransactionally(params: {
  refreshToken: string;
  newRefreshToken: string;
  scope: string;
  resource?: string;
}, supabase: SupabaseRpcOnly = getSupabaseClient()): Promise<TransactionalRefreshRotationStatus> {
  const { data, error } = await supabase.rpc('mcp_rotate_refresh_token', {
    p_refresh_token: params.refreshToken,
    p_new_refresh_token: params.newRefreshToken,
    p_scope: params.scope,
    p_resource: params.resource ?? null,
    p_expires_at: getRefreshTokenExpiresAt(),
  });

  if (error) {
    throw new Error(`Failed to rotate refresh token transactionally: ${error.message}`);
  }

  const status = (data as { status?: string } | null)?.status;
  if (status === 'ok' || status === 'invalid_refresh_token') {
    return status;
  }

  throw new Error('Unexpected response from mcp_rotate_refresh_token');
}
