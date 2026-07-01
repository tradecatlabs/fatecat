/**
 * AI 分析查询工具函数（客户端）
 *
 * 浏览器侧统一通过 feature API 查询历史分析与摘要。
 */

import {
    getSourceDataModelId,
    getSourceDataReasoning,
} from '@/lib/source-contracts';
import type { ChatMessage } from '@/types';

export function extractAnalysisFromConversation(
    messages: ChatMessage[] = [],
    sourceData?: Record<string, unknown>
) {
    const assistant = messages.find(m => m.role === 'assistant');
    const modelId = typeof assistant?.model === 'string'
        ? assistant.model
        : getSourceDataModelId(sourceData);
    const reasoning = typeof assistant?.reasoning === 'string'
        ? assistant.reasoning
        : getSourceDataReasoning(sourceData);

    return {
        analysis: assistant?.content || null,
        reasoning,
        modelId,
    };
}

export function hydrateConversationMessages(
    messages: ChatMessage[] = [],
    sourceData?: Record<string, unknown>
) {
    if (!sourceData) return messages;
    const modelId = getSourceDataModelId(sourceData);
    const reasoningText = getSourceDataReasoning(sourceData);
    if (!modelId && !reasoningText) return messages;
    return messages.map(msg => {
        if (msg.role !== 'assistant') return msg;
        return {
            ...msg,
            model: msg.model || modelId || undefined,
            reasoning: msg.reasoning || reasoningText || undefined,
        };
    });
}

