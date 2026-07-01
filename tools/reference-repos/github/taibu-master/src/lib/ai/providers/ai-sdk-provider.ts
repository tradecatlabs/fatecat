/**
 * AI SDK Provider 适配层
 *
 * 基于 Vercel AI SDK（ai v6 + @ai-sdk/openai v3）
 * 替换原有的 openai-compatible.ts / vision-provider.ts
 */

import { createOpenAI } from '@ai-sdk/openai';
// @ts-expect-error TS Cannot find module 'ai' due to Next.js 15 bundler resolution in CLI tsc
import { generateText, streamText, type CoreMessage, type LanguageModel, type ProviderOptions, type JSONValue } from 'ai';
import type { AIModelConfig } from '@/types';
import type { ChatMessage, AIReasoningEffort } from '@/types';
import { normalizeCustomProviderBaseUrl } from '@/lib/ai/custom-provider-url';

// AI 请求只需要最小消息结构，避免强制依赖存储/展示字段。
export type AIRequestMessage = Pick<ChatMessage, 'role' | 'content' | 'model' | 'reasoning'>;

export interface AIProviderOptions {
    temperature?: number;
    maxTokens?: number;
    reasoning?: boolean;
    reasoningEffort?: AIReasoningEffort;
    imageBase64?: string;
    imageMimeType?: string;
}

export function getApiKey(envVar: string): string | undefined {
    return process.env[envVar];
}

/**
 * 根据 AIModelConfig 动态创建 AI SDK provider 实例和模型
 *
 * 当 reasoning 为 true 且 config.reasoningModelId 存在时，
 * 使用 reasoningModelId 替代 modelId，确保推理请求命中正确的后端模型。
 */
export function createModelFromConfig(
    config: AIModelConfig,
    options?: { reasoning?: boolean },
): LanguageModel {
    const apiKey = getApiKey(config.apiKeyEnvVar);
    if (!apiKey || apiKey === 'your_api_key_here') {
        throw new Error(`${config.name || config.id} API key not configured (${config.apiKeyEnvVar})`);
    }

    const baseURL = normalizeBaseUrl(config.apiUrl);
    const provider = createOpenAI({
        apiKey,
        baseURL,
        // 自定义 fetch：部分网关上游的 Cloudflare WAF 会拦截 Node.js 默认指纹，
        // 使用浏览器风格请求头绕过 bot 检测
        fetch: gatewayFetch,
    });

    // 推理模式下使用 reasoningModelId（如 deepseek-pro 的独立推理模型）
    const modelId = (options?.reasoning && config.reasoningModelId)
        ? config.reasoningModelId
        : config.modelId;

    // For OpenAI-compatible gateways (NewAPI/Octopus), use chat-completions mode.
    return provider.chat(modelId);
}

/**
 * 检查模型配置是否可用（API Key是否配置）
 */
export function isModelAvailable(config: AIModelConfig): boolean {
    const key = getApiKey(config.apiKeyEnvVar);
    return !!key && key !== 'your_api_key_here';
}

/**
 * 将 AIRequestMessage 转换为 AI SDK CoreMessage 格式
 */
export function toCoreMessages(
    messages: AIRequestMessage[],
    options?: { imageBase64?: string; imageMimeType?: string },
): CoreMessage[] {
    // system role 通过 streamText/generateText 的 system 参数传递，不放入 messages 数组
    return messages.filter(msg => msg.role !== 'system').map((msg, index, filtered) => {
        // Vision: 在最后一条用户消息中添加图片
        if (
            msg.role === 'user' &&
            options?.imageBase64 &&
            index === filtered.length - 1
        ) {
            return {
                role: 'user' as const,
                content: [
                    {
                        type: 'image' as const,
                        image: `data:${options.imageMimeType || 'image/jpeg'};base64,${options.imageBase64}`,
                    },
                    {
                        type: 'text' as const,
                        text: msg.content,
                    },
                ],
            };
        }

        return {
            role: msg.role as 'user' | 'assistant',
            content: msg.content,
        };
    });
}

/**
 * 需要 enable_thinking 参数激活推理模式的供应商集合
 */
const ENABLE_THINKING_VENDORS = new Set(['glm', 'deepseek', 'moonshot', 'qwen', 'qwen-vl']);

/**
 * 构建 vendor-specific 的推理模式参数
 *
 * reasoningEffortFormat 优先（标准 API 字段），
 * 否则走 vendor 特定的 enable_thinking 开关。
 */
function buildThinkingParams(
    vendor: string,
    reasoning?: boolean,
): Record<string, JSONValue> {
    if (!reasoning) return {};
    if (ENABLE_THINKING_VENDORS.has(vendor)) {
        return { enable_thinking: true };
    }
    return {};
}

/**
 * 构建 AI SDK 调用的 provider-specific 选项
 */
function buildProviderOptions(
    config: AIModelConfig,
    options?: AIProviderOptions,
): ProviderOptions | undefined {
    const providerOptions: Record<string, JSONValue> = {};

    // 推理模式：reasoningEffortFormat 优先（标准 API 字段），否则走 vendor 特定开关
    if (options?.reasoning) {
        const effort = options.reasoningEffort ?? config.defaultReasoningEffort;
        if (config.reasoningEffortFormat === 'reasoning_effort' && effort) {
            providerOptions.reasoningEffort = effort;
        } else if (config.reasoningEffortFormat === 'reasoning_object' && effort) {
            providerOptions.reasoning = { effort };
        } else {
            // GLM/DeepSeek/Moonshot/Qwen 等使用 vendor 特定参数激活推理
            Object.assign(providerOptions, buildThinkingParams(config.vendor, true));
        }
    }

    // 自定义参数透传
    if (config.customParameters && typeof config.customParameters === 'object') {
        Object.assign(providerOptions, config.customParameters);
    }

    if (Object.keys(providerOptions).length === 0) return undefined;

    return { openai: providerOptions };
}

/**
 * 非流式调用
 */
export async function callWithAISDK(
    model: LanguageModel,
    messages: CoreMessage[],
    systemPrompt: string,
    config: AIModelConfig,
    options?: AIProviderOptions,
): Promise<{ text: string; reasoning?: string }> {
    const result = await generateText({
        model,
        system: systemPrompt,
        messages,
        maxRetries: 0,
        temperature: options?.temperature ?? config.defaultTemperature ?? 0.7,
        maxOutputTokens: options?.maxTokens ?? config.defaultMaxTokens ?? undefined,
        topP: config.defaultTopP ?? undefined,
        presencePenalty: config.defaultPresencePenalty ?? undefined,
        frequencyPenalty: config.defaultFrequencyPenalty ?? undefined,
        providerOptions: buildProviderOptions(config, options),
    });

    return {
        text: result.text,
        reasoning: result.reasoningText ?? undefined,
    };
}

/**
 * 流式调用 — 返回 AI SDK StreamTextResult
 *
 * 调用方可以使用:
 * - result.toDataStream() 获取 DataStream（用于 chat route 的 toDataStreamResponse）
 * - result.textStream 获取纯文本流
 * - result.fullStream 获取完整事件流
 */
export function streamWithAISDK(
    model: LanguageModel,
    messages: CoreMessage[],
    systemPrompt: string,
    config: AIModelConfig,
    options?: AIProviderOptions,
) {
    const result = streamText({
        model,
        system: systemPrompt,
        messages,
        maxRetries: 0,
        temperature: options?.temperature ?? config.defaultTemperature ?? 0.7,
        maxOutputTokens: options?.maxTokens ?? config.defaultMaxTokens ?? undefined,
        topP: config.defaultTopP ?? undefined,
        presencePenalty: config.defaultPresencePenalty ?? undefined,
        frequencyPenalty: config.defaultFrequencyPenalty ?? undefined,
        providerOptions: buildProviderOptions(config, options),
    });

    return result;
}

// ─── Internal Helpers ───

/**
 * 自定义 fetch：绕过部分网关上游 Cloudflare WAF 的 bot 检测。
 *
 * Node.js 默认 fetch 的 TLS 指纹和请求头会被某些 CDN 拦截（返回 403），
 * 使用浏览器风格的 User-Agent 和 Accept 头即可通过。
 */
const BROWSER_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36';

function normalizeGatewayHeaders(init?: RequestInit): Headers {
    const headers = new Headers(init?.headers);
    headers.set('User-Agent', BROWSER_UA);
    if (!headers.has('Accept')) {
        let isStream = true;
        try {
            if (typeof init?.body === 'string') {
                isStream = JSON.parse(init.body).stream !== false;
            }
        } catch { /* default to stream */ }
        headers.set('Accept', isStream ? 'text/event-stream' : 'application/json');
    }
    return headers;
}

function mergeAbortSignals(signals: AbortSignal[]): AbortSignal {
    if (signals.length === 1) {
        return signals[0];
    }
    if (typeof AbortSignal.any === 'function') {
        return AbortSignal.any(signals);
    }

    const controller = new AbortController();
    const abort = (reason?: unknown) => {
        if (!controller.signal.aborted) {
            controller.abort(reason);
        }
    };
    for (const signal of signals) {
        if (signal.aborted) {
            abort(signal.reason);
            break;
        }
        signal.addEventListener('abort', () => abort(signal.reason), { once: true });
    }
    return controller.signal;
}

async function fetchWithGatewayHeaders(
    url: string | URL | Request,
    init?: RequestInit,
    timeoutMs?: number,
    connectTimeoutMs?: number,
): Promise<Response> {
    const headers = normalizeGatewayHeaders(init);
    const signalParts: AbortSignal[] = [];
    if (init?.signal) {
        signalParts.push(init.signal);
    }
    if (typeof timeoutMs === 'number' && typeof AbortSignal.timeout === 'function') {
        signalParts.push(AbortSignal.timeout(timeoutMs));
    }

    let connectTimer: ReturnType<typeof setTimeout> | null = null;
    let connectController: AbortController | null = null;
    if (typeof connectTimeoutMs === 'number') {
        connectController = new AbortController();
        connectTimer = setTimeout(() => {
            connectController?.abort(new Error('CONNECT_TIMEOUT'));
        }, connectTimeoutMs);
        connectTimer.unref?.();
        signalParts.push(connectController.signal);
    }

    try {
        return await globalThis.fetch(url, {
            ...init,
            headers,
            signal: signalParts.length > 0 ? mergeAbortSignals(signalParts) : undefined,
        });
    } catch (error) {
        if (connectController?.signal.aborted && connectController.signal.reason instanceof Error) {
            throw connectController.signal.reason;
        }
        throw error;
    } finally {
        if (connectTimer) {
            clearTimeout(connectTimer);
        }
    }
}

function gatewayFetch(url: string | URL | Request, init?: RequestInit): Promise<Response> {
    return fetchWithGatewayHeaders(url, init);
}

/**
 * 标准化 baseURL：
 * - AI SDK createOpenAI 内部会拼 /chat/completions
 * - 如果用户配置的 URL 包含完整路径，截掉
 * - 如果 URL 不含 /v1，补上（NewAPI 等网关需要 /v1 前缀）
 */
function normalizeBaseUrl(apiUrl: string): string {
    return normalizeCustomProviderBaseUrl(apiUrl);
}
