/**
 * 共享 SSE 流式响应解析 Hook
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useState, useCallback)
 * - 需要在客户端处理流式响应
 */
'use client';

import { useState, useCallback, useRef } from 'react';
import type { CustomProviderRequest } from '@/types';
import {
    buildBrowserDirectMessages,
    streamBrowserDirectProvider,
    normalizeBrowserDirectError,
} from '@/lib/ai/browser-direct-provider';
import { useStreamingText, type StreamingTextOptions } from './useStreamingText';

interface StreamingState {
    content: string;
    reasoning: string | null;
    reasoningStartTime: number | undefined;
    reasoningDuration: number | undefined;
    isStreaming: boolean;
    error: string | null;
}

interface StreamingResponseOptions {
    /** 是否启用平滑渲染 */
    smoothRendering?: boolean;
    /** 平滑渲染配置 */
    smoothRenderingOptions?: StreamingTextOptions;
}

interface StreamingCallbacks {
    onContent?: (content: string) => void;
    onReasoning?: (reasoning: string) => void;
    onReasoningStart?: (startTime: number) => void;
    onComplete?: (content: string, reasoning: string | null) => void;
    onError?: (error: string) => void;
}

export interface DirectStreamingRequest {
    provider: CustomProviderRequest;
    systemPrompt: string;
    messages: Array<{
        role: 'system' | 'user' | 'assistant';
        content: string;
    }>;
}

interface ParsedSSEData {
    type?: string;
    delta?: string;
    error?: string;
    errorText?: string;
    conversationId?: string | null;
    metadata?: Record<string, unknown>;
    messageMetadata?: Record<string, unknown>;
}

interface ParsedStreamingSSEFrame {
    contentDelta?: string;
    reasoningDelta?: string;
    error?: string;
    conversationId?: string | null;
    done: boolean;
}

export function parseStreamingSSEData(data: string): ParsedStreamingSSEFrame {
    if (data === '[DONE]') {
        return { done: true };
    }

    try {
        const parsed: ParsedSSEData = JSON.parse(data);
        return {
            contentDelta: parsed.type === 'text-delta' ? parsed.delta : undefined,
            reasoningDelta: parsed.type === 'reasoning-delta' ? parsed.delta : undefined,
            error: typeof parsed.errorText === 'string'
                ? parsed.errorText
                : (typeof parsed.error === 'string' ? parsed.error : undefined),
            conversationId: typeof parsed.conversationId === 'string' ? parsed.conversationId : null,
            done: false,
        };
    } catch {
        return { done: false };
    }
}

/**
 * 解析 SSE 流式响应的 Hook
 */
export function useStreamingResponse(
    callbacks?: StreamingCallbacks,
    options?: StreamingResponseOptions
) {
    const { smoothRendering = false, smoothRenderingOptions } = options || {};

    // 平滑渲染 hook（用于内容）
    const contentStreaming = useStreamingText(smoothRenderingOptions);
    // 平滑渲染 hook（用于推理）
    const reasoningStreaming = useStreamingText(smoothRenderingOptions);

    const [state, setState] = useState<StreamingState>({
        content: '',
        reasoning: null,
        reasoningStartTime: undefined,
        reasoningDuration: undefined,
        isStreaming: false,
        error: null,
    });

    // 原始内容（未经平滑渲染）
    const rawContentRef = useRef('');
    const rawReasoningRef = useRef('');

    const abortControllerRef = useRef<AbortController | null>(null);

    const reset = useCallback(() => {
        setState({
            content: '',
            reasoning: null,
            reasoningStartTime: undefined,
            reasoningDuration: undefined,
            isStreaming: false,
            error: null,
        });
        rawContentRef.current = '';
        rawReasoningRef.current = '';
        if (smoothRendering) {
            contentStreaming.reset();
            reasoningStreaming.reset();
        }
    }, [smoothRendering, contentStreaming, reasoningStreaming]);

    const stop = useCallback(() => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
            abortControllerRef.current = null;
        }
        if (smoothRendering) {
            contentStreaming.stop();
            reasoningStreaming.stop();
        }
    }, [smoothRendering, contentStreaming, reasoningStreaming]);

    const processStream = useCallback(async (response: Response) => {
        const reader = response.body?.getReader();
        if (!reader) {
            const errorMsg = '无法读取响应流';
            setState(prev => ({ ...prev, error: errorMsg, isStreaming: false }));
            callbacks?.onError?.(errorMsg);
            return { content: '', reasoning: null };
        }

        const decoder = new TextDecoder();
        let accumulatedContent = '';
        let accumulatedReasoning = '';
        let streamError: string | undefined = undefined;
        let streamReasoningStartTime: number | undefined = undefined;
        let buffer = '';

        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() ?? '';

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        const frame = parseStreamingSSEData(data);
                        if (frame.done) continue;

                        if (frame.error) {
                            streamError = frame.error;
                            setState(prev => ({
                                ...prev,
                                error: frame.error || null,
                            }));
                            callbacks?.onError?.(frame.error);
                            continue;
                        }

                        // 处理推理内容
                        const reasoningContent = frame.reasoningDelta;
                        if (reasoningContent) {
                            if (!accumulatedReasoning && !streamReasoningStartTime) {
                                streamReasoningStartTime = Date.now();
                                setState(prev => ({
                                    ...prev,
                                    reasoningStartTime: streamReasoningStartTime,
                                }));
                                callbacks?.onReasoningStart?.(streamReasoningStartTime);
                            }
                            accumulatedReasoning += reasoningContent;
                            rawReasoningRef.current = accumulatedReasoning;
                            if (smoothRendering) {
                                reasoningStreaming.addCharacters(reasoningContent);
                            } else {
                                setState(prev => ({
                                    ...prev,
                                    reasoning: accumulatedReasoning,
                                }));
                            }
                            callbacks?.onReasoning?.(accumulatedReasoning);
                        }

                        // 处理正常内容
                        const content = frame.contentDelta;
                        if (content) {
                            accumulatedContent += content;
                            rawContentRef.current = accumulatedContent;
                            if (smoothRendering) {
                                contentStreaming.addCharacters(content);
                            } else {
                                setState(prev => ({
                                    ...prev,
                                    content: accumulatedContent,
                                }));
                            }
                            callbacks?.onContent?.(accumulatedContent);
                        }
                    }
                }
            }
        } finally {
            reader.releaseLock();
        }

        // 计算推理用时
        const reasoningDuration = streamReasoningStartTime
            ? Math.floor((Date.now() - streamReasoningStartTime) / 1000)
            : undefined;

        // 平滑渲染模式下，立即完成渲染
        if (smoothRendering) {
            contentStreaming.flush();
            reasoningStreaming.flush();
        }

        setState(prev => ({
            ...prev,
            isStreaming: false,
            error: streamError || prev.error,
            reasoningDuration,
            content: accumulatedContent,
            reasoning: accumulatedReasoning || null,
        }));

        callbacks?.onComplete?.(
            accumulatedContent,
            accumulatedReasoning || null
        );

        return {
            content: accumulatedContent,
            reasoning: accumulatedReasoning || null,
            error: streamError,
        };
    }, [callbacks, smoothRendering, contentStreaming, reasoningStreaming]);

    const startDirectStream = useCallback(async (
        request: DirectStreamingRequest,
    ): Promise<{ content: string; reasoning: string | null; error?: string } | null> => {
        setState({
            content: '',
            reasoning: null,
            reasoningStartTime: undefined,
            reasoningDuration: undefined,
            isStreaming: true,
            error: null,
        });
        rawContentRef.current = '';
        rawReasoningRef.current = '';
        if (smoothRendering) {
            contentStreaming.reset();
            reasoningStreaming.reset();
        }

        abortControllerRef.current = new AbortController();

        let accumulatedContent = '';
        let accumulatedReasoning = '';
        let streamReasoningStartTime: number | undefined;

        try {
            const result = await streamBrowserDirectProvider({
                provider: request.provider,
                messages: buildBrowserDirectMessages(request.systemPrompt, request.messages),
                signal: abortControllerRef.current.signal,
                onContentDelta: (delta) => {
                    accumulatedContent += delta;
                    rawContentRef.current = accumulatedContent;
                    if (smoothRendering) {
                        contentStreaming.addCharacters(delta);
                    } else {
                        setState((prev) => ({
                            ...prev,
                            content: accumulatedContent,
                        }));
                    }
                    callbacks?.onContent?.(accumulatedContent);
                },
                onReasoningDelta: (delta) => {
                    if (!accumulatedReasoning && !streamReasoningStartTime) {
                        streamReasoningStartTime = Date.now();
                        setState((prev) => ({
                            ...prev,
                            reasoningStartTime: streamReasoningStartTime,
                        }));
                        callbacks?.onReasoningStart?.(streamReasoningStartTime);
                    }
                    accumulatedReasoning += delta;
                    rawReasoningRef.current = accumulatedReasoning;
                    if (smoothRendering) {
                        reasoningStreaming.addCharacters(delta);
                    } else {
                        setState((prev) => ({
                            ...prev,
                            reasoning: accumulatedReasoning,
                        }));
                    }
                    callbacks?.onReasoning?.(accumulatedReasoning);
                },
            });

            if (smoothRendering) {
                contentStreaming.flush();
                reasoningStreaming.flush();
            }

            const reasoningDuration = streamReasoningStartTime
                ? Math.floor((Date.now() - streamReasoningStartTime) / 1000)
                : undefined;

            setState((prev) => ({
                ...prev,
                isStreaming: false,
                error: null,
                reasoningDuration,
                content: result.content,
                reasoning: result.reasoning,
            }));

            callbacks?.onComplete?.(result.content, result.reasoning);
            return result;
        } catch (error) {
            const normalized = normalizeBrowserDirectError(error);
            if (normalized.code === 'ABORTED') {
                setState((prev) => ({ ...prev, isStreaming: false }));
                return { content: accumulatedContent, reasoning: accumulatedReasoning || null };
            }
            setState((prev) => ({
                ...prev,
                error: normalized.message,
                isStreaming: false,
            }));
            callbacks?.onError?.(normalized.message);
            return {
                content: accumulatedContent,
                reasoning: accumulatedReasoning || null,
                error: normalized.message,
            };
        } finally {
            abortControllerRef.current = null;
        }
    }, [callbacks, smoothRendering, contentStreaming, reasoningStreaming]);

    const startStream = useCallback(async (
        url: string,
        options: RequestInit
    ): Promise<{ content: string; reasoning: string | null; error?: string } | null> => {
        // 重置状态
        setState({
            content: '',
            reasoning: null,
            reasoningStartTime: undefined,
            reasoningDuration: undefined,
            isStreaming: true,
            error: null,
        });
        rawContentRef.current = '';
        rawReasoningRef.current = '';
        if (smoothRendering) {
            contentStreaming.reset();
            reasoningStreaming.reset();
        }

        // 创建 AbortController
        abortControllerRef.current = new AbortController();

        try {
            const response = await fetch(url, {
                ...options,
                signal: abortControllerRef.current.signal,
            });

            if (!response.ok) {
                const data = await response.json();
                const errorMsg = data.error || '请求失败';
                setState(prev => ({
                    ...prev,
                    error: errorMsg,
                    isStreaming: false,
                }));
                callbacks?.onError?.(errorMsg);
                return { content: '', reasoning: null, error: errorMsg };
            }

            return await processStream(response);
        } catch (err) {
            if (err instanceof Error && err.name === 'AbortError') {
                setState(prev => ({ ...prev, isStreaming: false }));
                return { content: '', reasoning: null };
            }
            const errorMsg = err instanceof Error ? err.message : '请求失败';
            setState(prev => ({
                ...prev,
                error: errorMsg,
                isStreaming: false,
            }));
            callbacks?.onError?.(errorMsg);
            return { content: '', reasoning: null, error: errorMsg };
        } finally {
            abortControllerRef.current = null;
        }
    }, [processStream, callbacks, smoothRendering, contentStreaming, reasoningStreaming]);

    // 平滑渲染模式下，返回平滑渲染的内容
    const displayContent = smoothRendering ? contentStreaming.visibleContent : state.content;
    const displayReasoning = smoothRendering ? reasoningStreaming.visibleContent : state.reasoning;

    return {
        ...state,
        content: displayContent,
        reasoning: displayReasoning || null,
        // 额外暴露原始内容（用于保存等场景）
        rawContent: rawContentRef.current,
        rawReasoning: rawReasoningRef.current,
        // 平滑渲染状态
        isContentRendering: smoothRendering ? contentStreaming.isRendering : false,
        isReasoningRendering: smoothRendering ? reasoningStreaming.isRendering : false,
        startStream,
        startDirectStream,
        processStream,
        reset,
        stop,
    };
}

/**
 * 检查错误是否为积分不足
 */
export function isCreditsError(error: string | null): boolean {
    if (!error) return false;
    return error.includes('积分不足') || error.includes('充值') || error.includes('获取积分');
}
