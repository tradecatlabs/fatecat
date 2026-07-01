/**
 * AI 模型管理 API
 *
 * GET: 获取所有模型配置（含网关绑定）
 * POST: 创建新模型
 */
import { NextRequest } from 'next/server';
import { requireAdminUser, jsonError, jsonOk, getSystemAdminClient } from '@/lib/api-utils';
import { clearModelCache } from '@/lib/server/ai-config';
import type {
    AIReasoningEffort,
    AIReasoningEffortFormat,
    AIRoutingMode,
    AITransport,
    AIUsageType,
} from '@/types';
import {
    buildManagedApiUrl,
    DEFAULT_AI_TRANSPORT,
    getModelUsageType,
    isManagedSourceKey,
    sortModelSources,
    type ManagedAISourceKey,
} from '@/lib/ai/source-runtime';

function hasEnvVar(envVarName: string): boolean {
    return !!envVarName && !!process.env[envVarName];
}

const VALID_USAGE_TYPES: AIUsageType[] = ['chat', 'vision', 'embedding', 'rerank'];
const VALID_ROUTING_MODES: AIRoutingMode[] = ['auto', 'newapi', 'octopus'];
const VALID_REASONING_EFFORTS: AIReasoningEffort[] = ['minimal', 'low', 'medium', 'high'];
const VALID_REASONING_EFFORT_FORMATS: AIReasoningEffortFormat[] = ['reasoning_object', 'reasoning_effort'];

const MODEL_SELECT = `
    id,
    model_key,
    display_name,
    vendor,
    usage_type,
    routing_mode,
    is_enabled,
    sort_order,
    required_tier,
    supports_reasoning,
    reasoning_required_tier,
    is_reasoning_default,
    supports_vision,
    default_temperature,
    default_top_p,
    default_presence_penalty,
    default_frequency_penalty,
    default_max_tokens,
    default_reasoning_effort,
    reasoning_effort_format,
    custom_parameters,
    description,
    created_at,
    updated_at,
    bindings:ai_model_gateway_bindings (
        id,
        model_id_override,
        reasoning_model_id,
        is_enabled,
        priority,
        notes,
        gateway:ai_gateways (
            id,
            gateway_key,
            display_name,
            base_url,
            api_key_env_var,
            transport,
            is_enabled,
            notes
        )
    )
`;

type AdminGatewayRow = {
    id: string;
    gateway_key: string | null;
    display_name: string | null;
    base_url: string | null;
    api_key_env_var: string | null;
    transport?: string | null;
    is_enabled?: boolean | null;
    notes?: string | null;
};

type AdminBindingRow = {
    id: string;
    model_id_override: string | null;
    reasoning_model_id: string | null;
    is_enabled: boolean;
    priority?: number | null;
    notes?: string | null;
    gateway?: AdminGatewayRow | AdminGatewayRow[] | null;
};

type AdminModelRow = {
    id: string;
    model_key: string;
    display_name: string;
    vendor: string;
    usage_type?: AIUsageType;
    routing_mode?: AIRoutingMode;
    is_enabled: boolean;
    sort_order: number;
    required_tier: 'free' | 'plus' | 'pro';
    supports_reasoning: boolean;
    reasoning_required_tier: 'free' | 'plus' | 'pro';
    is_reasoning_default: boolean;
    supports_vision: boolean;
    default_temperature: number | string | null;
    default_top_p?: number | string | null;
    default_presence_penalty?: number | string | null;
    default_frequency_penalty?: number | string | null;
    default_max_tokens: number | null;
    default_reasoning_effort?: AIReasoningEffort | null;
    reasoning_effort_format?: AIReasoningEffortFormat | null;
    custom_parameters?: Record<string, unknown> | null;
    description: string | null;
    created_at: string;
    updated_at: string;
    bindings?: AdminBindingRow[];
};

function normalizeCustomParameters(input: unknown): Record<string, unknown> | null {
    if (input == null) {
        return null;
    }
    if (typeof input !== 'object' || Array.isArray(input)) {
        throw new Error('customParameters 必须为 JSON 对象');
    }
    return input as Record<string, unknown>;
}

type AdminModelSource = {
    id: string;
    sourceKey: string;
    sourceName: string;
    apiUrl: string;
    apiKeyEnvVar: string;
    hasApiKey: boolean;
    modelIdOverride: string | null;
    reasoningModelId: string | null;
    isActive: boolean;
    isEnabled: boolean;
    priority: number;
    transport: AITransport;
    maxContextTokens: null;
    maxOutputTokens: null;
    notes: string | null;
};

type PendingAdminModelSource = Omit<AdminModelSource, 'isActive'>;

type AdminModelMutationResult = {
    status?: string | null;
    model?: Record<string, unknown> | null;
};

function pickGateway(input: AdminBindingRow['gateway']): AdminGatewayRow | null {
    if (Array.isArray(input)) {
        return input[0] ?? null;
    }
    return input ?? null;
}

function resolvePrimaryGatewayKey(
    primaryGatewayKey: unknown,
    routingMode: AIRoutingMode,
): ManagedAISourceKey | null {
    if (typeof primaryGatewayKey === 'string' && primaryGatewayKey.length > 0) {
        return isManagedSourceKey(primaryGatewayKey) ? primaryGatewayKey : null;
    }

    if (routingMode === 'newapi' || routingMode === 'octopus') {
        return routingMode;
    }

    return 'newapi';
}

function parseAdminModelMutationResult(value: unknown): AdminModelMutationResult | null {
    if (!value || typeof value !== 'object' || Array.isArray(value)) {
        return null;
    }
    return value as AdminModelMutationResult;
}

function mapModelSources(model: AdminModelRow) {
    const usageType = getModelUsageType({
        usageType: model.usage_type,
        supportsVision: model.supports_vision,
    });

    const mappedSources = (model.bindings || [])
        .map((binding): PendingAdminModelSource | null => {
            const gateway = pickGateway(binding.gateway);
            if (!gateway || !isManagedSourceKey(gateway.gateway_key)) {
                return null;
            }

            return {
                id: binding.id,
                sourceKey: gateway.gateway_key,
                sourceName: gateway.display_name || gateway.gateway_key,
                apiUrl: buildManagedApiUrl(gateway.base_url, usageType),
                apiKeyEnvVar: gateway.api_key_env_var || '',
                hasApiKey: hasEnvVar(gateway.api_key_env_var || ''),
                modelIdOverride: binding.model_id_override,
                reasoningModelId: binding.reasoning_model_id,
                isEnabled: binding.is_enabled !== false && gateway.is_enabled !== false,
                priority: binding.priority ?? 0,
                transport: (gateway.transport as AITransport) || DEFAULT_AI_TRANSPORT,
                maxContextTokens: null,
                maxOutputTokens: null,
                notes: binding.notes ?? gateway.notes ?? null,
            };
        })
        .filter((source): source is PendingAdminModelSource => source !== null);

    const sortedSources = sortModelSources(mappedSources);
    let activeAssigned = false;

    return sortedSources.map((source) => {
        const isActive = !activeAssigned && source.isEnabled;
        if (isActive) {
            activeAssigned = true;
        }
        return {
            ...source,
            isActive,
        };
    });
}

export async function GET(request: NextRequest) {
    const authResult = await requireAdminUser(request);
    if ('error' in authResult) {
        return jsonError(authResult.error.message, authResult.error.status);
    }

    const supabase = getSystemAdminClient();
    const url = new URL(request.url);
    const includeDisabled = url.searchParams.get('includeDisabled') === 'true';

    let query = supabase
        .from('ai_models')
        .select(MODEL_SELECT)
        .order('sort_order', { ascending: true });

    if (!includeDisabled) {
        query = query.eq('is_enabled', true);
    }

    const { data: models, error } = await query;

    if (error) {
        console.error('[ai-models] Failed to fetch models:', error);
        return jsonError('获取模型列表失败', 500);
    }

    const formattedModels = (models as AdminModelRow[] | null)?.map((model) => ({
        id: model.id,
        modelKey: model.model_key,
        displayName: model.display_name,
        vendor: model.vendor,
        usageType: model.usage_type || (model.supports_vision ? 'vision' : 'chat'),
        routingMode: model.routing_mode || 'auto',
        isEnabled: model.is_enabled,
        sortOrder: model.sort_order,
        requiredTier: model.required_tier,
        supportsReasoning: model.supports_reasoning,
        reasoningRequiredTier: model.reasoning_required_tier,
        isReasoningDefault: model.is_reasoning_default,
        supportsVision: model.supports_vision,
        defaultTemperature:
            model.default_temperature != null
                ? Number.parseFloat(String(model.default_temperature))
                : 0.7,
        defaultTopP:
            model.default_top_p != null
                ? Number.parseFloat(String(model.default_top_p))
                : null,
        defaultPresencePenalty:
            model.default_presence_penalty != null
                ? Number.parseFloat(String(model.default_presence_penalty))
                : null,
        defaultFrequencyPenalty:
            model.default_frequency_penalty != null
                ? Number.parseFloat(String(model.default_frequency_penalty))
                : null,
        defaultMaxTokens: model.default_max_tokens,
        defaultReasoningEffort: model.default_reasoning_effort || null,
        reasoningEffortFormat: model.reasoning_effort_format || null,
        customParameters: model.custom_parameters || null,
        description: model.description,
        createdAt: model.created_at,
        updatedAt: model.updated_at,
        sources: mapModelSources(model),
    })) || [];

    return jsonOk({ models: formattedModels });
}

export async function POST(request: NextRequest) {
    const authResult = await requireAdminUser(request);
    if ('error' in authResult) {
        return jsonError(authResult.error.message, authResult.error.status);
    }

    const supabase = getSystemAdminClient();

    try {
        const body = await request.json();
        const {
            modelKey,
            displayName,
            vendor,
            primaryGatewayKey,
            isEnabled = true,
            sortOrder = 0,
            requiredTier = 'free',
            supportsReasoning = false,
            reasoningRequiredTier = 'plus',
            isReasoningDefault = false,
            supportsVision = false,
            usageType = 'chat',
            routingMode = 'auto',
            defaultTemperature = 0.7,
            defaultTopP = null,
            defaultPresencePenalty = null,
            defaultFrequencyPenalty = null,
            defaultMaxTokens = null,
            defaultReasoningEffort = null,
            reasoningEffortFormat = null,
            customParameters = null,
            description,
        } = body;

        if (!modelKey || !displayName || !vendor) {
            return jsonError('缺少必填字段: modelKey, displayName, vendor', 400);
        }

        const validTiers = ['free', 'plus', 'pro'];
        if (!validTiers.includes(requiredTier)) {
            return jsonError('无效的 requiredTier 值', 400);
        }
        if (!validTiers.includes(reasoningRequiredTier)) {
            return jsonError('无效的 reasoningRequiredTier 值', 400);
        }
        if (!VALID_USAGE_TYPES.includes(usageType)) {
            return jsonError('无效的 usageType 值', 400);
        }
        if (!VALID_ROUTING_MODES.includes(routingMode)) {
            return jsonError('无效的 routingMode 值', 400);
        }
        const selectedGatewayKey = resolvePrimaryGatewayKey(primaryGatewayKey, routingMode);
        if (!selectedGatewayKey) {
            return jsonError('无效的 primaryGatewayKey 值', 400);
        }
        if (defaultReasoningEffort && !VALID_REASONING_EFFORTS.includes(defaultReasoningEffort)) {
            return jsonError('无效的 defaultReasoningEffort 值', 400);
        }
        if (reasoningEffortFormat && !VALID_REASONING_EFFORT_FORMATS.includes(reasoningEffortFormat)) {
            return jsonError('无效的 reasoningEffortFormat 值', 400);
        }

        let normalizedCustomParameters: Record<string, unknown> | null;
        try {
            normalizedCustomParameters = normalizeCustomParameters(customParameters);
        } catch (error) {
            return jsonError(error instanceof Error ? error.message : '自定义参数格式错误', 400);
        }

        const insertData = {
            model_key: modelKey,
            display_name: displayName,
            vendor,
            usage_type: usageType,
            routing_mode: routingMode,
            is_enabled: isEnabled,
            sort_order: sortOrder,
            required_tier: requiredTier,
            supports_reasoning: supportsReasoning,
            reasoning_required_tier: reasoningRequiredTier,
            is_reasoning_default: isReasoningDefault,
            supports_vision: supportsVision || usageType === 'vision',
            default_temperature: defaultTemperature,
            default_top_p: defaultTopP,
            default_presence_penalty: defaultPresencePenalty,
            default_frequency_penalty: defaultFrequencyPenalty,
            default_max_tokens: defaultMaxTokens,
            default_reasoning_effort: supportsReasoning ? defaultReasoningEffort : null,
            reasoning_effort_format: supportsReasoning ? reasoningEffortFormat : null,
            custom_parameters: normalizedCustomParameters,
            description,
        };

        const { data, error } = await supabase.rpc('admin_create_ai_model_with_binding', {
            p_model: insertData,
            p_primary_gateway_key: selectedGatewayKey,
        });

        if (error) {
            console.error('[ai-models] Failed to create model transaction:', error);
            return jsonError('创建模型失败', 500);
        }

        const result = parseAdminModelMutationResult(data);
        if (!result?.status) {
            console.error('[ai-models] Invalid create model RPC result:', data);
            return jsonError('创建模型失败', 500);
        }

        if (result.status === 'conflict') {
            return jsonError('模型 ID 已存在', 409);
        }

        if (result.status === 'gateway_not_found') {
            return jsonError('来源网关不存在，请先在网关管理中配置', 404);
        }

        if (result.status !== 'ok' || !result.model) {
            console.error('[ai-models] Unexpected create model RPC status:', result.status);
            return jsonError('创建模型失败', 500);
        }

        clearModelCache();

        return jsonOk({ success: true, model: result.model }, 201);
    } catch (e) {
        console.error('[ai-models] Invalid request body:', e);
        return jsonError('请求格式错误', 400);
    }
}
