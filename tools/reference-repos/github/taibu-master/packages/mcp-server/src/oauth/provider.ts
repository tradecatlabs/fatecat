/**
 * MCP OAuth Server Provider 实现
 *
 * 实现 MCP SDK 的 OAuthServerProvider 接口
 */

import type { Response } from 'express';
import type { OAuthServerProvider, AuthorizationParams } from '@modelcontextprotocol/sdk/server/auth/provider.js';
import type { OAuthRegisteredClientsStore } from '@modelcontextprotocol/sdk/server/auth/clients.js';
import type { OAuthClientInformationFull, OAuthTokens, OAuthTokenRevocationRequest } from '@modelcontextprotocol/sdk/shared/auth.js';
import type { AuthInfo } from '@modelcontextprotocol/sdk/server/auth/types.js';

import { TaiBuClientsStore } from './store.js';
import {
  getCodeChallenge,
  getAuthorizationCode,
  exchangeAuthorizationCodeTransactionally,
  getActiveRefreshToken,
  rotateRefreshTokenTransactionally,
  revokeRefreshToken,
  type StoredAuthCode,
  type StoredRefreshToken,
} from './store.js';
import {
  signAccessToken,
  verifyAccessToken as jwtVerify,
  generateRefreshToken,
} from './jwt.js';
import { renderAuthorizePage } from './authorize-page.js';
import { oauthDebug, oauthError } from './logger.js';

function normalizeResource(resource?: URL | string | null): string | null {
  if (!resource) return null;

  const raw = typeof resource === 'string' ? resource : resource.href;
  try {
    return new URL(raw).href;
  } catch {
    return raw;
  }
}

function parseScopes(scope: string | null | undefined): string[] {
  if (!scope) return [];
  return [...new Set(scope.split(/\s+/).map((item) => item.trim()).filter(Boolean))];
}

function resolveRefreshScope(storedScope: string | null, requestedScopes?: string[]): string {
  const grantedScopes = parseScopes(storedScope || 'mcp:tools');
  if (grantedScopes.length === 0) grantedScopes.push('mcp:tools');
  const requested = [...new Set((requestedScopes ?? []).map((item) => item.trim()).filter(Boolean))];

  if (requested.length === 0) {
    return grantedScopes.join(' ');
  }

  const grantedSet = new Set(grantedScopes);
  if (requested.some((scope) => !grantedSet.has(scope))) {
    throw new Error('Refresh token scope escalation not allowed');
  }
  return requested.join(' ');
}

function resolveBoundResource(
  storedResource: string | null,
  requestedResource?: URL,
  tokenType: 'Authorization code' | 'Refresh token' = 'Authorization code',
): string | undefined {
  const bound = normalizeResource(storedResource);
  const requested = normalizeResource(requestedResource);

  if (requested && requested !== bound) {
    throw new Error(`${tokenType} resource mismatch`);
  }
  return bound ?? undefined;
}

type OAuthProviderDeps = {
  getCodeChallenge: (code: string) => Promise<string | null>;
  getAuthorizationCode: (code: string) => Promise<StoredAuthCode | null>;
  exchangeAuthorizationCodeTransactionally: (params: {
    authorizationCode: string;
    refreshToken: string;
  }) => Promise<'ok' | 'invalid_code'>;
  getActiveRefreshToken: (refreshToken: string) => Promise<StoredRefreshToken | null>;
  rotateRefreshTokenTransactionally: (params: {
    refreshToken: string;
    newRefreshToken: string;
    scope: string;
    resource?: string;
  }) => Promise<'ok' | 'invalid_refresh_token'>;
  revokeRefreshToken: (refreshToken: string) => Promise<void>;
  signAccessToken: (
    userId: string,
    clientId: string,
    scope: string,
    resource?: string,
  ) => Promise<{ token: string; expiresIn: number }>;
  verifyAccessToken: (token: string) => Promise<AuthInfo>;
  generateRefreshToken: () => string;
};

export class TaiBuOAuthProvider implements OAuthServerProvider {
  private _clientsStore = new TaiBuClientsStore();
  private deps: OAuthProviderDeps;

  constructor(deps?: Partial<OAuthProviderDeps>) {
    this.deps = {
      getCodeChallenge,
      getAuthorizationCode,
      exchangeAuthorizationCodeTransactionally,
      getActiveRefreshToken,
      rotateRefreshTokenTransactionally,
      revokeRefreshToken,
      signAccessToken,
      verifyAccessToken: jwtVerify,
      generateRefreshToken,
      ...deps,
    };
  }

  get clientsStore(): OAuthRegisteredClientsStore {
    return this._clientsStore;
  }

  /**
   * 渲染授权登录页面
   *
   * SDK 的 authorizationHandler 在验证 client_id / redirect_uri / PKCE 参数后调用此方法。
   * 我们渲染 HTML 登录表单，表单 POST 到 /oauth/login（自定义路由）。
   */
  async authorize(
    client: OAuthClientInformationFull,
    params: AuthorizationParams,
    res: Response,
  ): Promise<void> {
    const html = renderAuthorizePage({
      clientName: client.client_name,
      scopes: params.scopes ?? [],
      clientId: client.client_id,
      redirectUri: params.redirectUri,
      codeChallenge: params.codeChallenge,
      codeChallengeMethod: 'S256',
      state: params.state,
      scope: params.scopes?.join(' '),
      resource: params.resource?.href,
    });

    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.status(200).send(html);
  }

  /**
   * 返回授权码对应的 code_challenge
   */
  async challengeForAuthorizationCode(
    _client: OAuthClientInformationFull,
    authorizationCode: string,
  ): Promise<string> {
    oauthDebug('challengeForAuthorizationCode called');
    const challenge = await this.deps.getCodeChallenge(authorizationCode);
    if (!challenge) {
      oauthError('challengeForAuthorizationCode failed: code not found or expired');
      throw new Error('Authorization code not found or expired');
    }
    return challenge;
  }

  /**
   * 用授权码换取 access_token + refresh_token
   */
  async exchangeAuthorizationCode(
    client: OAuthClientInformationFull,
    authorizationCode: string,
    _codeVerifier?: string,
    redirectUri?: string,
    resource?: URL,
  ): Promise<OAuthTokens> {
    oauthDebug('exchangeAuthorizationCode called');
    const stored = await this.deps.getAuthorizationCode(authorizationCode);
    if (!stored) {
      oauthError('exchangeAuthorizationCode failed: code not found/expired/used');
      throw new Error('Invalid or expired authorization code');
    }

    if (stored.clientId !== client.client_id) {
      throw new Error('Authorization code was issued to a different client');
    }

    if (redirectUri && stored.redirectUri !== redirectUri) {
      throw new Error('Authorization code redirect_uri mismatch');
    }

    const scope = stored.scope || 'mcp:tools';
    const boundResource = resolveBoundResource(stored.resource, resource, 'Authorization code');
    const { token: accessToken, expiresIn } = await this.deps.signAccessToken(
      stored.userId,
      client.client_id,
      scope,
      boundResource,
    );

    const refreshToken = this.deps.generateRefreshToken();
    const exchangeStatus = await this.deps.exchangeAuthorizationCodeTransactionally({
      authorizationCode,
      refreshToken,
    });
    if (exchangeStatus !== 'ok') {
      oauthError('exchangeAuthorizationCode failed: code lost before transactional exchange');
      throw new Error('Invalid or expired authorization code');
    }

    oauthDebug('exchangeAuthorizationCode succeeded');
    return {
      access_token: accessToken,
      token_type: 'bearer',
      expires_in: expiresIn,
      refresh_token: refreshToken,
      scope,
    };
  }

  /**
   * 用 refresh_token 换取新的 access_token（token rotation）
   */
  async exchangeRefreshToken(
    client: OAuthClientInformationFull,
    refreshToken: string,
    scopes?: string[],
    resource?: URL,
  ): Promise<OAuthTokens> {
    const stored = await this.deps.getActiveRefreshToken(refreshToken);
    if (!stored) throw new Error('Invalid or expired refresh token');

    if (stored.clientId !== client.client_id) {
      throw new Error('Refresh token was issued to a different client');
    }

    const scope = resolveRefreshScope(stored.scope, scopes);
    const boundResource = resolveBoundResource(stored.resource, resource, 'Refresh token');

    const { token: accessToken, expiresIn } = await this.deps.signAccessToken(
      stored.userId,
      client.client_id,
      scope,
      boundResource,
    );

    const newRefreshToken = this.deps.generateRefreshToken();
    const rotationStatus = await this.deps.rotateRefreshTokenTransactionally({
      refreshToken,
      newRefreshToken,
      scope,
      resource: boundResource,
    });
    if (rotationStatus !== 'ok') {
      throw new Error('Invalid or expired refresh token');
    }

    return {
      access_token: accessToken,
      token_type: 'bearer',
      expires_in: expiresIn,
      refresh_token: newRefreshToken,
      scope,
    };
  }

  /**
   * 验证 JWT access_token
   */
  async verifyAccessToken(token: string): Promise<AuthInfo> {
    try {
      return await this.deps.verifyAccessToken(token);
    } catch (err) {
      oauthError('verifyAccessToken failed', err);
      throw err;
    }
  }

  /**
   * 吊销 token
   */
  async revokeToken(
    _client: OAuthClientInformationFull,
    request: OAuthTokenRevocationRequest,
  ): Promise<void> {
    // 仅处理 refresh_token 吊销（access_token 是 JWT，无法主动吊销）
    if (request.token_type_hint === 'access_token') return;
    await this.deps.revokeRefreshToken(request.token);
  }
}
