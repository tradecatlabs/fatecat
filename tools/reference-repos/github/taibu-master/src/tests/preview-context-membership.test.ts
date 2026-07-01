import { test } from 'node:test';
import assert from 'node:assert/strict';

process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';

test('buildPreviewPromptContext reuses shared prompt builder even with preview-only overrides', async (t) => {
    t.after(() => {
        delete require.cache[require.resolve('../lib/chat/preview-context')];
    });
    delete require.cache[require.resolve('../lib/chat/preview-context')];
    const { buildPreviewPromptContext } = await import('../lib/chat/preview-context');

    let capturedRequest: Record<string, unknown> | null = null;

    const result = await buildPreviewPromptContext({
        auth: {
            user: { id: 'user-1' },
            supabase: {},
        } as never,
        body: {
            messages: [
                {
                    id: 'a1',
                    role: 'assistant',
                    content: '上一条 AI 回复',
                    createdAt: new Date().toISOString(),
                },
            ],
            userMessage: '新的提问',
            expressionStyle: 'gentle',
            customInstructions: null,
            userProfile: { identity: '创业者' },
        },
        requestedModelId: 'deepseek-chat',
        reasoningEnabled: false,
        membershipType: 'pro',
        knowledgeBaseFeatureEnabled: true,
        accessTokenForKB: 'token-1',
        sharedPromptContextBuilder: (async (request) => {
            capturedRequest = request as unknown as Record<string, unknown>;
            return {
                sanitizedMessages: [],
                fallbackPersonality: 'general' as const,
                systemPrompt: '共享系统提示词',
                promptKnowledgeBases: [{ id: 'kb-1', name: '知识库' }],
                metadata: {
                    sources: [],
                    kbSearchEnabled: true,
                    kbHitCount: 0,
                    promptDiagnostics: {
                        modelId: 'deepseek-chat',
                        layers: [],
                        totalTokens: 12,
                        budgetTotal: 48,
                        userMessageTokens: 3,
                    },
                },
            };
        }) as never,
    });

    assert.ok(capturedRequest);
    assert.equal(capturedRequest?.membershipType, 'pro');
    assert.equal(capturedRequest?.accessTokenForKB, 'token-1');
    assert.equal((capturedRequest?.body as Record<string, unknown>).expressionStyle, 'gentle');
    assert.equal((capturedRequest?.body as Record<string, unknown>).customInstructions, null);
    assert.deepEqual((capturedRequest?.body as Record<string, unknown>).userProfile, { identity: '创业者' });
    const messages = (capturedRequest?.body as { messages: Array<{ id: string; role: string; content: string; createdAt: string }> }).messages;
    assert.equal(messages.length, 2);
    assert.equal(messages[0]?.id, 'a1');
    assert.equal(messages[0]?.role, 'assistant');
    assert.equal(messages[0]?.content, '上一条 AI 回复');
    assert.equal(messages[1]?.id, 'preview-user-2');
    assert.equal(messages[1]?.role, 'user');
    assert.equal(messages[1]?.content, '新的提问');
    assert.equal(typeof messages[1]?.createdAt, 'string');
    assert.equal(result.totalTokens, 12);
    assert.equal(result.promptKnowledgeBases[0]?.id, 'kb-1');
    assert.ok(result.contextTotal > 0);
});
