import 'server-only';

import type {
  AIModelConfig,
  AIModelSourceConfig,
  AIVendor,
} from '@/types';
import { buildModels, clearModelCache as clearSharedModelCache } from '@/lib/ai/ai-config';
import {
  applySourceToModel,
  buildManagedApiUrl,
  DEFAULT_AI_TRANSPORT,
  getModelUsageType,
  getOrderedModelSources,
  isManagedSourceKey,
  sortModelSources,
} from '@/lib/ai/source-runtime';
import { getSystemAdminClient } from '@/lib/supabase-server';

interface DBGatewayRow {
  gateway_key: string | null;
  display_name: string | null;
  base_url: string | null;
  api_key_env_var: string | null;
  transport?: string | null;
  is_enabled?: boolean | null;
}

interface DBModelGatewayBindingRow {
  id?: string;
  model_id_override: string | null;
  reasoning_model_id: string | null;
  is_enabled: boolean;
  priority?: number | null;
  notes?: string | null;
  gateway?: DBGatewayRow | DBGatewayRow[] | null;
}

interface DBModelRow {
  model_key: string;
  display_name: string;
  vendor: string;
  usage_type?: AIModelConfig['usageType'];
  routing_mode?: AIModelConfig['routingMode'];
  supports_reasoning: boolean;
  is_reasoning_default: boolean;
  supports_vision: boolean;
  default_temperature: number | string | null;
  default_top_p?: number | string | null;
  default_presence_penalty?: number | string | null;
  default_frequency_penalty?: number | string | null;
  default_max_tokens: number | null;
  default_reasoning_effort?: AIModelConfig['defaultReasoningEffort'] | null;
  reasoning_effort_format?: AIModelConfig['reasoningEffortFormat'] | null;
  custom_parameters?: Record<string, unknown> | null;
  required_tier?: AIModelConfig['requiredTier'];
  reasoning_required_tier?: AIModelConfig['reasoningRequiredTier'];
  bindings?: DBModelGatewayBindingRow[];
}

const MODEL_SELECT = `
  model_key,
  display_name,
  vendor,
  usage_type,
  routing_mode,
  supports_reasoning,
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
  required_tier,
  reasoning_required_tier,
  bindings:ai_model_gateway_bindings (
    id,
    model_id_override,
    reasoning_model_id,
    is_enabled,
    priority,
    notes,
    gateway:ai_gateways (
      gateway_key,
      display_name,
      base_url,
      api_key_env_var,
      transport,
      is_enabled
    )
  )
`;

let dbModelsCache: AIModelConfig[] | null = null;
let dbLastFetch = 0;
const DB_CACHE_TTL = 5 * 60 * 1000;
import { IS_NODE_TEST_RUNTIME } from '@/lib/runtime';

function pickGateway(input: DBModelGatewayBindingRow['gateway']): DBGatewayRow | null {
  if (Array.isArray(input)) {
    return input[0] ?? null;
  }
  return input ?? null;
}

function buildSourcesForModel(row: DBModelRow): AIModelSourceConfig[] {
  const usageType = getModelUsageType({
    usageType: row.usage_type,
    supportsVision: row.supports_vision,
  });

  const mappedSources = (row.bindings || [])
    .map((binding): AIModelSourceConfig | null => {
      const gateway = pickGateway(binding.gateway);
      if (!gateway || !isManagedSourceKey(gateway.gateway_key)) {
        return null;
      }

      return {
        sourceKey: gateway.gateway_key,
        sourceName: gateway.display_name || gateway.gateway_key,
        apiUrl: buildManagedApiUrl(gateway.base_url, usageType),
        apiKeyEnvVar: gateway.api_key_env_var || '',
        modelIdOverride: binding.model_id_override || row.model_key,
        reasoningModelId: binding.reasoning_model_id || undefined,
        transport: (gateway.transport as AIModelConfig['transport']) || DEFAULT_AI_TRANSPORT,
        priority: binding.priority ?? undefined,
        isEnabled: binding.is_enabled !== false && gateway.is_enabled !== false,
      };
    })
    .filter((source): source is AIModelSourceConfig => source !== null);

  return sortModelSources(mappedSources).map((source, index) => ({
    ...source,
    isActive: index === 0,
  }));
}

function mapDbModelRows(rows: DBModelRow[]): AIModelConfig[] {
  return rows.map((row) => {
    const sources = buildSourcesForModel(row);

    const baseModel: AIModelConfig = {
      id: row.model_key,
      name: row.display_name,
      vendor: row.vendor as AIVendor,
      usageType: row.usage_type,
      routingMode: row.routing_mode,
      modelId: row.model_key,
      apiUrl: '',
      apiKeyEnvVar: '',
      supportsReasoning: row.supports_reasoning,
      isReasoningDefault: row.is_reasoning_default,
      supportsVision: row.supports_vision,
      defaultTemperature:
        row.default_temperature != null
          ? Number.parseFloat(String(row.default_temperature))
          : undefined,
      defaultTopP:
        row.default_top_p != null
          ? Number.parseFloat(String(row.default_top_p))
          : undefined,
      defaultPresencePenalty:
        row.default_presence_penalty != null
          ? Number.parseFloat(String(row.default_presence_penalty))
          : undefined,
      defaultFrequencyPenalty:
        row.default_frequency_penalty != null
          ? Number.parseFloat(String(row.default_frequency_penalty))
          : undefined,
      defaultMaxTokens: row.default_max_tokens ?? undefined,
      defaultReasoningEffort: row.default_reasoning_effort ?? undefined,
      reasoningEffortFormat: row.reasoning_effort_format ?? undefined,
      customParameters: row.custom_parameters ?? null,
      requiredTier: row.required_tier,
      reasoningRequiredTier: row.reasoning_required_tier,
      transport: DEFAULT_AI_TRANSPORT,
      sources,
    };

    if (sources.length === 0) {
      return baseModel;
    }

    return applySourceToModel(baseModel, sources[0]);
  });
}

function hasAvailableSource(model: AIModelConfig): boolean {
  return getOrderedModelSources(model).some((source) => {
    if (!source.apiUrl || !source.apiKeyEnvVar) {
      return false;
    }
    return !!process.env[source.apiKeyEnvVar];
  });
}

async function fetchModelsFromDB(): Promise<AIModelConfig[] | null> {
  const now = Date.now();
  if (dbModelsCache && now - dbLastFetch < DB_CACHE_TTL) {
    return dbModelsCache;
  }

  let supabase;
  try {
    supabase = getSystemAdminClient();
  } catch (error) {
    if (!IS_NODE_TEST_RUNTIME) {
      console.warn('[ai-config/server] Supabase client unavailable, fallback to env models:', error);
    }
    return null;
  }

  const modelQuery = supabase.from('ai_models') as unknown as {
    select?: (columns: string) => {
      eq: (column: string, value: unknown) => {
        order: (column: string, options: { ascending: boolean }) => Promise<{
          data: unknown[] | null;
          error: unknown;
        }>;
      };
    };
  };
  if (!modelQuery?.select) {
    return null;
  }

  let data: unknown[] | null = null;
  let error: unknown = null;
  try {
    const result = await modelQuery
      .select(MODEL_SELECT)
      .eq('is_enabled', true)
      .order('sort_order', { ascending: true });
    data = result.data;
    error = result.error;
  } catch {
    return null;
  }

  if (error) {
    console.error('[ai-config/server] Failed to fetch from DB:', error);
    return null;
  }

  if (!data) {
    return null;
  }

  dbModelsCache = mapDbModelRows(data as DBModelRow[]);
  dbLastFetch = now;
  return dbModelsCache;
}

export async function getModelsAsync(): Promise<AIModelConfig[]> {
  const dbModels = await fetchModelsFromDB();
  if (dbModels !== null) {
    return dbModels;
  }
  return buildModels();
}

export async function getModelsByUsageTypeAsync(
  usageType: NonNullable<AIModelConfig['usageType']>
): Promise<AIModelConfig[]> {
  const models = await getModelsAsync();
  return models.filter((model) => getModelUsageType(model) === usageType);
}

export async function getDefaultModelConfigAsync(
  usageType: NonNullable<AIModelConfig['usageType']> = 'chat'
): Promise<AIModelConfig | undefined> {
  const models = await getModelsByUsageTypeAsync(usageType);
  return models.find((model) => hasAvailableSource(model));
}

export async function getModelConfigAsync(
  modelId: string
): Promise<AIModelConfig | undefined> {
  const models = await getModelsAsync();
  const direct = models.find((model) => model.id === modelId);
  if (direct) return direct;
  if (modelId === 'deepseek-chat' || modelId === 'deepseek') {
    return models.find((model) => model.id === 'deepseek-v3.2');
  }
  return undefined;
}

export function clearModelCache(): void {
  clearSharedModelCache();
  dbModelsCache = null;
  dbLastFetch = 0;
  console.info('[ai-config/server] Model cache cleared');
}
