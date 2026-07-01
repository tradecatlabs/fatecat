/**
 * AI 模型网关绑定管理 API
 *
 * GET: 获取模型的所有网关绑定
 * POST: 添加新绑定
 */
import { NextRequest } from 'next/server';
import { requireAdminUser, jsonError, jsonOk, getSystemAdminClient } from '@/lib/api-utils';
import { clearModelCache } from '@/lib/server/ai-config';
import type { AITransport } from '@/types';
import {
    buildManagedApiUrl,
    DEFAULT_AI_TRANSPORT,
    getModelUsageType,
    isManagedSourceKey,
    sortModelSources,
} from '@/lib/ai/source-runtime';

function hasEnvVar(envVarName: string): boolean {
    return !!envVarName && !!process.env[envVarName];
}

type RouteContext = {
    params: Promise<{ id: string }>;
};

type GatewayRow = {
    id: string;
    gateway_key: string | null;
    display_name: string | null;
    base_url: string | null;
    api_key_env_var: string | null;
    transport?: string | null;
    is_enabled?: boolean | null;
    notes?: string | null;
};

type BindingRow = {
    id: string;
    model_id_override: string | null;
    reasoning_model_id: string | null;
    is_enabled: boolean;
    priority?: number | null;
    notes?: string | null;
    gateway?: GatewayRow | GatewayRow[] | null;
};

type BindingSourceResponse = {
    id: string;
    sourceKey: string;
    sourceName: string;
    apiUrl: string;
    apiKeyEnvVar: string;
    hasApiKey: boolean;
    transport: AITransport;
    modelIdOverride: string | null;
    reasoningModelId: string | null;
    isActive: boolean;
    isEnabled: boolean;
    priority: number;
    notes: string | null;
    maxContextTokens: null;
    maxOutputTokens: null;
};

type PendingBindingSourceResponse = Omit<BindingSourceResponse, 'isActive'>;

function pickGateway(input: BindingRow['gateway']): GatewayRow | null {
    if (Array.isArray(input)) {
        return input[0] ?? null;
    }
    return input ?? null;
}

function normalizeOptionalTextField(
    value: unknown,
    fieldName: string,
): { value: string | null | undefined; error: string | null } {
    if (value === undefined) {
        return { value: undefined, error: null };
    }
    if (value === null) {
        return { value: null, error: null };
    }
    if (typeof value !== 'string') {
        return { value: undefined, error: `${fieldName} 必须是字符串或 null` };
    }

    return { value, error: null };
}

async function getModelUsageMeta(supabase: ReturnType<typeof getSystemAdminClient>, modelId: string) {
    const { data: model, error } = await supabase
        .from('ai_models')
        .select('model_key, usage_type, supports_vision')
        .eq('id', modelId)
        .single();

    if (error || !model) {
        return null;
    }

    return {
        modelKey: model.model_key as string,
        usageType: getModelUsageType({
            usageType: model.usage_type,
            supportsVision: model.supports_vision,
        }),
    };
}

function mapBindingSources(bindings: BindingRow[], usageType: 'chat' | 'vision' | 'embedding' | 'rerank') {
    const mappedSources = bindings
        .map((binding): PendingBindingSourceResponse | null => {
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
                transport: (gateway.transport as AITransport) || DEFAULT_AI_TRANSPORT,
                modelIdOverride: binding.model_id_override,
                reasoningModelId: binding.reasoning_model_id,
                isEnabled: binding.is_enabled !== false && gateway.is_enabled !== false,
                priority: binding.priority ?? 0,
                maxContextTokens: null,
                maxOutputTokens: null,
                notes: binding.notes ?? gateway.notes ?? null,
            };
        })
        .filter((source): source is PendingBindingSourceResponse => source !== null);

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

export async function GET(request: NextRequest, context: RouteContext) {
    const authResult = await requireAdminUser(request);
    if ('error' in authResult) {
        return jsonError(authResult.error.message, authResult.error.status);
    }

    const { id: modelId } = await context.params;
    const supabase = getSystemAdminClient();
    const modelMeta = await getModelUsageMeta(supabase, modelId);
    if (!modelMeta) {
        return jsonError('模型不存在', 404);
    }

    const { data: bindings, error } = await supabase
        .from('ai_model_gateway_bindings')
        .select(`
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
        `)
        .eq('model_id', modelId)
        .order('priority', { ascending: true });

    if (error) {
        console.error('[ai-models] Failed to fetch bindings:', error);
        return jsonError('获取来源列表失败', 500);
    }

    return jsonOk({ sources: mapBindingSources((bindings as BindingRow[] | null) || [], modelMeta.usageType) });
}

export async function POST(request: NextRequest, context: RouteContext) {
    const authResult = await requireAdminUser(request);
    if ('error' in authResult) {
        return jsonError(authResult.error.message, authResult.error.status);
    }

    const { id: modelId } = await context.params;
    const supabase = getSystemAdminClient();

    try {
        const body = await request.json();
        const {
            sourceKey,
            modelIdOverride,
            reasoningModelId,
            isEnabled = true,
            priority,
            notes,
        } = body;

        if (!sourceKey) {
            return jsonError('缺少必填字段: sourceKey', 400);
        }
        if (!isManagedSourceKey(sourceKey)) {
            return jsonError('仅支持 NewAPI 和 Octopus 来源', 400);
        }

        const normalizedModelIdOverride = normalizeOptionalTextField(modelIdOverride, 'modelIdOverride');
        if (normalizedModelIdOverride.error) {
            return jsonError(normalizedModelIdOverride.error, 400);
        }

        const normalizedReasoningModelId = normalizeOptionalTextField(reasoningModelId, 'reasoningModelId');
        if (normalizedReasoningModelId.error) {
            return jsonError(normalizedReasoningModelId.error, 400);
        }

        const normalizedNotes = normalizeOptionalTextField(notes, 'notes');
        if (normalizedNotes.error) {
            return jsonError(normalizedNotes.error, 400);
        }

        if (isEnabled !== undefined && typeof isEnabled !== 'boolean') {
            return jsonError('isEnabled 必须是布尔值', 400);
        }

        if (priority !== undefined && (!Number.isInteger(priority) || priority < 0)) {
            return jsonError('priority 必须是大于等于 0 的整数', 400);
        }

        const { data, error } = await supabase.rpc('admin_create_ai_model_binding', {
            p_model_id: modelId,
            p_source_key: sourceKey,
            p_model_id_override: normalizedModelIdOverride.value ?? null,
            p_reasoning_model_id: normalizedReasoningModelId.value ?? null,
            p_is_enabled: isEnabled,
            p_priority: priority ?? null,
            p_notes: normalizedNotes.value ?? null,
        });

        if (error) {
            console.error('[ai-models] Failed to create binding transactionally:', error);
            return jsonError('创建来源失败', 500);
        }

        const result = (Array.isArray(data) ? data[0] : data) as { status?: string; binding?: Record<string, unknown> | null } | null;
        if (!result?.status) {
            console.error('[ai-models] Invalid binding create RPC result:', data);
            return jsonError('创建来源失败', 500);
        }

        if (result.status === 'model_not_found') {
            return jsonError('模型不存在', 404);
        }

        if (result.status === 'gateway_not_found') {
            return jsonError('来源网关不存在，请先在网关管理中配置', 404);
        }

        if (result.status === 'conflict') {
            return jsonError('该来源已存在', 409);
        }

        if (result.status !== 'ok' || !result.binding) {
            console.error('[ai-models] Unexpected binding create RPC status:', result.status);
            return jsonError('创建来源失败', 500);
        }

        clearModelCache();

        return jsonOk({ success: true, source: result.binding }, 201);
    } catch (e) {
        console.error('[ai-models] Invalid request body:', e);
        return jsonError('请求格式错误', 400);
    }
}
