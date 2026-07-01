/**
 * Shared test helpers for API route tests.
 *
 * Provides reusable mock utilities so individual route tests
 * don't need to duplicate the same setup code.
 */

import { createMockSupabaseClient, FREE_USER_TABLE, type MockSupabaseConfig } from './supabase-mock';

export type { MockSupabaseConfig };
export { createMockSupabaseClient, FREE_USER_TABLE };

/** Temporarily replaces console.error with a capturing stub. */
export function captureConsoleErrors() {
    const original = console.error;
    const errors: string[] = [];
    console.error = (...args: unknown[]) => {
        errors.push(args.map(String).join(' '));
    };
    return {
        errors,
        restore: () => {
            console.error = original;
        },
    };
}

/** Standard env vars needed by most route tests. */
export function ensureRouteTestEnv() {
    process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';
    process.env.NEWAPI_API_KEY = process.env.NEWAPI_API_KEY || 'test-key';
    process.env.NEWAPI_BASE_URL = process.env.NEWAPI_BASE_URL || 'https://newapi.example';
    process.env.MINGAI_FALLBACK_MODELS_JSON = process.env.MINGAI_FALLBACK_MODELS_JSON || JSON.stringify([
        {
            id: 'deepseek-v3.2',
            name: 'DeepSeek V3.2',
            vendor: 'deepseek',
            usageType: 'chat',
            supportsReasoning: false,
        },
    ]);
}

interface RouteTestSetup {
    /** Cleanup function to call in t.after() */
    cleanup: () => void;
    /** Console error capture */
    consoleCapture: ReturnType<typeof captureConsoleErrors>;
}

interface RouteTestOptions {
    /** User ID for auth mock. Default: 'user-1' */
    userId?: string;
    /** getUserAuthInfo return value */
    authInfo?: { credits: number; effectiveMembership: string; hasCredits: boolean };
    /** useCredit return value. null = failure */
    useCreditResult?: number | null;
    /** Supabase client config */
    supabaseConfig?: MockSupabaseConfig;
    /** Mock global.fetch response */
    fetchResponse?: { ok: boolean; json: () => Promise<unknown> };
    /** Mock callAIWithReasoning */
    aiResponse?: { content: string; reasoning?: string | null };
    /** Mock callAIStream */
    aiStream?: ReadableStream<Uint8Array>;
    /** Mock createAIAnalysisConversation. Returns conv ID or captures args. */
    createConversation?: string | ((args: Record<string, unknown>) => string);
}

/**
 * Sets up common mocks for route tests.
 * Returns a cleanup function to restore all originals.
 */
export function setupRouteTest(options: RouteTestOptions = {}): RouteTestSetup {
    const consoleCapture = captureConsoleErrors();

    /* eslint-disable @typescript-eslint/no-require-imports, @typescript-eslint/no-explicit-any */
    const credits = require('../../lib/user/credits') as any;
    const supabaseModule = require('../../lib/auth') as any;
    const supabaseServerModule = require('../../lib/supabase-server') as any;
    /* eslint-enable @typescript-eslint/no-require-imports, @typescript-eslint/no-explicit-any */

    const originals: Array<() => void> = [consoleCapture.restore];

    // Auth mock
    const originalGetUser = supabaseModule.supabase.auth.getUser;
    supabaseModule.supabase.auth.getUser = async () => ({
        data: { user: { id: options.userId ?? 'user-1' } },
        error: null,
    });
    originals.push(() => { supabaseModule.supabase.auth.getUser = originalGetUser; });

    // Credits mock
    if (options.authInfo) {
        const originalGetUserAuthInfo = credits.getUserAuthInfo;
        credits.getUserAuthInfo = async () => options.authInfo;
        originals.push(() => { credits.getUserAuthInfo = originalGetUserAuthInfo; });
    }

    if (options.useCreditResult !== undefined) {
        const originalUseCredit = credits.useCredit;
        credits.useCredit = async () => options.useCreditResult;
        originals.push(() => { credits.useCredit = originalUseCredit; });
    }

    // Supabase service client mock
    if (options.supabaseConfig) {
        const originalGetServiceClient = supabaseServerModule.getSystemAdminClient;
        const mockClient = createMockSupabaseClient(options.supabaseConfig);
        supabaseServerModule.getSystemAdminClient = () => mockClient;
        originals.push(() => { supabaseServerModule.getSystemAdminClient = originalGetServiceClient; });
    }

    // Fetch mock
    if (options.fetchResponse) {
        const originalFetch = global.fetch;
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        global.fetch = async () => options.fetchResponse as any;
        originals.push(() => { global.fetch = originalFetch; });
    }

    // AI mocks
    if (options.aiResponse) {
        // eslint-disable-next-line @typescript-eslint/no-require-imports, @typescript-eslint/no-explicit-any
        const aiModule = require('../../lib/ai/ai') as any;
        const originalCallAI = aiModule.callAIWithReasoning;
        aiModule.callAIWithReasoning = async () => options.aiResponse;
        originals.push(() => { aiModule.callAIWithReasoning = originalCallAI; });
    }

    if (options.aiStream) {
        // eslint-disable-next-line @typescript-eslint/no-require-imports, @typescript-eslint/no-explicit-any
        const aiModule = require('../../lib/ai/ai') as any;
        const originalCallAIStream = aiModule.callAIStream;
        aiModule.callAIStream = async () => options.aiStream;
        originals.push(() => { aiModule.callAIStream = originalCallAIStream; });
    }

    if (options.createConversation) {
        // eslint-disable-next-line @typescript-eslint/no-require-imports, @typescript-eslint/no-explicit-any
        const aiAnalysisModule = require('../../lib/ai/ai-analysis') as any;
        const originalCreate = aiAnalysisModule.createAIAnalysisConversation;
        const handler = options.createConversation;
        aiAnalysisModule.createAIAnalysisConversation = typeof handler === 'function'
            ? async (args: Record<string, unknown>) => handler(args)
            : async () => handler;
        originals.push(() => { aiAnalysisModule.createAIAnalysisConversation = originalCreate; });
    }

    return {
        consoleCapture,
        cleanup: () => {
            for (const restore of originals) restore();
        },
    };
}
