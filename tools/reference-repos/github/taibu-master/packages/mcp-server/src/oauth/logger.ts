const OAUTH_DEBUG_ENABLED = process.env.MCP_OAUTH_DEBUG === 'true';

export function isOAuthDebugEnabled(): boolean {
  return OAUTH_DEBUG_ENABLED;
}

export function oauthDebug(message: string): void {
  if (OAUTH_DEBUG_ENABLED) {
    console.log(`[OAuth] ${message}`);
  }
}

export function oauthWarn(message: string): void {
  console.warn(`[OAuth] ${message}`);
}

export function oauthError(message: string, error?: unknown): void {
  if (error instanceof Error) {
    console.error(`[OAuth] ${message}: ${error.message}`);
    return;
  }

  if (typeof error === 'string') {
    console.error(`[OAuth] ${message}: ${error}`);
    return;
  }

  console.error(`[OAuth] ${message}`);
}
