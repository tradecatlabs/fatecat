import { test } from 'node:test';
import assert from 'node:assert/strict';
import { NextRequest } from 'next/server';

process.env.NEXT_PUBLIC_SUPABASE_URL = 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon';
process.env.INTERNAL_API_SECRET = 'internal-secret';

const waitForMicrotask = () => new Promise((resolve) => setTimeout(resolve, 0));

interface MockState {
    authInfoCalls: number;
    useCreditCalls: number;
    addCreditCalls: number;
    aiUiCalls: number;
    rateLimitCalls: number;
    rateLimitEndpoint: string | null;
}

function createUIChunkStream(chunks: Array<Record<string, unknown>>): ReadableStream<Record<string, unknown>> {
    return new ReadableStream<Record<string, unknown>>({
        start(controller) {
            for (const chunk of chunks) {
                controller.enqueue(chunk);
            }
            controller.close();
        },
    });
}

function createMockUIMessageResult(
    chunks: Array<Record<string, unknown>>,
    responseMessage: { parts: Array<Record<string, unknown>> },
    finishReason: string = 'stop',
) {
    return {
        toUIMessageStreamResponse(options?: {
            headers?: Record<string, string>;
            messageMetadata?: (input: { part: { type: string } }) => unknown;
            onFinish?: (event: {
                responseMessage: { parts: Array<Record<string, unknown>> };
                finishReason?: string;
                isAborted: boolean;
                isContinuation: boolean;
                messages: Array<{ parts: Array<Record<string, unknown>> }>;
            }) => PromiseLike<void> | void;
        }) {
            const encoder = new TextEncoder();
            const stream = new ReadableStream<Uint8Array>({
                async start(controller) {
                    const metadata = options?.messageMetadata?.({ part: { type: 'start' } });
                    if (metadata) {
                        controller.enqueue(encoder.encode(`data: ${JSON.stringify({ type: 'start', messageMetadata: metadata })}\n\n`));
                    }
                    for (const chunk of chunks) {
                        controller.enqueue(encoder.encode(`data: ${JSON.stringify(chunk)}\n\n`));
                    }
                    await options?.onFinish?.({
                        responseMessage,
                        finishReason,
                        isAborted: false,
                        isContinuation: false,
                        messages: [responseMessage],
                    });
                    controller.enqueue(encoder.encode('data: [DONE]\n\n'));
                    controller.close();
                },
            });
            return new Response(stream, {
                headers: {
                    'Content-Type': 'text/event-stream',
                    'Cache-Control': 'no-cache, no-transform',
                    'Connection': 'keep-alive',
                    'X-Accel-Buffering': 'no',
                    'x-vercel-ai-ui-message-stream': 'v1',
                    ...(options?.headers || {}),
                },
            });
        },
    };
}

function setupRouteMocks(
    t: { after: (fn: () => void) => void },
    streamBody: ReadableStream<unknown>
): MockState {
    const routeModulePath = require.resolve('../app/api/chat/route');
    const directPrepareRouteModulePath = require.resolve('../app/api/chat/direct/prepare/route');
    const requestModulePath = require.resolve('../lib/server/chat/request');
    const aiModule = require('../lib/ai/ai') as any;
    const creditsModule = require('../lib/user/credits') as any;
    const aiConfigServerModule = require('../lib/server/ai-config') as any;
    const aiAccessModule = require('../lib/ai/ai-access') as any;
    const promptBuilderModule = require('../lib/ai/prompt-builder') as any;
    const supabaseServerModule = require('../lib/supabase-server') as any;
    const apiUtilsModule = require('../lib/api-utils') as any;
    const rateLimitModule = require('../lib/rate-limit') as any;

    const originalCallAIStream = aiModule.callAIStream;
    const originalCallAIUIMessageResult = aiModule.callAIUIMessageResult;
    const originalGetUserAuthInfo = creditsModule.getUserAuthInfo;
    const originalAttemptCreditUse = creditsModule.attemptCreditUse;
    const originalUseCredit = creditsModule.useCredit;
    const originalRefundCreditsOrLog = creditsModule.refundCreditsOrLog;
    const originalAddCredits = creditsModule.addCredits;
    const originalGetModelConfigAsync = aiConfigServerModule.getModelConfigAsync;
    const originalGetDefaultModelConfigAsync = aiConfigServerModule.getDefaultModelConfigAsync;
    const originalIsModelAllowedForMembership = aiAccessModule.isModelAllowedForMembership;
    const originalIsReasoningAllowedForMembership = aiAccessModule.isReasoningAllowedForMembership;
    const originalBuildPromptWithSources = promptBuilderModule.buildPromptWithSources;
    const originalBuildMinimalChatSystemPrompt = promptBuilderModule.buildMinimalChatSystemPrompt;
    const originalGetPromptBudget = promptBuilderModule.calculatePromptBudget;
    const originalResolvePersonalities = promptBuilderModule.resolvePersonalities;
    const originalGetServiceClient = supabaseServerModule.getSystemAdminClient;
    const originalRequireUserContext = apiUtilsModule.requireUserContext;
    const originalCheckRateLimit = rateLimitModule.checkRateLimit;

    const state: MockState = {
        authInfoCalls: 0,
        useCreditCalls: 0,
        addCreditCalls: 0,
        aiUiCalls: 0,
        rateLimitCalls: 0,
        rateLimitEndpoint: null,
    };

    aiModule.callAIStream = async () => createUIChunkStream([]);
    aiModule.callAIUIMessageResult = async () => {
        state.aiUiCalls += 1;
        const chunks: Array<Record<string, unknown>> = [];
        const reader = streamBody.getReader();
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value as Record<string, unknown>);
        }
        reader.releaseLock();

        const text = chunks
            .filter((chunk) => chunk.type === 'text-delta' && typeof chunk.delta === 'string')
            .map((chunk) => String(chunk.delta))
            .join('');
        const reasoning = chunks
            .filter((chunk) => chunk.type === 'reasoning-delta' && typeof chunk.delta === 'string')
            .map((chunk) => String(chunk.delta))
            .join('');
        const responseParts: Array<Record<string, unknown>> = [];
        if (text) {
            responseParts.push({ type: 'text', text, state: 'done' });
        }
        if (reasoning) {
            responseParts.push({ type: 'reasoning', text: reasoning, state: 'done' });
        }

        return createMockUIMessageResult(chunks, { parts: responseParts });
    };
    creditsModule.getUserAuthInfo = async () => {
        state.authInfoCalls += 1;
        return {
            credits: 1,
            effectiveMembership: 'free',
            hasCredits: true,
        };
    };
    creditsModule.useCredit = async () => {
        state.useCreditCalls += 1;
        return 0;
    };
    creditsModule.attemptCreditUse = async () => {
        state.useCreditCalls += 1;
        return {
            ok: true,
            remaining: 0,
        };
    };
    creditsModule.addCredits = async () => {
        state.addCreditCalls += 1;
        return 1;
    };
    creditsModule.refundCreditsOrLog = async () => {
        state.addCreditCalls += 1;
        return true;
    };

    const mockModelConfig = {
        id: 'deepseek-chat',
        modelKey: 'deepseek-chat',
        vendor: 'deepseek',
        supportsReasoning: true,
        supportsVision: false,
        requiredTier: 'free',
    };
    aiConfigServerModule.getModelConfigAsync = async () => mockModelConfig;
    aiConfigServerModule.getDefaultModelConfigAsync = async () => mockModelConfig;
    aiAccessModule.isModelAllowedForMembership = () => true;
    aiAccessModule.isReasoningAllowedForMembership = () => true;

    promptBuilderModule.calculatePromptBudget = async () => 1024;
    promptBuilderModule.resolvePersonalities = () => ({ personalities: ['general'] });
    promptBuilderModule.buildMinimalChatSystemPrompt = () => ({
        systemPrompt: '',
        personalities: ['general'],
    });
    promptBuilderModule.buildPromptWithSources = async () => ({
        userMessagePrefix: '',
        sources: [],
        diagnostics: [],
        totalTokens: 0,
        budgetTotal: 0,
        userMessageTokens: 0,
        systemPrompt: '',
    });
    apiUtilsModule.requireUserContext = async () => ({
        user: { id: 'user-1' },
        supabase: {
            auth: {
                getSession: async () => ({ data: { session: null } }),
            },
        },
    });
    rateLimitModule.checkRateLimit = async (_identifier: string, endpoint: string) => {
        state.rateLimitCalls += 1;
        state.rateLimitEndpoint = endpoint;
        return {
            allowed: true,
            remaining: 19,
            resetAt: new Date(Date.now() + 60_000),
        };
    };

    supabaseServerModule.getSystemAdminClient = () => ({
        auth: {
            getUser: async () => ({ data: { user: { id: 'user-1' } }, error: null }),
        },
        rpc: async () => ({
            data: {
                allowed: true,
                remaining: 19,
                reset_at: new Date(Date.now() + 60_000).toISOString(),
            },
            error: null,
        }),
        from: (table: string) => {
            if (table === 'user_settings') {
                return {
                    select: () => ({
                        eq: () => ({
                            maybeSingle: async () => ({ data: null, error: null }),
                        }),
                    }),
                };
            }
            if (table === 'knowledge_bases') {
                return {
                    select: () => ({
                        eq: () => ({
                            in: async () => ({ data: [], error: null }),
                        }),
                    }),
                };
            }
            return {
                select: () => ({
                    eq: () => ({
                        maybeSingle: async () => ({ data: null, error: null }),
                    }),
                }),
            };
        },
    });

    delete require.cache[routeModulePath];
    delete require.cache[directPrepareRouteModulePath];
    delete require.cache[requestModulePath];

    t.after(() => {
        aiModule.callAIStream = originalCallAIStream;
        aiModule.callAIUIMessageResult = originalCallAIUIMessageResult;
        creditsModule.getUserAuthInfo = originalGetUserAuthInfo;
        creditsModule.attemptCreditUse = originalAttemptCreditUse;
        creditsModule.useCredit = originalUseCredit;
        creditsModule.refundCreditsOrLog = originalRefundCreditsOrLog;
        creditsModule.addCredits = originalAddCredits;
        aiConfigServerModule.getModelConfigAsync = originalGetModelConfigAsync;
        aiConfigServerModule.getDefaultModelConfigAsync = originalGetDefaultModelConfigAsync;
        aiAccessModule.isModelAllowedForMembership = originalIsModelAllowedForMembership;
        aiAccessModule.isReasoningAllowedForMembership = originalIsReasoningAllowedForMembership;
        promptBuilderModule.buildPromptWithSources = originalBuildPromptWithSources;
        promptBuilderModule.buildMinimalChatSystemPrompt = originalBuildMinimalChatSystemPrompt;
        promptBuilderModule.calculatePromptBudget = originalGetPromptBudget;
        promptBuilderModule.resolvePersonalities = originalResolvePersonalities;
        supabaseServerModule.getSystemAdminClient = originalGetServiceClient;
        apiUtilsModule.requireUserContext = originalRequireUserContext;
        rateLimitModule.checkRateLimit = originalCheckRateLimit;
        delete require.cache[routeModulePath];
        delete require.cache[directPrepareRouteModulePath];
        delete require.cache[requestModulePath];
    });

    return state;
}

function createChatRequest() {
    return new NextRequest('http://localhost/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer test-token',
        },
        body: JSON.stringify({
            stream: true,
            messages: [
                {
                    id: 'm1',
                    role: 'user',
                    content: '你好',
                    createdAt: new Date().toISOString(),
                },
            ],
        }),
    });
}

function createByokChatRequest() {
    return new NextRequest('http://localhost/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer test-token',
        },
        body: JSON.stringify({
            stream: true,
            customProvider: {
                apiUrl: 'https://8.8.8.8/v1',
                apiKey: 'sk-test',
                modelId: 'gpt-4.1-mini',
            },
            messages: [
                {
                    id: 'm1',
                    role: 'user',
                    content: '你好',
                    createdAt: new Date().toISOString(),
                },
            ],
        }),
    });
}

function createDirectPrepareRequest() {
    return new NextRequest('http://localhost/api/chat/direct/prepare', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer test-token',
        },
        body: JSON.stringify({
            messages: [
                {
                    id: 'm1',
                    role: 'user',
                    content: '你好',
                    createdAt: new Date().toISOString(),
                },
            ],
            model: 'gpt-4.1-mini',
            reasoning: false,
            stream: true,
        }),
    });
}

function createInvalidJsonRequest(url: string) {
    return new NextRequest(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer test-token',
        },
        body: '{invalid-json',
    });
}

test('chat route does not charge when stream ends before visible content', async (t) => {
    const streamBody = createUIChunkStream([
        { type: 'reasoning-delta', id: 'r1', delta: 'thinking' },
    ]);
    const state = setupRouteMocks(t, streamBody);
    const { POST } = await import('../app/api/chat/route');

    const response = await POST(createChatRequest());
    await response.text();
    await waitForMicrotask();

    assert.equal(state.authInfoCalls, 1);
    assert.equal(state.useCreditCalls, 1);
    assert.equal(state.addCreditCalls, 1);
});

test('chat route blocks before deduction when combined auth info reports no credits', async (t) => {
    const streamBody = createUIChunkStream([
        { type: 'text-delta', id: 't1', delta: '你好' },
    ]);
    const state = setupRouteMocks(t, streamBody);
    const creditsModule = require('../lib/user/credits') as any;
    creditsModule.getUserAuthInfo = async () => {
        state.authInfoCalls += 1;
        return {
            credits: 0,
            effectiveMembership: 'free',
            hasCredits: false,
        };
    };

    const { POST } = await import('../app/api/chat/route');

    const response = await POST(createChatRequest());
    const payload = await response.json();

    assert.equal(response.status, 402);
    assert.equal(payload.code, 'INSUFFICIENT_CREDITS');
    assert.equal(state.authInfoCalls, 1);
    assert.equal(state.useCreditCalls, 0);
    assert.equal(state.aiUiCalls, 0);
});

test('chat route rejects streamed requests when upfront credit deduction fails', async (t) => {
    const streamBody = createUIChunkStream([
        { type: 'text-delta', id: 't1', delta: '你好' },
    ]);
    const state = setupRouteMocks(t, streamBody);
    const creditsModule = require('../lib/user/credits') as any;
    creditsModule.attemptCreditUse = async () => {
        state.useCreditCalls += 1;
        return {
            ok: false,
            reason: 'deduction_failed',
        };
    };

    const { POST } = await import('../app/api/chat/route');

    const response = await POST(createChatRequest());
    const payload = await response.json();

    assert.equal(response.status, 500);
    assert.equal(payload.code, 'CREDIT_DEDUCTION_FAILED');
    assert.equal(state.useCreditCalls, 1);
    assert.equal(state.aiUiCalls, 0);
});

test('chat route keeps upfront charge when stream produces visible content', async (t) => {
    const streamBody = createUIChunkStream([
        { type: 'reasoning-delta', id: 'r1', delta: 'thinking' },
        { type: 'text-delta', id: 't1', delta: '你' },
        { type: 'text-delta', id: 't1', delta: '好' },
    ]);
    const state = setupRouteMocks(t, streamBody);
    const { POST } = await import('../app/api/chat/route');

    const response = await POST(createChatRequest());
    await response.text();
    await waitForMicrotask();

    assert.equal(state.useCreditCalls, 1);
    assert.equal(state.addCreditCalls, 0);
});

test('chat route keeps charge and does not refund when stream fails after visible content', async (t) => {
    const failingStream = createUIChunkStream([
        { type: 'text-delta', id: 't1', delta: 'partial' },
        { type: 'error', errorText: 'stream read failed' },
    ]);

    const state = setupRouteMocks(t, failingStream);
    const { POST } = await import('../app/api/chat/route');

    const response = await POST(createChatRequest());
    await response.text().catch(() => undefined);
    await waitForMicrotask();

    assert.equal(state.useCreditCalls, 1);
    assert.equal(state.addCreditCalls, 0);
});

test('chat route no longer uses the legacy BYOK server proxy path', async (t) => {
    const state = setupRouteMocks(t, createUIChunkStream([
        { type: 'text-delta', id: 't1', delta: 'ok' },
    ]));
    const { POST } = await import('../app/api/chat/route');

    const response = await POST(createByokChatRequest());
    await response.text();
    await waitForMicrotask();

    assert.equal(response.status, 200);
    assert.equal(state.authInfoCalls, 1);
    assert.equal(state.useCreditCalls, 1);
    assert.equal(state.addCreditCalls, 0);
    assert.equal(state.aiUiCalls, 1);
});

test('chat route returns 400 for invalid JSON bodies', async (t) => {
    setupRouteMocks(t, createUIChunkStream([]));
    const { POST } = await import('../app/api/chat/route');

    const response = await POST(createInvalidJsonRequest('http://localhost/api/chat'));
    const payload = await response.json();

    assert.equal(response.status, 400);
    assert.equal(payload.error, '请求体不是合法 JSON');
});

test('chat direct prepare builds prompt context without deducting credits', async (t) => {
    const state = setupRouteMocks(t, createUIChunkStream([]));
    const { POST } = await import('../app/api/chat/direct/prepare/route');

    const response = await POST(createDirectPrepareRequest());
    const payload = await response.json() as {
        systemPrompt?: string;
        sanitizedMessages?: Array<{ content: string }>;
        metadata?: Record<string, unknown>;
        requestedModelId?: string;
    };

    assert.equal(response.status, 200);
    assert.equal(state.authInfoCalls, 1);
    assert.equal(state.useCreditCalls, 0);
    assert.equal(state.addCreditCalls, 0);
    assert.equal(state.rateLimitCalls, 1);
    assert.equal(state.rateLimitEndpoint, '/api/chat/direct/prepare');
    assert.equal(payload.requestedModelId, 'gpt-4.1-mini');
    assert.equal(Array.isArray(payload.sanitizedMessages), true);
    assert.equal(payload.sanitizedMessages?.[0]?.content, '你好');
    assert.equal(typeof payload.metadata, 'object');
});

test('chat direct prepare returns 429 when BYOK rate limit is exhausted', async (t) => {
    const state = setupRouteMocks(t, createUIChunkStream([]));
    const rateLimitModule = require('../lib/rate-limit') as any;
    rateLimitModule.checkRateLimit = async (_identifier: string, endpoint: string) => {
        state.rateLimitCalls += 1;
        state.rateLimitEndpoint = endpoint;
        return {
            allowed: false,
            remaining: 0,
            resetAt: new Date(Date.now() + 60_000),
        };
    };

    const { POST } = await import('../app/api/chat/direct/prepare/route');
    const response = await POST(createDirectPrepareRequest());
    const payload = await response.json();

    assert.equal(response.status, 429);
    assert.equal(payload.error, '请求过于频繁，请稍后再试');
    assert.equal(state.rateLimitCalls, 1);
    assert.equal(state.rateLimitEndpoint, '/api/chat/direct/prepare');
    assert.equal(state.authInfoCalls, 0);
    assert.equal(state.useCreditCalls, 0);
});

test('chat direct prepare returns 400 for invalid JSON bodies', async (t) => {
    const state = setupRouteMocks(t, createUIChunkStream([]));
    const { POST } = await import('../app/api/chat/direct/prepare/route');

    const response = await POST(createInvalidJsonRequest('http://localhost/api/chat/direct/prepare'));
    const payload = await response.json();

    assert.equal(response.status, 400);
    assert.equal(payload.error, '请求体不是合法 JSON');
    assert.equal(state.rateLimitCalls, 0);
    assert.equal(state.authInfoCalls, 0);
    assert.equal(state.useCreditCalls, 0);
});
