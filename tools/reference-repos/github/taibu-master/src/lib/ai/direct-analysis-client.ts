import type { CustomProviderRequest } from '@/types';
import type { DirectStreamingRequest } from '@/lib/hooks/useStreamingResponse';

type StreamingLike = {
    startDirectStream: (request: DirectStreamingRequest) => Promise<{
        content: string;
        reasoning: string | null;
        error?: string;
    } | null>;
};

export interface DirectAnalysisFlowOptions {
    endpoint: string;
    headers: Record<string, string>;
    provider: CustomProviderRequest;
    prepareBody: Record<string, unknown>;
    persistBody: Record<string, unknown>;
    streaming: StreamingLike;
}

export interface DirectAnalysisFlowResult {
    content: string;
    reasoning: string | null;
    conversationId: string | null;
    error?: string;
}

async function parseApiError(response: Response, fallbackMessage: string): Promise<string> {
    try {
        const data = await response.json() as { error?: string };
        if (typeof data.error === 'string' && data.error.trim()) {
            return data.error;
        }
    } catch {
        // ignore
    }
    return fallbackMessage;
}

export async function runDirectAnalysisFlow(
    options: DirectAnalysisFlowOptions,
): Promise<DirectAnalysisFlowResult> {
    const { endpoint, headers, provider, prepareBody, persistBody, streaming } = options;

    const prepareResponse = await fetch(endpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify(prepareBody),
    });
    if (!prepareResponse.ok) {
        return {
            content: '',
            reasoning: null,
            conversationId: null,
            error: await parseApiError(prepareResponse, '生成直连上下文失败，请稍后重试'),
        };
    }

    const prepared = await prepareResponse.json() as {
        data?: {
            systemPrompt?: string;
            userPrompt?: string;
        };
    };
    const systemPrompt = prepared.data?.systemPrompt || '';
    const userPrompt = prepared.data?.userPrompt || '';

    const streamResult = await streaming.startDirectStream({
        provider,
        systemPrompt,
        messages: [{ role: 'user', content: userPrompt }],
    });

    if (!streamResult) {
        return {
            content: '',
            reasoning: null,
            conversationId: null,
            error: '直连请求失败，请稍后重试',
        };
    }

    if (streamResult.error) {
        return {
            content: streamResult.content,
            reasoning: streamResult.reasoning,
            conversationId: null,
            error: streamResult.error,
        };
    }

    const persistResponse = await fetch(endpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify({
            ...persistBody,
            content: streamResult.content,
            reasoningText: streamResult.reasoning,
            customModelId: provider.modelId,
        }),
    });

    if (!persistResponse.ok) {
        return {
            content: streamResult.content,
            reasoning: streamResult.reasoning,
            conversationId: null,
            error: await parseApiError(persistResponse, '保存结果失败，请稍后重试'),
        };
    }

    const persisted = await persistResponse.json() as {
        data?: {
            conversationId?: string | null;
        };
    };

    return {
        content: streamResult.content,
        reasoning: streamResult.reasoning,
        conversationId: persisted.data?.conversationId ?? null,
    };
}
