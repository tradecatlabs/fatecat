import type { OAuthClientInformationFull } from '@modelcontextprotocol/sdk/shared/auth.js';

type LoginValidationInput = {
  client: OAuthClientInformationFull;
  redirectUri: string;
  scope?: string;
  resource?: string;
  issuerUrl: URL;
  allowedAudiences: string[];
};

type LoginValidationSuccess = {
  ok: true;
  value: {
    redirectUri: string;
    scope: string;
    scopes: string[];
    resource?: string;
  };
};

type LoginValidationFailure = {
  ok: false;
  error: 'Invalid redirect_uri' | 'Invalid scope' | 'Invalid resource';
};

export type LoginValidationResult = LoginValidationSuccess | LoginValidationFailure;

function normalizeUrl(input: string): string | null {
  if (!input) return null;
  try {
    return new URL(input).href;
  } catch {
    return null;
  }
}

function parseScopes(raw: string | undefined, fallback: string[]): string[] {
  const base = raw?.trim()
    ? raw.trim().split(/\s+/)
    : fallback;

  const deduped = new Set<string>();
  for (const scope of base) {
    const s = scope.trim();
    if (!s) continue;
    deduped.add(s);
  }
  return [...deduped];
}

function normalizeAudiences(values: string[]): Set<string> {
  const normalized = new Set<string>();
  for (const value of values) {
    const uri = normalizeUrl(value);
    if (uri) normalized.add(uri);
  }
  return normalized;
}

export function validateOAuthLoginRequest(input: LoginValidationInput): LoginValidationResult {
  const redirectUri = normalizeUrl(input.redirectUri);
  if (!redirectUri) {
    return { ok: false, error: 'Invalid redirect_uri' };
  }

  const registeredRedirects = new Set(
    (input.client.redirect_uris ?? [])
      .map((uri) => normalizeUrl(uri))
      .filter((uri): uri is string => Boolean(uri))
  );

  if (!registeredRedirects.has(redirectUri)) {
    return { ok: false, error: 'Invalid redirect_uri' };
  }

  const requestedScopes = parseScopes(input.scope, ['mcp:tools']);
  const allowedScopes = parseScopes(input.client.scope ?? undefined, ['mcp:tools']);
  if (requestedScopes.some((scope) => !allowedScopes.includes(scope))) {
    return { ok: false, error: 'Invalid scope' };
  }

  let normalizedResource: string | undefined;
  if (input.resource) {
    normalizedResource = normalizeUrl(input.resource) ?? undefined;
    if (!normalizedResource) {
      return { ok: false, error: 'Invalid resource' };
    }

    const allowedAudiences = normalizeAudiences(input.allowedAudiences);
    if (allowedAudiences.size === 0) {
      const fallback = normalizeUrl(input.issuerUrl.href);
      if (fallback) allowedAudiences.add(fallback);
    }

    if (!allowedAudiences.has(normalizedResource)) {
      return { ok: false, error: 'Invalid resource' };
    }
  }

  return {
    ok: true,
    value: {
      redirectUri,
      scopes: requestedScopes,
      scope: requestedScopes.join(' '),
      resource: normalizedResource,
    },
  };
}
