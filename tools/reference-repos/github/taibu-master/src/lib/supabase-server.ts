/**
 * Supabase 服务端特权客户端
 *
 * 不再依赖 service role key：
 * 使用 anon key + 系统管理员会话 access token（RLS + admin policy）。
 */

import { createClient, type Session, type SupabaseClient } from '@supabase/supabase-js';
import { getSupabaseAnonKey, getSupabaseAuthAdminKey, getSupabaseUrl } from '@/lib/supabase-env';

let serviceClient: SupabaseClient | null = null;
let authClient: SupabaseClient | null = null;
let authAdminClient: SupabaseClient | null = null;

let cachedAccessToken: string | null = null;
let cachedAccessTokenExpiresAt = 0;
let tokenPromise: Promise<string | null> | null = null;
let hasWarnedMissingSystemSession = false;
const SYSTEM_ADMIN_SESSION_REQUIRED = process.env.NODE_ENV === 'production';
import { IS_NODE_TEST_RUNTIME } from '@/lib/runtime';
const MISSING_SYSTEM_ADMIN_CREDENTIALS_ERROR = 'Missing SUPABASE_SYSTEM_ADMIN_EMAIL or SUPABASE_SYSTEM_ADMIN_PASSWORD';

function getSystemAuthClient(): SupabaseClient {
    if (authClient) return authClient;

    authClient = createClient(getSupabaseUrl(), getSupabaseAnonKey(), {
        auth: { persistSession: false, autoRefreshToken: false },
    });
    return authClient;
}

async function signInSystemAdmin(): Promise<Session | null> {
    const email = process.env.SUPABASE_SYSTEM_ADMIN_EMAIL;
    const password = process.env.SUPABASE_SYSTEM_ADMIN_PASSWORD;

    if (!email || !password) {
        if (SYSTEM_ADMIN_SESSION_REQUIRED) {
            throw new Error(MISSING_SYSTEM_ADMIN_CREDENTIALS_ERROR);
        }
        return null;
    }

    const client = getSystemAuthClient();
    const { data, error } = await client.auth.signInWithPassword({ email, password });

    if (error || !data.session) {
        if (SYSTEM_ADMIN_SESSION_REQUIRED) {
            throw new Error('[supabase-server] Failed to sign in system admin session');
        }
        console.error('[supabase-server] Failed to sign in system admin:', error);
        return null;
    }

    return data.session;
}

async function getSystemAccessToken(): Promise<string | null> {
    const now = Date.now();
    if (cachedAccessToken && cachedAccessTokenExpiresAt - now > 60_000) {
        return cachedAccessToken;
    }

    if (tokenPromise) return tokenPromise;

    tokenPromise = (async () => {
        const session = await signInSystemAdmin();
        if (!session) return null;

        cachedAccessToken = session.access_token;
        cachedAccessTokenExpiresAt = (session.expires_at ?? Math.floor(now / 1000) + 3000) * 1000;
        return cachedAccessToken;
    })();

    try {
        return await tokenPromise;
    } finally {
        tokenPromise = null;
    }
}

/**
 * 获取服务端 Supabase 客户端（系统管理员会话）
 * 使用单例避免重复构建；token 由 accessToken 回调按需获取。
 */
export function getSystemAdminClient(): SupabaseClient {
    if (serviceClient) return serviceClient;

    const url = getSupabaseUrl();
    const anonKey = getSupabaseAnonKey();

    serviceClient = createClient(url, anonKey, {
        auth: { persistSession: false, autoRefreshToken: false },
        accessToken: async () => {
            const token = await getSystemAccessToken();
            if (!token && !hasWarnedMissingSystemSession && !IS_NODE_TEST_RUNTIME) {
                hasWarnedMissingSystemSession = true;
                const warning = SYSTEM_ADMIN_SESSION_REQUIRED
                    ? `[supabase-server] ${MISSING_SYSTEM_ADMIN_CREDENTIALS_ERROR}`
                    : '[supabase-server] Missing system admin session config, privileged queries may fail with RLS';
                console.warn(warning);
            }
            return token;
        },
    });

    return serviceClient;
}

/**
 * 获取专用 Auth 管理客户端。
 * 仅用于 auth.admin.* 管理接口，避免与 accessToken 客户端职责混淆。
 */
export function getAuthAdminClient(): SupabaseClient | null {
    if (authAdminClient) return authAdminClient;

    const adminKey = getSupabaseAuthAdminKey();
    if (!adminKey) {
        return null;
    }

    authAdminClient = createClient(getSupabaseUrl(), adminKey, {
        auth: { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false },
    });

    return authAdminClient;
}
