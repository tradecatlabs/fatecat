/**
 * AI 模型管理面板
 *
 * 功能：
 * - 查看所有模型及其配置
 * - 启用/禁用模型
 * - 修改模型参数
 * - 切换活跃来源
 */
'use client';

import { useState, useEffect, useCallback } from 'react';
import {
    RefreshCw,
    Check,
    ChevronDown,
    ChevronUp,
    Zap,
    Eye,
    Plus,
    Layers,
    Pencil,
    Save,
    Trash2,
} from 'lucide-react';
import { requestBrowserData } from '@/lib/browser-api';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { ConfirmDialog } from '@/components/ui/ConfirmDialog';
import { useToast } from '@/components/ui/Toast';
import { invalidateQueriesForPath } from '@/lib/query/invalidation';
import { getVendorIcon } from '@/lib/ai/vendor-config';
import { getVendorName, VENDOR_PRESETS as VENDOR_PRESET_KEYS } from '@/lib/ai/ai-config';

// 类型定义
interface ModelSource {
    id: string;
    sourceKey: string;
    sourceName: string;
    apiUrl: string;
    apiKeyEnvVar: string;
    transport?: 'openai_compatible';
    hasApiKey: boolean;
    modelIdOverride: string | null;
    reasoningModelId: string | null;
    isActive: boolean;
    isEnabled: boolean;
    priority: number;
    notes: string | null;
}

interface AIModel {
    id: string;
    modelKey: string;
    displayName: string;
    vendor: string;
    usageType: 'chat' | 'vision' | 'embedding' | 'rerank';
    routingMode: 'auto' | 'newapi' | 'octopus';
    isEnabled: boolean;
    sortOrder: number;
    requiredTier: 'free' | 'plus' | 'pro';
    supportsReasoning: boolean;
    reasoningRequiredTier: string;
    isReasoningDefault: boolean;
    supportsVision: boolean;
    defaultTemperature: number;
    defaultTopP: number | null;
    defaultPresencePenalty: number | null;
    defaultFrequencyPenalty: number | null;
    defaultMaxTokens: number | null;
    defaultReasoningEffort: 'minimal' | 'low' | 'medium' | 'high' | null;
    reasoningEffortFormat: 'reasoning_object' | 'reasoning_effort' | null;
    customParameters: Record<string, unknown> | null;
    description: string | null;
    sources: ModelSource[];
}

type CreateVendorPreset = string;

type ManagedGatewayKey = 'newapi' | 'octopus';

type CreateModelDraft = {
    modelKey: string;
    displayName: string;
    vendorPreset: CreateVendorPreset;
    customVendor: string;
    usageType: AIModel['usageType'];
    routingMode: AIModel['routingMode'];
    primaryGatewayKey: ManagedGatewayKey;
    requiredTier: AIModel['requiredTier'];
    supportsReasoning: boolean;
    reasoningRequiredTier: string;
    isReasoningDefault: boolean;
    supportsVision: boolean;
    defaultTemperature: number;
    defaultTopP: number | null;
    defaultPresencePenalty: number | null;
    defaultFrequencyPenalty: number | null;
    defaultMaxTokens: number | null;
    defaultReasoningEffort: AIModel['defaultReasoningEffort'];
    reasoningEffortFormat: AIModel['reasoningEffortFormat'];
    customParametersText: string;
    description: string;
};

type SourceDraft = {
    modelIdOverride: string;
    reasoningModelId: string;
    priority: number;
    isEnabled: boolean;
    notes: string;
};

type EditModelDraft = {
    modelKey: string;
    displayName: string;
    vendorPreset: CreateVendorPreset;
    customVendor: string;
    usageType: AIModel['usageType'];
    routingMode: AIModel['routingMode'];
    requiredTier: AIModel['requiredTier'];
    sortOrder: number;
    supportsReasoning: boolean;
    reasoningRequiredTier: string;
    isReasoningDefault: boolean;
    supportsVision: boolean;
    defaultTemperature: number;
    defaultTopP: number | null;
    defaultPresencePenalty: number | null;
    defaultFrequencyPenalty: number | null;
    defaultMaxTokens: number | null;
    defaultReasoningEffort: AIModel['defaultReasoningEffort'];
    reasoningEffortFormat: AIModel['reasoningEffortFormat'];
    customParametersText: string;
    description: string;
};

const TIER_LABELS: Record<string, { label: string; color: string }> = {
    free: { label: 'Free', color: 'text-gray-500 bg-gray-500/10' },
    plus: { label: 'Plus', color: 'text-amber-500 bg-amber-500/10' },
    pro: { label: 'Pro', color: 'text-purple-500 bg-purple-500/10' },
};

const VENDOR_PRESETS: Array<{ value: string; label: string }> =
    VENDOR_PRESET_KEYS.map(v => ({ value: v, label: getVendorName(v) }));

const USAGE_TYPE_LABELS: Record<AIModel['usageType'], string> = {
    chat: '聊天',
    vision: '视觉',
    embedding: 'Embedding',
    rerank: 'Rerank',
};

const ROUTING_MODE_LABELS: Record<AIModel['routingMode'], string> = {
    auto: '自动故障转移',
    newapi: '固定 NewAPI',
    octopus: '固定 Octopus',
};

function createInitialNewModel(): CreateModelDraft {
    return {
        modelKey: '',
        displayName: '',
        vendorPreset: 'deepseek',
        customVendor: '',
        usageType: 'chat',
        routingMode: 'auto',
        primaryGatewayKey: 'newapi',
        requiredTier: 'free',
        supportsReasoning: false,
        reasoningRequiredTier: 'plus',
        isReasoningDefault: false,
        supportsVision: false,
        defaultTemperature: 0.7,
        defaultTopP: null,
        defaultPresencePenalty: null,
        defaultFrequencyPenalty: null,
        defaultMaxTokens: null,
        defaultReasoningEffort: null,
        reasoningEffortFormat: 'reasoning_object',
        customParametersText: '',
        description: '',
    };
}

function resolveDraftVendor(model: CreateModelDraft): string {
    return model.vendorPreset === '__custom__'
        ? model.customVendor.trim()
        : model.vendorPreset;
}

function resolveVendorDraft(vendor: string): Pick<EditModelDraft, 'vendorPreset' | 'customVendor'> {
    const matchedPreset = VENDOR_PRESETS.find((preset) => preset.value === vendor);
    if (matchedPreset) {
        return {
            vendorPreset: matchedPreset.value,
            customVendor: '',
        };
    }
    return {
        vendorPreset: '__custom__',
        customVendor: vendor,
    };
}

function createEditModelDraft(model: AIModel): EditModelDraft {
    return {
        modelKey: model.modelKey,
        displayName: model.displayName,
        ...resolveVendorDraft(model.vendor),
        usageType: model.usageType,
        routingMode: model.routingMode,
        requiredTier: model.requiredTier,
        sortOrder: model.sortOrder,
        supportsReasoning: model.supportsReasoning,
        reasoningRequiredTier: model.reasoningRequiredTier,
        isReasoningDefault: model.isReasoningDefault,
        supportsVision: model.supportsVision,
        defaultTemperature: model.defaultTemperature,
        defaultTopP: model.defaultTopP,
        defaultPresencePenalty: model.defaultPresencePenalty,
        defaultFrequencyPenalty: model.defaultFrequencyPenalty,
        defaultMaxTokens: model.defaultMaxTokens,
        defaultReasoningEffort: model.defaultReasoningEffort,
        reasoningEffortFormat: model.reasoningEffortFormat,
        customParametersText: model.customParameters ? JSON.stringify(model.customParameters, null, 2) : '',
        description: model.description || '',
    };
}

function createInitialSourceDraft(): SourceDraft {
    return {
        modelIdOverride: '',
        reasoningModelId: '',
        priority: 0,
        isEnabled: true,
        notes: '',
    };
}

function normalizeSourceModelIdInput(modelIdOverride: string, modelKey: string): string | null {
    const normalizedOverride = modelIdOverride.trim();
    const normalizedModelKey = modelKey.trim();
    if (!normalizedOverride || normalizedOverride === normalizedModelKey) {
        return null;
    }
    return normalizedOverride;
}

function getSourceModelIdState(modelKey: string, modelIdOverride: string | null) {
    const normalizedModelKey = modelKey.trim();
    const normalizedOverride = modelIdOverride?.trim();
    if (!normalizedOverride || normalizedOverride === normalizedModelKey) {
        return {
            value: normalizedModelKey,
            inherited: true,
        };
    }
    return {
        value: normalizedOverride,
        inherited: false,
    };
}

export function AIModelPanel() {
    const [models, setModels] = useState<AIModel[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [expandedModel, setExpandedModel] = useState<string | null>(null);
    const [updating, setUpdating] = useState<string | null>(null);
    const [showCreateForm, setShowCreateForm] = useState(false);
    const [showCreateAdvanced, setShowCreateAdvanced] = useState(false);
    const [modelDrafts, setModelDrafts] = useState<Record<string, EditModelDraft>>({});
    const [addingToModel, setAddingToModel] = useState<string | null>(null);
    const [editingSourceId, setEditingSourceId] = useState<string | null>(null);
    const [editingDraft, setEditingDraft] = useState<SourceDraft | null>(null);
    const [deleteTarget, setDeleteTarget] = useState<{ modelId: string; sourceId: string } | null>(null);
    const [deleteModelTarget, setDeleteModelTarget] = useState<{ modelId: string; displayName: string } | null>(null);
    const { showToast } = useToast();
    const [newModel, setNewModel] = useState<CreateModelDraft>(createInitialNewModel);
    const [newSource, setNewSource] = useState(() => ({
        sourceKey: 'newapi' as ManagedGatewayKey,
        ...createInitialSourceDraft(),
    }));

    const resetNewModel = () => {
        setNewModel(createInitialNewModel());
    };

    const resetNewSource = () => {
        setNewSource({
            sourceKey: 'newapi',
            ...createInitialSourceDraft(),
        });
    };

    // 加载模型列表
    const loadModels = useCallback(async () => {
        setLoading(true);
        setError(null);

        try {
            const data = await requestBrowserData<{ models?: AIModel[] }>(
                '/api/admin/ai-models?includeDisabled=true',
                { method: 'GET' },
                { fallbackMessage: '获取模型列表失败' },
            );
            const loadedModels = data.models || [];
            setModels(loadedModels);
            setModelDrafts(
                Object.fromEntries(
                    loadedModels.map((model: AIModel) => [model.id, createEditModelDraft(model)])
                )
            );
        } catch (e) {
            setError(e instanceof Error ? e.message : '获取模型列表失败');
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadModels();
    }, [loadModels]);

    const parseCustomParametersText = (input: string): Record<string, unknown> | null => {
        const trimmed = input.trim();
        if (!trimmed) {
            return null;
        }
        const parsed = JSON.parse(trimmed);
        if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
            throw new Error('自定义参数必须是 JSON 对象');
        }
        return parsed as Record<string, unknown>;
    };

    const updateNewModel = (updates: Partial<CreateModelDraft>) => {
        setNewModel((current) => ({ ...current, ...updates }));
    };

    const updateModelDraft = (modelId: string, updates: Partial<EditModelDraft>) => {
        setModelDrafts((current) => ({
            ...current,
            [modelId]: {
                ...current[modelId],
                ...updates,
            },
        }));
    };

    const handleCreateRoutingModeChange = (routingMode: AIModel['routingMode']) => {
        updateNewModel({
            routingMode,
            primaryGatewayKey:
                routingMode === 'newapi' || routingMode === 'octopus'
                    ? routingMode
                    : newModel.primaryGatewayKey,
        });
    };

    const handleCreatePrimaryGatewayChange = (primaryGatewayKey: ManagedGatewayKey) => {
        updateNewModel({
            primaryGatewayKey,
            routingMode:
                newModel.routingMode === 'newapi' || newModel.routingMode === 'octopus'
                    ? primaryGatewayKey
                    : newModel.routingMode,
        });
    };

    // 更新模型
    const updateModel = async (modelId: string, updates: Partial<AIModel>) => {
        setUpdating(modelId);

        try {
            await requestBrowserData(
                `/api/admin/ai-models/${modelId}`,
                {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(updates),
                },
                { fallbackMessage: '更新失败' },
            );

            // 刷新列表
            await loadModels();
            invalidateQueriesForPath('/api/admin/ai-models');
        } catch (e) {
            console.error('Update model failed:', e);
            showToast('error', e instanceof Error ? e.message : '更新失败');
        } finally {
            setUpdating(null);
        }
    };

    const createModel = async () => {
        const vendor = resolveDraftVendor(newModel);

        if (!newModel.modelKey.trim() || !newModel.displayName.trim()) {
            showToast('warning', '请填写模型 ID 和显示名称');
            return;
        }
        if (!vendor) {
            showToast('warning', '请选择供应商，或填写自定义供应商');
            return;
        }

        setUpdating('creating');
        try {
            const customParameters = parseCustomParametersText(newModel.customParametersText);

            await requestBrowserData(
                '/api/admin/ai-models',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        modelKey: newModel.modelKey.trim(),
                        displayName: newModel.displayName.trim(),
                        vendor,
                        usageType: newModel.usageType,
                        routingMode: newModel.routingMode,
                        primaryGatewayKey: newModel.primaryGatewayKey,
                        requiredTier: newModel.requiredTier,
                        supportsReasoning: newModel.supportsReasoning,
                        reasoningRequiredTier: newModel.reasoningRequiredTier,
                        isReasoningDefault: newModel.isReasoningDefault,
                        supportsVision: newModel.supportsVision,
                        defaultTemperature: newModel.defaultTemperature,
                        defaultTopP: newModel.defaultTopP,
                        defaultPresencePenalty: newModel.defaultPresencePenalty,
                        defaultFrequencyPenalty: newModel.defaultFrequencyPenalty,
                        defaultMaxTokens: newModel.defaultMaxTokens,
                        defaultReasoningEffort: newModel.supportsReasoning ? newModel.defaultReasoningEffort : null,
                        reasoningEffortFormat: newModel.supportsReasoning ? newModel.reasoningEffortFormat : null,
                        customParameters,
                        description: newModel.description.trim() || undefined,
                    }),
                },
                { fallbackMessage: '创建模型失败' },
            );

            showToast('success', '模型已创建');
            setShowCreateForm(false);
            setShowCreateAdvanced(false);
            resetNewModel();
            await loadModels();
            invalidateQueriesForPath('/api/admin/ai-models');
        } catch (e) {
            showToast('error', e instanceof Error ? e.message : '创建模型失败');
        } finally {
            setUpdating(null);
        }
    };

    const saveModelSettings = async (modelId: string) => {
        const draft = modelDrafts[modelId];
        if (!draft) return;

        const vendor = draft.vendorPreset === '__custom__'
            ? draft.customVendor.trim()
            : draft.vendorPreset;

        if (!draft.modelKey.trim() || !draft.displayName.trim()) {
            showToast('warning', '请填写模型 ID 和显示名称');
            return;
        }
        if (!vendor) {
            showToast('warning', '请选择供应商，或填写自定义供应商');
            return;
        }

        try {
            const customParameters = parseCustomParametersText(draft.customParametersText);
            await updateModel(modelId, {
                modelKey: draft.modelKey.trim(),
                displayName: draft.displayName.trim(),
                vendor,
                usageType: draft.usageType,
                routingMode: draft.routingMode,
                requiredTier: draft.requiredTier,
                sortOrder: draft.sortOrder,
                supportsReasoning: draft.supportsReasoning,
                reasoningRequiredTier: draft.reasoningRequiredTier,
                isReasoningDefault: draft.supportsReasoning ? draft.isReasoningDefault : false,
                supportsVision: draft.supportsVision,
                defaultTemperature: draft.defaultTemperature,
                defaultTopP: draft.defaultTopP,
                defaultPresencePenalty: draft.defaultPresencePenalty,
                defaultFrequencyPenalty: draft.defaultFrequencyPenalty,
                defaultMaxTokens: draft.defaultMaxTokens,
                defaultReasoningEffort: draft.supportsReasoning ? draft.defaultReasoningEffort : null,
                reasoningEffortFormat: draft.supportsReasoning ? draft.reasoningEffortFormat : null,
                customParameters,
                description: draft.description.trim() || null,
            } as Partial<AIModel> & { modelKey: string });
        } catch (error) {
            showToast('error', error instanceof Error ? error.message : '自定义参数格式错误');
        }
    };

    // 切换活跃来源
    const activateSource = async (modelId: string, sourceId: string) => {
        setUpdating(modelId);

        try {
            await requestBrowserData(
                `/api/admin/ai-models/${modelId}/sources/${sourceId}`,
                {
                    method: 'POST',
                },
                { fallbackMessage: '切换来源失败' },
            );

            // 刷新列表
            await loadModels();
        } catch (e) {
            console.error('Activate source failed:', e);
            showToast('error', e instanceof Error ? e.message : '切换来源失败');
        } finally {
            setUpdating(null);
        }
    };

    const beginEditSource = (source: ModelSource, modelKey: string) => {
        setEditingSourceId(source.id);
        setEditingDraft({
            modelIdOverride: normalizeSourceModelIdInput(source.modelIdOverride || '', modelKey) || '',
            reasoningModelId: source.reasoningModelId || '',
            priority: source.priority,
            isEnabled: source.isEnabled,
            notes: source.notes || '',
        });
    };

    const saveSource = async (modelId: string, sourceId: string, modelKey: string) => {
        if (!editingDraft) return;

        setUpdating(modelId);
        try {
            await requestBrowserData(
                `/api/admin/ai-models/${modelId}/sources/${sourceId}`,
                {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        modelIdOverride: normalizeSourceModelIdInput(editingDraft.modelIdOverride, modelKey),
                        reasoningModelId: editingDraft.reasoningModelId.trim() || null,
                        priority: editingDraft.priority,
                        isEnabled: editingDraft.isEnabled,
                        notes: editingDraft.notes.trim() || null,
                    }),
                },
                { fallbackMessage: '保存来源失败' },
            );

            setEditingSourceId(null);
            setEditingDraft(null);
            await loadModels();
            invalidateQueriesForPath('/api/admin/ai-models');
            showToast('success', '来源已更新');
        } catch (e) {
            showToast('error', e instanceof Error ? e.message : '保存来源失败');
        } finally {
            setUpdating(null);
        }
    };

    const addSource = async (modelId: string, modelKey: string) => {
        setUpdating(modelId);
        try {
            await requestBrowserData(
                `/api/admin/ai-models/${modelId}/sources`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        sourceKey: newSource.sourceKey,
                        modelIdOverride: normalizeSourceModelIdInput(newSource.modelIdOverride, modelKey),
                        reasoningModelId: newSource.reasoningModelId.trim() || null,
                        priority: newSource.priority,
                        isEnabled: newSource.isEnabled,
                        notes: newSource.notes.trim() || null,
                    }),
                },
                { fallbackMessage: '添加来源失败' },
            );

            setAddingToModel(null);
            resetNewSource();
            await loadModels();
            invalidateQueriesForPath('/api/admin/ai-models');
            showToast('success', '来源已添加');
        } catch (e) {
            showToast('error', e instanceof Error ? e.message : '添加来源失败');
        } finally {
            setUpdating(null);
        }
    };

    const deleteSource = async (modelId: string, sourceId: string) => {
        setUpdating(modelId);
        try {
            await requestBrowserData(
                `/api/admin/ai-models/${modelId}/sources/${sourceId}`,
                {
                    method: 'DELETE',
                },
                { fallbackMessage: '删除来源失败' },
            );

            await loadModels();
            invalidateQueriesForPath('/api/admin/ai-models');
            setDeleteTarget(null);
            showToast('success', '来源已删除');
        } catch (e) {
            showToast('error', e instanceof Error ? e.message : '删除来源失败');
        } finally {
            setUpdating(null);
        }
    };

    const deleteModel = async (modelId: string) => {
        setUpdating(modelId);
        try {
            await requestBrowserData(
                `/api/admin/ai-models/${modelId}`,
                {
                    method: 'DELETE',
                },
                { fallbackMessage: '删除模型失败' },
            );

            if (expandedModel === modelId) {
                setExpandedModel(null);
            }
            setDeleteModelTarget(null);
            await loadModels();
            invalidateQueriesForPath('/api/admin/ai-models');
            showToast('success', '模型已删除');
        } catch (e) {
            showToast('error', e instanceof Error ? e.message : '删除模型失败');
        } finally {
            setUpdating(null);
        }
    };

    // 清除缓存
    const clearCache = async () => {
        try {
            await requestBrowserData(
                '/api/admin/ai-models/cache',
                {
                    method: 'POST',
                },
                { fallbackMessage: '清除缓存失败' },
            );
            invalidateQueriesForPath('/api/admin/ai-models/cache');
            showToast('success', '缓存已清除');
        } catch (e) {
            console.error('Clear cache failed:', e);
        }
    };

    if (loading) {
        return <SoundWaveLoader variant="block" />;
    }

    if (error) {
        return (
            <div className="text-center py-12">
                <p className="text-red-500 mb-4">{error}</p>
                <button
                    onClick={loadModels}
                    className="px-4 py-2 rounded-lg bg-accent text-white hover:bg-accent/90"
                >
                    重试
                </button>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {/* 工具栏 */}
            <div className="flex items-center justify-between mb-4">
                <p className="text-sm text-foreground-secondary">
                    共 {models.length} 个模型
                </p>
                <div className="flex gap-2">
                    <button
                        onClick={() => setShowCreateForm((value) => !value)}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm bg-accent text-white hover:bg-accent/90 transition-colors"
                    >
                        <Plus className="w-3.5 h-3.5" />
                        新增模型
                    </button>
                    <button
                        onClick={clearCache}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm bg-background-secondary hover:bg-background-secondary/80 transition-colors"
                    >
                        <RefreshCw className="w-3.5 h-3.5" />
                        清除缓存
                    </button>
                </div>
            </div>

            {showCreateForm && (
                <div className="border border-border rounded-xl p-4 bg-background-secondary/30 space-y-4">
                    <div className="flex items-center justify-between">
                        <h3 className="text-sm font-medium">创建模型</h3>
                        <button
                            onClick={() => {
                                setShowCreateForm(false);
                                setShowCreateAdvanced(false);
                                resetNewModel();
                            }}
                            className="text-xs text-foreground-secondary hover:text-foreground"
                        >
                            取消
                        </button>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-xs text-foreground-secondary mb-1">模型 ID</label>
                            <input
                                type="text"
                                value={newModel.modelKey}
                                onChange={(e) => updateNewModel({ modelKey: e.target.value })}
                                placeholder="deepseek-v3.2"
                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                            />
                        </div>
                        <div>
                            <label className="block text-xs text-foreground-secondary mb-1">显示名称</label>
                            <input
                                type="text"
                                value={newModel.displayName}
                                onChange={(e) => updateNewModel({ displayName: e.target.value })}
                                placeholder="DeepSeek V3.2"
                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                            />
                        </div>
                        <div>
                            <label className="block text-xs text-foreground-secondary mb-1">供应商</label>
                            <select
                                value={newModel.vendorPreset}
                                onChange={(e) => updateNewModel({ vendorPreset: e.target.value as CreateVendorPreset })}
                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                            >
                                {VENDOR_PRESETS.map((vendor) => (
                                    <option key={vendor.value} value={vendor.value}>
                                        {vendor.label}
                                    </option>
                                ))}
                                <option value="__custom__">自定义供应商</option>
                            </select>
                            {newModel.vendorPreset === '__custom__' && (
                                <input
                                    type="text"
                                    value={newModel.customVendor}
                                    onChange={(e) => updateNewModel({ customVendor: e.target.value })}
                                    placeholder="添加供应商，如 ChatGPT"
                                    className="mt-2 w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                />
                            )}
                        </div>
                        <div>
                            <label className="block text-xs text-foreground-secondary mb-1">模型类型</label>
                            <select
                                value={newModel.usageType}
                                onChange={(e) => updateNewModel({ usageType: e.target.value as AIModel['usageType'] })}
                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                            >
                                <option value="chat">聊天</option>
                                <option value="vision">视觉</option>
                                <option value="embedding">Embedding</option>
                                <option value="rerank">Rerank</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-xs text-foreground-secondary mb-1">路由模式</label>
                            <select
                                value={newModel.routingMode}
                                onChange={(e) => handleCreateRoutingModeChange(e.target.value as AIModel['routingMode'])}
                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                            >
                                <option value="auto">自动故障转移</option>
                                <option value="newapi">固定 NewAPI</option>
                                <option value="octopus">固定 Octopus</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-xs text-foreground-secondary mb-1">主绑定网关</label>
                            <select
                                value={newModel.primaryGatewayKey}
                                onChange={(e) => handleCreatePrimaryGatewayChange(e.target.value as ManagedGatewayKey)}
                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                            >
                                <option value="newapi">NewAPI</option>
                                <option value="octopus">Octopus</option>
                            </select>
                            <p className="mt-1 text-[11px] text-foreground-secondary">
                                创建时直接绑定主网关；若选择自动故障转移，后续可再添加备用来源。
                            </p>
                        </div>
                        <div>
                            <label className="block text-xs text-foreground-secondary mb-1">会员等级</label>
                            <select
                                value={newModel.requiredTier}
                                onChange={(e) => updateNewModel({ requiredTier: e.target.value as AIModel['requiredTier'] })}
                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                            >
                                <option value="free">Free</option>
                                <option value="plus">Plus</option>
                                <option value="pro">Pro</option>
                            </select>
                        </div>
                        <div className="col-span-2">
                            <label className="block text-xs text-foreground-secondary mb-1">描述</label>
                            <input
                                type="text"
                                value={newModel.description}
                                onChange={(e) => updateNewModel({ description: e.target.value })}
                                placeholder="可选"
                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                            />
                        </div>
                    </div>
                    <div className="flex flex-wrap gap-4 text-sm">
                        <label className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                checked={newModel.supportsReasoning}
                                onChange={(e) => setNewModel({
                                    ...newModel,
                                    supportsReasoning: e.target.checked,
                                    isReasoningDefault: e.target.checked ? newModel.isReasoningDefault : false,
                                })}
                            />
                            支持推理
                        </label>
                        <label className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                checked={newModel.isReasoningDefault}
                                disabled={!newModel.supportsReasoning}
                                onChange={(e) => updateNewModel({ isReasoningDefault: e.target.checked })}
                            />
                            默认开启推理
                        </label>
                        <label className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                checked={newModel.supportsVision}
                                onChange={(e) => updateNewModel({ supportsVision: e.target.checked })}
                            />
                            支持视觉
                        </label>
                    </div>
                    {newModel.supportsReasoning && (
                        <div>
                            <label className="block text-xs text-foreground-secondary mb-1">推理等级</label>
                            <select
                                value={newModel.reasoningRequiredTier}
                                onChange={(e) => updateNewModel({ reasoningRequiredTier: e.target.value })}
                                className="w-full max-w-xs px-3 py-2 rounded-lg border border-border bg-background text-sm"
                            >
                                <option value="free">Free</option>
                                <option value="plus">Plus</option>
                                <option value="pro">Pro</option>
                            </select>
                        </div>
                    )}
                    <div className="pt-2 border-t border-border/70">
                        <button
                            type="button"
                            onClick={() => setShowCreateAdvanced((value) => !value)}
                            className="flex items-center gap-2 text-sm font-medium text-foreground-secondary hover:text-foreground"
                        >
                            {showCreateAdvanced ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                            高级设置
                        </button>
                    </div>
                    {showCreateAdvanced && (
                        <div className="space-y-4 rounded-xl border border-border bg-background/70 p-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-xs text-foreground-secondary mb-1">默认温度</label>
                                    <input
                                        type="number"
                                        min="0"
                                        max="2"
                                        step="0.1"
                                        value={newModel.defaultTemperature}
                                        onChange={(e) => setNewModel({ ...newModel, defaultTemperature: parseFloat(e.target.value || '0.7') })}
                                        className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs text-foreground-secondary mb-1">Top P</label>
                                    <label className="flex items-center gap-2 text-sm mb-2">
                                        <input
                                            type="checkbox"
                                            checked={newModel.defaultTopP !== null}
                                            onChange={(e) => setNewModel({
                                                ...newModel,
                                                defaultTopP: e.target.checked ? 1 : null,
                                            })}
                                        />
                                        启用 Top P
                                    </label>
                                    {newModel.defaultTopP !== null && (
                                        <input
                                            type="number"
                                            min="0"
                                            max="1"
                                            step="0.1"
                                            value={newModel.defaultTopP}
                                            onChange={(e) => setNewModel({ ...newModel, defaultTopP: parseFloat(e.target.value || '1') })}
                                            className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                        />
                                    )}
                                </div>
                                <div>
                                    <label className="block text-xs text-foreground-secondary mb-1">Presence Penalty</label>
                                    <label className="flex items-center gap-2 text-sm mb-2">
                                        <input
                                            type="checkbox"
                                            checked={newModel.defaultPresencePenalty !== null}
                                            onChange={(e) => setNewModel({
                                                ...newModel,
                                                defaultPresencePenalty: e.target.checked ? 0 : null,
                                            })}
                                        />
                                        启用 Presence Penalty
                                    </label>
                                    {newModel.defaultPresencePenalty !== null && (
                                        <input
                                            type="number"
                                            min="-2"
                                            max="2"
                                            step="0.1"
                                            value={newModel.defaultPresencePenalty}
                                            onChange={(e) => setNewModel({
                                                ...newModel,
                                                defaultPresencePenalty: parseFloat(e.target.value || '0'),
                                            })}
                                            className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                        />
                                    )}
                                </div>
                                <div>
                                    <label className="block text-xs text-foreground-secondary mb-1">Frequency Penalty</label>
                                    <label className="flex items-center gap-2 text-sm mb-2">
                                        <input
                                            type="checkbox"
                                            checked={newModel.defaultFrequencyPenalty !== null}
                                            onChange={(e) => setNewModel({
                                                ...newModel,
                                                defaultFrequencyPenalty: e.target.checked ? 0 : null,
                                            })}
                                        />
                                        启用 Frequency Penalty
                                    </label>
                                    {newModel.defaultFrequencyPenalty !== null && (
                                        <input
                                            type="number"
                                            min="-2"
                                            max="2"
                                            step="0.1"
                                            value={newModel.defaultFrequencyPenalty}
                                            onChange={(e) => setNewModel({
                                                ...newModel,
                                                defaultFrequencyPenalty: parseFloat(e.target.value || '0'),
                                            })}
                                            className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                        />
                                    )}
                                </div>
                                <div className="col-span-2">
                                    <label className="flex items-center gap-2 text-sm mb-2">
                                        <input
                                            type="checkbox"
                                            checked={newModel.defaultMaxTokens !== null}
                                            onChange={(e) => setNewModel({
                                                ...newModel,
                                                defaultMaxTokens: e.target.checked ? 4000 : null,
                                            })}
                                        />
                                        启用最大输出限制（Cherry 默认不强制写死）
                                    </label>
                                    {newModel.defaultMaxTokens !== null && (
                                        <input
                                            type="number"
                                            min="1"
                                            step="1"
                                            value={newModel.defaultMaxTokens}
                                            onChange={(e) => setNewModel({ ...newModel, defaultMaxTokens: parseInt(e.target.value || '4000', 10) })}
                                            className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                        />
                                    )}
                                </div>
                                {newModel.supportsReasoning && (
                                    <>
                                        <div>
                                            <label className="block text-xs text-foreground-secondary mb-1">默认思考等级</label>
                                            <select
                                                value={newModel.defaultReasoningEffort || ''}
                                                onChange={(e) => setNewModel({
                                                    ...newModel,
                                                    defaultReasoningEffort: (e.target.value || null) as AIModel['defaultReasoningEffort'],
                                                })}
                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                            >
                                                <option value="">不设置</option>
                                                <option value="minimal">Minimal</option>
                                                <option value="low">Low</option>
                                                <option value="medium">Medium</option>
                                                <option value="high">High</option>
                                            </select>
                                        </div>
                                        <div>
                                            <label className="block text-xs text-foreground-secondary mb-1">思考等级参数格式</label>
                                            <select
                                                value={newModel.reasoningEffortFormat || 'reasoning_object'}
                                                onChange={(e) => setNewModel({
                                                    ...newModel,
                                                    reasoningEffortFormat: e.target.value as AIModel['reasoningEffortFormat'],
                                                })}
                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                            >
                                                <option value="reasoning_object">reasoning.effort</option>
                                                <option value="reasoning_effort">reasoning_effort</option>
                                            </select>
                                        </div>
                                    </>
                                )}
                                <div className="col-span-2">
                                    <label className="block text-xs text-foreground-secondary mb-1">自定义参数</label>
                                    <textarea
                                        value={newModel.customParametersText}
                                        onChange={(e) => setNewModel({ ...newModel, customParametersText: e.target.value })}
                                        rows={6}
                                        placeholder={'{\n  "presence_penalty": 0.5,\n  "frequency_penalty": 0.2,\n  "reasoning": { "effort": "high" }\n}'}
                                        className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm font-mono"
                                    />
                                    <p className="text-[11px] text-foreground-secondary mt-1">
                                        Cherry 风格做法：模型专属参数如 `presence_penalty`、`frequency_penalty`、供应商私有字段放这里。这里会在基础参数之后合并并覆盖。
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}
                    <div className="flex justify-end">
                        <button
                            onClick={createModel}
                            disabled={updating === 'creating'}
                            className="px-4 py-2 rounded-lg bg-accent text-white hover:bg-accent/90 disabled:opacity-50 text-sm"
                        >
                            {updating === 'creating' ? '创建中...' : '创建模型'}
                        </button>
                    </div>
                </div>
            )}

            {/* 模型列表 */}
            <div className="space-y-3">
                {models.map(model => {
                    const isExpanded = expandedModel === model.id;
                    const isUpdating = updating === model.id;
                    const activeSource = model.sources.find(s => s.isActive);
                    const tierInfo = TIER_LABELS[model.requiredTier];
                    const modelDraft = modelDrafts[model.id] || createEditModelDraft(model);
                    const isAddingHere = addingToModel === model.id;
                    const availableGatewayOptions = (['newapi', 'octopus'] as ManagedGatewayKey[]).filter(
                        (gatewayKey) => !model.sources.some((source) => source.sourceKey === gatewayKey)
                    );

                    return (
                        <div
                            key={model.id}
                            className="border border-border rounded-xl overflow-hidden"
                        >
                            {/* 模型头部 */}
                            <div
                                className="flex items-center justify-between p-4 cursor-pointer hover:bg-background-secondary/50 transition-colors"
                                onClick={() => setExpandedModel(isExpanded ? null : model.id)}
                            >
                                <div className="flex items-center gap-3">
                                    {/* 启用状态 */}
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            updateModel(model.id, { isEnabled: !model.isEnabled });
                                        }}
                                        disabled={isUpdating}
                                        className={`w-10 h-6 rounded-full relative transition-colors ${model.isEnabled ? 'bg-green-500' : 'bg-background-tertiary'
                                            }`}
                                    >
                                        <span
                                            className={`absolute top-1 w-4 h-4 rounded-full bg-background transition-transform ${model.isEnabled ? 'left-5' : 'left-1'
                                                }`}
                                        />
                                    </button>

                                    {/* 模型信息 */}
                                    <div>
                                        <div className="flex items-center gap-2">
                                            {getVendorIcon(model.vendor, 16)}
                                            <span className="font-medium">{model.displayName}</span>
                                            <span className="text-xs text-foreground-secondary">
                                                {getVendorName(model.vendor)}
                                            </span>
                                            <span className="text-xs px-2 py-0.5 rounded-full bg-background-secondary text-foreground-secondary">
                                                {USAGE_TYPE_LABELS[model.usageType] || model.usageType}
                                            </span>
                                            <span className={`text-xs px-2 py-0.5 rounded-full ${tierInfo.color}`}>
                                                {tierInfo.label}
                                            </span>
                                            {model.supportsReasoning && (
                                                <span title="支持推理">
                                                    <Zap className="w-3.5 h-3.5 text-amber-500" />
                                                </span>
                                            )}
                                            {model.supportsVision && (
                                                <span title="支持视觉">
                                                    <Eye className="w-3.5 h-3.5 text-blue-500" />
                                                </span>
                                            )}
                                        </div>
                                        <p className="text-xs text-foreground-secondary mt-0.5">
                                            {activeSource?.sourceName || '无活跃来源'}
                                            {activeSource && !activeSource.hasApiKey && (
                                                <span className="text-red-500 ml-2">API Key 未配置</span>
                                            )}
                                            <span className="ml-2">· {ROUTING_MODE_LABELS[model.routingMode]}</span>
                                        </p>
                                    </div>
                                </div>

                                <div className="flex items-center gap-2">
                                    {isUpdating && <SoundWaveLoader variant="inline" />}
                                    {isExpanded ? (
                                        <ChevronUp className="w-5 h-5 text-foreground-secondary" />
                                    ) : (
                                        <ChevronDown className="w-5 h-5 text-foreground-secondary" />
                                    )}
                                </div>
                            </div>

                            {/* 展开内容 */}
                            {isExpanded && (
                                <div className="border-t border-border p-4 bg-background-secondary/30">
                                    <div className="rounded-xl border border-border bg-background/70 p-4 space-y-4 mb-4">
                                        <div className="flex items-center justify-between gap-3">
                                            <div>
                                                <p className="text-sm font-medium">基础信息</p>
                                                <p className="text-[11px] text-foreground-secondary mt-1">
                                                    模型 ID、显示名称和供应商会直接影响管理员配置和运行时解析。
                                                </p>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <button
                                                    type="button"
                                                    onClick={() => saveModelSettings(model.id)}
                                                    disabled={isUpdating}
                                                    className="px-3 py-1.5 rounded-lg text-sm bg-background-secondary hover:bg-background-secondary/80"
                                                >
                                                    保存模型设置
                                                </button>
                                                <button
                                                    type="button"
                                                    onClick={() => setDeleteModelTarget({
                                                        modelId: model.id,
                                                        displayName: model.displayName,
                                                    })}
                                                    disabled={isUpdating}
                                                    className="px-3 py-1.5 rounded-lg text-sm border border-red-500/30 text-red-500 hover:bg-red-500/10"
                                                >
                                                    删除模型
                                                </button>
                                            </div>
                                        </div>
                                        <div className="grid grid-cols-2 gap-4">
                                            <div>
                                                <label className="block text-xs text-foreground-secondary mb-1">模型 ID</label>
                                                <input
                                                    type="text"
                                                    value={modelDraft.modelKey}
                                                    onChange={(e) => updateModelDraft(model.id, { modelKey: e.target.value })}
                                                    disabled={isUpdating}
                                                    className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                />
                                            </div>
                                            <div>
                                                <label className="block text-xs text-foreground-secondary mb-1">显示名称</label>
                                                <input
                                                    type="text"
                                                    value={modelDraft.displayName}
                                                    onChange={(e) => updateModelDraft(model.id, { displayName: e.target.value })}
                                                    disabled={isUpdating}
                                                    className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                />
                                            </div>
                                            <div>
                                                <label className="block text-xs text-foreground-secondary mb-1">模型类型</label>
                                                <select
                                                    value={modelDraft.usageType}
                                                    onChange={(e) => updateModelDraft(model.id, {
                                                        usageType: e.target.value as AIModel['usageType'],
                                                    })}
                                                    disabled={isUpdating}
                                                    className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                >
                                                    <option value="chat">聊天</option>
                                                    <option value="vision">视觉</option>
                                                    <option value="embedding">Embedding</option>
                                                    <option value="rerank">Rerank</option>
                                                </select>
                                            </div>
                                            <div>
                                                <label className="block text-xs text-foreground-secondary mb-1">供应商</label>
                                                <select
                                                    value={modelDraft.vendorPreset}
                                                    onChange={(e) => updateModelDraft(model.id, {
                                                        vendorPreset: e.target.value as CreateVendorPreset,
                                                    })}
                                                    disabled={isUpdating}
                                                    className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                >
                                                    {VENDOR_PRESETS.map((vendor) => (
                                                        <option key={vendor.value} value={vendor.value}>
                                                            {vendor.label}
                                                        </option>
                                                    ))}
                                                    <option value="__custom__">自定义供应商</option>
                                                </select>
                                                {modelDraft.vendorPreset === '__custom__' && (
                                                    <input
                                                        type="text"
                                                        value={modelDraft.customVendor}
                                                        onChange={(e) => updateModelDraft(model.id, { customVendor: e.target.value })}
                                                        disabled={isUpdating}
                                                        placeholder="添加供应商，如 ChatGPT"
                                                        className="mt-2 w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                    />
                                                )}
                                            </div>
                                            <div className="col-span-2">
                                                <label className="block text-xs text-foreground-secondary mb-1">描述</label>
                                                <input
                                                    type="text"
                                                    value={modelDraft.description}
                                                    onChange={(e) => updateModelDraft(model.id, { description: e.target.value })}
                                                    disabled={isUpdating}
                                                    placeholder="可选"
                                                    className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                />
                                            </div>
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-2 gap-4 mb-4">
                                        <div>
                                            <label className="block text-xs text-foreground-secondary mb-1">
                                                所需会员等级
                                            </label>
                                            <select
                                                value={modelDraft.requiredTier}
                                                onChange={(e) => updateModelDraft(model.id, {
                                                    requiredTier: e.target.value as AIModel['requiredTier'],
                                                })}
                                                disabled={isUpdating}
                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                            >
                                                <option value="free">Free</option>
                                                <option value="plus">Plus</option>
                                                <option value="pro">Pro</option>
                                            </select>
                                        </div>

                                        <div>
                                            <label className="block text-xs text-foreground-secondary mb-1">
                                                路由模式
                                            </label>
                                            <select
                                                value={modelDraft.routingMode}
                                                onChange={(e) => updateModelDraft(model.id, {
                                                    routingMode: e.target.value as AIModel['routingMode'],
                                                })}
                                                disabled={isUpdating}
                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                            >
                                                <option value="auto">自动故障转移</option>
                                                <option value="newapi">固定 NewAPI</option>
                                                <option value="octopus">固定 Octopus</option>
                                            </select>
                                        </div>

                                        <div>
                                            <label className="block text-xs text-foreground-secondary mb-1">
                                                排序优先级
                                            </label>
                                            <input
                                                type="number"
                                                min="0"
                                                step="1"
                                                value={modelDraft.sortOrder}
                                                onChange={(e) => updateModelDraft(model.id, {
                                                    sortOrder: parseInt(e.target.value || '0', 10),
                                                })}
                                                disabled={isUpdating}
                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                            />
                                            <p className="text-[11px] text-foreground-secondary mt-1">
                                                数值越小，越优先作为该类型模型的线上默认项
                                            </p>
                                        </div>

                                        <div>
                                            <label className="block text-xs text-foreground-secondary mb-1">
                                                推理等级
                                            </label>
                                            <select
                                                value={modelDraft.reasoningRequiredTier}
                                                onChange={(e) => updateModelDraft(model.id, {
                                                    reasoningRequiredTier: e.target.value,
                                                })}
                                                disabled={isUpdating || !modelDraft.supportsReasoning}
                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                            >
                                                <option value="free">Free</option>
                                                <option value="plus">Plus</option>
                                                <option value="pro">Pro</option>
                                            </select>
                                            <p className="text-[11px] text-foreground-secondary mt-1">
                                                启用“支持推理”后生效。
                                            </p>
                                        </div>

                                        <div className="col-span-2">
                                            <div className="flex flex-wrap gap-4 text-sm">
                                                <label className="flex items-center gap-2">
                                                    <input
                                                        type="checkbox"
                                                        checked={modelDraft.supportsReasoning}
                                                        onChange={(e) => updateModelDraft(model.id, {
                                                            supportsReasoning: e.target.checked,
                                                            isReasoningDefault: e.target.checked ? modelDraft.isReasoningDefault : false,
                                                            defaultReasoningEffort: e.target.checked ? modelDraft.defaultReasoningEffort : null,
                                                            reasoningEffortFormat: e.target.checked ? (modelDraft.reasoningEffortFormat || 'reasoning_object') : null,
                                                        })}
                                                        disabled={isUpdating}
                                                    />
                                                    支持推理
                                                </label>
                                                <label className="flex items-center gap-2">
                                                    <input
                                                        type="checkbox"
                                                        checked={modelDraft.isReasoningDefault}
                                                        disabled={!modelDraft.supportsReasoning || isUpdating}
                                                        onChange={(e) => updateModelDraft(model.id, { isReasoningDefault: e.target.checked })}
                                                    />
                                                    默认开启推理
                                                </label>
                                                <label className="flex items-center gap-2">
                                                    <input
                                                        type="checkbox"
                                                        checked={modelDraft.supportsVision}
                                                        onChange={(e) => updateModelDraft(model.id, { supportsVision: e.target.checked })}
                                                        disabled={isUpdating}
                                                    />
                                                    支持视觉
                                                </label>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="rounded-xl border border-border bg-background/70 p-4 space-y-4">
                                        <div className="flex items-center gap-2 text-sm font-medium">
                                            <Layers className="w-4 h-4" />
                                            高级设置
                                        </div>
                                        <div className="grid grid-cols-2 gap-4">
                                            <div>
                                                <label className="block text-xs text-foreground-secondary mb-1">
                                                    默认温度
                                                </label>
                                                <input
                                                    type="number"
                                                    min="0"
                                                    max="2"
                                                    step="0.1"
                                                    value={modelDraft.defaultTemperature}
                                                    onChange={(e) => updateModelDraft(model.id, {
                                                        defaultTemperature: parseFloat(e.target.value || '0.7'),
                                                    })}
                                                    disabled={isUpdating}
                                                    className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                />
                                            </div>
                                            <div>
                                                <label className="block text-xs text-foreground-secondary mb-1">
                                                    Top P
                                                </label>
                                                <label className="flex items-center gap-2 text-sm mb-2">
                                                    <input
                                                        type="checkbox"
                                                        checked={modelDraft.defaultTopP !== null}
                                                        onChange={(e) => updateModelDraft(model.id, {
                                                            defaultTopP: e.target.checked ? 1 : null,
                                                        })}
                                                        disabled={isUpdating}
                                                    />
                                                    启用 Top P
                                                </label>
                                                {modelDraft.defaultTopP !== null && (
                                                    <input
                                                        type="number"
                                                        min="0"
                                                        max="1"
                                                        step="0.1"
                                                        value={modelDraft.defaultTopP}
                                                        onChange={(e) => updateModelDraft(model.id, {
                                                            defaultTopP: parseFloat(e.target.value || '1'),
                                                        })}
                                                        disabled={isUpdating}
                                                        className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                    />
                                                )}
                                            </div>
                                            <div>
                                                <label className="block text-xs text-foreground-secondary mb-1">
                                                    Presence Penalty
                                                </label>
                                                <label className="flex items-center gap-2 text-sm mb-2">
                                                    <input
                                                        type="checkbox"
                                                        checked={modelDraft.defaultPresencePenalty !== null}
                                                        onChange={(e) => updateModelDraft(model.id, {
                                                            defaultPresencePenalty: e.target.checked ? 0 : null,
                                                        })}
                                                        disabled={isUpdating}
                                                    />
                                                    启用 Presence Penalty
                                                </label>
                                                {modelDraft.defaultPresencePenalty !== null && (
                                                    <input
                                                        type="number"
                                                        min="-2"
                                                        max="2"
                                                        step="0.1"
                                                        value={modelDraft.defaultPresencePenalty}
                                                        onChange={(e) => updateModelDraft(model.id, {
                                                            defaultPresencePenalty: parseFloat(e.target.value || '0'),
                                                        })}
                                                        disabled={isUpdating}
                                                        className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                    />
                                                )}
                                            </div>
                                            <div>
                                                <label className="block text-xs text-foreground-secondary mb-1">
                                                    Frequency Penalty
                                                </label>
                                                <label className="flex items-center gap-2 text-sm mb-2">
                                                    <input
                                                        type="checkbox"
                                                        checked={modelDraft.defaultFrequencyPenalty !== null}
                                                        onChange={(e) => updateModelDraft(model.id, {
                                                            defaultFrequencyPenalty: e.target.checked ? 0 : null,
                                                        })}
                                                        disabled={isUpdating}
                                                    />
                                                    启用 Frequency Penalty
                                                </label>
                                                {modelDraft.defaultFrequencyPenalty !== null && (
                                                    <input
                                                        type="number"
                                                        min="-2"
                                                        max="2"
                                                        step="0.1"
                                                        value={modelDraft.defaultFrequencyPenalty}
                                                        onChange={(e) => updateModelDraft(model.id, {
                                                            defaultFrequencyPenalty: parseFloat(e.target.value || '0'),
                                                        })}
                                                        disabled={isUpdating}
                                                        className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                    />
                                                )}
                                            </div>
                                            <div className="col-span-2">
                                                <label className="flex items-center gap-2 text-sm mb-2">
                                                    <input
                                                        type="checkbox"
                                                        checked={modelDraft.defaultMaxTokens !== null}
                                                        onChange={(e) => updateModelDraft(model.id, {
                                                            defaultMaxTokens: e.target.checked ? 4000 : null,
                                                        })}
                                                        disabled={isUpdating}
                                                    />
                                                    启用最大输出限制
                                                </label>
                                                {modelDraft.defaultMaxTokens !== null && (
                                                    <input
                                                        type="number"
                                                        min="1"
                                                        step="1"
                                                        value={modelDraft.defaultMaxTokens}
                                                        onChange={(e) => updateModelDraft(model.id, {
                                                            defaultMaxTokens: parseInt(e.target.value || '4000', 10),
                                                        })}
                                                        disabled={isUpdating}
                                                        className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                    />
                                                )}
                                            </div>
                                            {modelDraft.supportsReasoning && (
                                                <>
                                                    <div>
                                                        <label className="block text-xs text-foreground-secondary mb-1">
                                                            默认思考等级
                                                        </label>
                                                        <select
                                                            value={modelDraft.defaultReasoningEffort || ''}
                                                            onChange={(e) => updateModelDraft(model.id, {
                                                                defaultReasoningEffort: (e.target.value || null) as AIModel['defaultReasoningEffort'],
                                                            })}
                                                            disabled={isUpdating}
                                                            className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                        >
                                                            <option value="">不设置</option>
                                                            <option value="minimal">Minimal</option>
                                                            <option value="low">Low</option>
                                                            <option value="medium">Medium</option>
                                                            <option value="high">High</option>
                                                        </select>
                                                    </div>
                                                    <div>
                                                        <label className="block text-xs text-foreground-secondary mb-1">
                                                            思考等级参数格式
                                                        </label>
                                                        <select
                                                            value={modelDraft.reasoningEffortFormat || 'reasoning_object'}
                                                            onChange={(e) => updateModelDraft(model.id, {
                                                                reasoningEffortFormat: e.target.value as AIModel['reasoningEffortFormat'],
                                                            })}
                                                            disabled={isUpdating}
                                                            className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                        >
                                                            <option value="reasoning_object">reasoning.effort</option>
                                                            <option value="reasoning_effort">reasoning_effort</option>
                                                        </select>
                                                    </div>
                                                </>
                                            )}
                                            <div className="col-span-2">
                                                <label className="block text-xs text-foreground-secondary mb-1">
                                                    自定义参数
                                                </label>
                                                <textarea
                                                    rows={6}
                                                    value={modelDraft.customParametersText}
                                                    onChange={(e) => updateModelDraft(model.id, {
                                                        customParametersText: e.target.value,
                                                    })}
                                                    className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm font-mono"
                                                />
                                                <p className="text-[11px] text-foreground-secondary mt-2">
                                                    模型专属参数建议放这里，例如 `presence_penalty`、`frequency_penalty`、供应商私有字段。这里会覆盖基础参数，并在“保存模型设置”时统一生效。
                                                </p>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="mt-4 rounded-xl border border-border bg-background/70 p-4">
                                        <div className="flex items-center justify-between gap-3 mb-3">
                                            <div>
                                                <p className="text-sm font-medium">来源与故障转移</p>
                                                <p className="text-[11px] text-foreground-secondary mt-1">
                                                    主来源失败时，自动切到下一个已启用且网关可用的来源。固定路由模式只会请求对应网关。
                                                </p>
                                            </div>
                                            {availableGatewayOptions.length > 0 ? (
                                                <button
                                                    type="button"
                                                    onClick={() => {
                                                        setAddingToModel(model.id);
                                                        setNewSource((current) => ({
                                                            ...current,
                                                            sourceKey: availableGatewayOptions[0],
                                                        }));
                                                    }}
                                                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm border border-dashed border-border hover:border-accent hover:text-accent transition-colors"
                                                >
                                                    <Plus className="w-3.5 h-3.5" />
                                                    {model.sources.length > 0 ? '添加备用来源' : '添加来源'}
                                                </button>
                                            ) : (
                                                <span className="text-[11px] text-foreground-secondary">
                                                    已绑定全部可用网关
                                                </span>
                                            )}
                                        </div>

                                        <div className="space-y-3">
                                            {model.sources.length === 0 && (
                                                <div className="text-sm text-foreground-secondary px-3 py-4 border border-dashed border-border rounded-lg">
                                                    当前模型还没有任何来源绑定，请至少绑定一个网关，否则运行时会直接失败。
                                                </div>
                                            )}

                                            {model.sources.map((source) => {
                                                const isEditing = editingSourceId === source.id && editingDraft;
                                                const sourceModelId = getSourceModelIdState(model.modelKey, source.modelIdOverride);
                                                return (
                                                    <div
                                                        key={source.id}
                                                        className={`rounded-lg border p-3 ${source.isActive
                                                            ? 'border-accent bg-accent/5'
                                                            : 'border-border bg-background'
                                                            }`}
                                                    >
                                                        <div className="flex items-start justify-between gap-3">
                                                            <div className="flex-1">
                                                                <div className="flex items-center gap-2 flex-wrap">
                                                                    <span className="font-medium text-sm">{source.sourceName}</span>
                                                                    {source.isActive && (
                                                                        <span className="text-xs bg-accent text-white px-2 py-0.5 rounded-full">
                                                                            首选
                                                                        </span>
                                                                    )}
                                                                    {!source.isEnabled && (
                                                                        <span className="text-xs bg-gray-500/10 text-gray-500 px-2 py-0.5 rounded-full">
                                                                            已禁用
                                                                        </span>
                                                                    )}
                                                                    {!source.hasApiKey && (
                                                                        <span className="text-xs bg-red-500/10 text-red-500 px-2 py-0.5 rounded-full">
                                                                            未配置 Key
                                                                        </span>
                                                                    )}
                                                                </div>
                                                                <div className="mt-1 space-y-1 text-xs text-foreground-secondary">
                                                                    <p>{source.apiKeyEnvVar || '未配置 Key 环境变量'} → {source.apiUrl || '未配置 Base URL'}</p>
                                                                    <p>
                                                                        {sourceModelId.inherited ? '模型 ID' : '上游模型 ID'}: {sourceModelId.value}
                                                                        {sourceModelId.inherited && '（跟随模型）'}
                                                                    </p>
                                                                    {source.reasoningModelId && <p>推理模型 ID: {source.reasoningModelId}</p>}
                                                                    <p>优先级: {source.priority}</p>
                                                                    {source.notes && <p>备注: {source.notes}</p>}
                                                                </div>

                                                                {isEditing && editingDraft && (
                                                                    <div className="grid grid-cols-2 gap-3 mt-3">
                                                                        <div>
                                                                            <label className="block text-xs text-foreground-secondary mb-1">上游模型 ID（可选）</label>
                                                                            <input
                                                                                type="text"
                                                                                value={editingDraft.modelIdOverride}
                                                                                onChange={(e) => setEditingDraft({ ...editingDraft, modelIdOverride: e.target.value })}
                                                                                placeholder={`留空则跟随模型 ID（${model.modelKey}）`}
                                                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                                            />
                                                                        </div>
                                                                        <div>
                                                                            <label className="block text-xs text-foreground-secondary mb-1">推理模型 ID</label>
                                                                            <input
                                                                                type="text"
                                                                                value={editingDraft.reasoningModelId}
                                                                                onChange={(e) => setEditingDraft({ ...editingDraft, reasoningModelId: e.target.value })}
                                                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                                            />
                                                                        </div>
                                                                        <div>
                                                                            <label className="block text-xs text-foreground-secondary mb-1">优先级</label>
                                                                            <input
                                                                                type="number"
                                                                                min="0"
                                                                                step="1"
                                                                                value={editingDraft.priority}
                                                                                onChange={(e) => setEditingDraft({ ...editingDraft, priority: parseInt(e.target.value || '0', 10) })}
                                                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                                            />
                                                                        </div>
                                                                        <div className="flex items-end">
                                                                            <label className="flex items-center gap-2 text-sm">
                                                                                <input
                                                                                    type="checkbox"
                                                                                    checked={editingDraft.isEnabled}
                                                                                    onChange={(e) => setEditingDraft({ ...editingDraft, isEnabled: e.target.checked })}
                                                                                />
                                                                                启用绑定
                                                                            </label>
                                                                        </div>
                                                                        <div className="col-span-2">
                                                                            <label className="block text-xs text-foreground-secondary mb-1">备注</label>
                                                                            <input
                                                                                type="text"
                                                                                value={editingDraft.notes}
                                                                                onChange={(e) => setEditingDraft({ ...editingDraft, notes: e.target.value })}
                                                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                                            />
                                                                        </div>
                                                                    </div>
                                                                )}
                                                            </div>

                                                            <div className="flex items-center gap-2">
                                                                {!isEditing && (
                                                                    <button
                                                                        type="button"
                                                                        onClick={() => beginEditSource(source, model.modelKey)}
                                                                        disabled={isUpdating}
                                                                        className="p-1.5 rounded-lg hover:bg-background-secondary transition-colors"
                                                                        title="编辑来源"
                                                                    >
                                                                        <Pencil className="w-4 h-4 text-foreground-secondary" />
                                                                    </button>
                                                                )}
                                                                {isEditing && editingDraft && (
                                                                    <>
                                                                        <button
                                                                            type="button"
                                                                            onClick={() => saveSource(model.id, source.id, model.modelKey)}
                                                                            disabled={isUpdating}
                                                                            className="p-1.5 rounded-lg hover:bg-background-secondary transition-colors"
                                                                            title="保存修改"
                                                                        >
                                                                            <Save className="w-4 h-4 text-green-500" />
                                                                        </button>
                                                                        <button
                                                                            type="button"
                                                                            onClick={() => {
                                                                                setEditingSourceId(null);
                                                                                setEditingDraft(null);
                                                                            }}
                                                                            disabled={isUpdating}
                                                                            className="p-1.5 rounded-lg hover:bg-background-secondary transition-colors"
                                                                            title="取消编辑"
                                                                        >
                                                                            <ChevronUp className="w-4 h-4 text-foreground-secondary" />
                                                                        </button>
                                                                    </>
                                                                )}
                                                                {!source.isActive && (
                                                                    <button
                                                                        type="button"
                                                                        onClick={() => activateSource(model.id, source.id)}
                                                                        disabled={isUpdating || !!isEditing || model.routingMode !== 'auto'}
                                                                        className="p-1.5 rounded-lg hover:bg-background-secondary transition-colors disabled:opacity-40"
                                                                        title={model.routingMode === 'auto' ? '设为首选' : '固定路由模式下不可切换首选'}
                                                                    >
                                                                        <Check className="w-4 h-4 text-green-500" />
                                                                    </button>
                                                                )}
                                                                <button
                                                                    type="button"
                                                                    onClick={() => setDeleteTarget({ modelId: model.id, sourceId: source.id })}
                                                                    disabled={isUpdating || !!isEditing}
                                                                    className="p-1.5 rounded-lg hover:bg-background-secondary transition-colors"
                                                                    title="删除来源"
                                                                >
                                                                    <Trash2 className="w-4 h-4 text-red-500" />
                                                                </button>
                                                            </div>
                                                        </div>
                                                    </div>
                                                );
                                            })}

                                            {isAddingHere && (
                                                <div className="rounded-lg border border-border bg-background p-4">
                                                    <h4 className="font-medium text-sm mb-3">添加来源</h4>
                                                    <div className="grid grid-cols-2 gap-3">
                                                        <div>
                                                            <label className="block text-xs text-foreground-secondary mb-1">绑定网关</label>
                                                            <select
                                                                value={newSource.sourceKey}
                                                                onChange={(e) => setNewSource({
                                                                    ...newSource,
                                                                    sourceKey: e.target.value as ManagedGatewayKey,
                                                                })}
                                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                            >
                                                                {availableGatewayOptions.map((gatewayKey) => (
                                                                    <option key={gatewayKey} value={gatewayKey}>
                                                                        {gatewayKey === 'newapi' ? 'NewAPI' : 'Octopus'}
                                                                    </option>
                                                                ))}
                                                            </select>
                                                        </div>
                                                        <div>
                                                            <label className="block text-xs text-foreground-secondary mb-1">上游模型 ID（可选）</label>
                                                            <input
                                                                type="text"
                                                                value={newSource.modelIdOverride}
                                                                onChange={(e) => setNewSource({ ...newSource, modelIdOverride: e.target.value })}
                                                                placeholder={`留空则跟随模型 ID（${model.modelKey}）`}
                                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                            />
                                                        </div>
                                                        <div>
                                                            <label className="block text-xs text-foreground-secondary mb-1">推理模型 ID</label>
                                                            <input
                                                                type="text"
                                                                value={newSource.reasoningModelId}
                                                                onChange={(e) => setNewSource({ ...newSource, reasoningModelId: e.target.value })}
                                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                            />
                                                        </div>
                                                        <div>
                                                            <label className="block text-xs text-foreground-secondary mb-1">优先级</label>
                                                            <input
                                                                type="number"
                                                                min="0"
                                                                step="1"
                                                                value={newSource.priority}
                                                                onChange={(e) => setNewSource({ ...newSource, priority: parseInt(e.target.value || '0', 10) })}
                                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                            />
                                                        </div>
                                                        <div className="col-span-2">
                                                            <label className="flex items-center gap-2 text-sm">
                                                                <input
                                                                    type="checkbox"
                                                                    checked={newSource.isEnabled}
                                                                    onChange={(e) => setNewSource({ ...newSource, isEnabled: e.target.checked })}
                                                                />
                                                                启用绑定
                                                            </label>
                                                        </div>
                                                        <div className="col-span-2">
                                                            <label className="block text-xs text-foreground-secondary mb-1">备注</label>
                                                            <input
                                                                type="text"
                                                                value={newSource.notes}
                                                                onChange={(e) => setNewSource({ ...newSource, notes: e.target.value })}
                                                                className="w-full px-3 py-2 rounded-lg border border-border bg-background text-sm"
                                                            />
                                                        </div>
                                                    </div>
                                                    <div className="flex justify-end gap-2 mt-4">
                                                        <button
                                                            type="button"
                                                            onClick={() => {
                                                                setAddingToModel(null);
                                                                resetNewSource();
                                                            }}
                                                            className="px-3 py-1.5 rounded-lg text-sm border border-border hover:bg-background-secondary"
                                                        >
                                                            取消
                                                        </button>
                                                        <button
                                                            type="button"
                                                            onClick={() => addSource(model.id, model.modelKey)}
                                                            disabled={isUpdating}
                                                            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm bg-accent text-white hover:bg-accent/90 disabled:opacity-50"
                                                        >
                                                            {isUpdating ? <SoundWaveLoader variant="inline" /> : <Save className="w-3.5 h-3.5" />}
                                                            保存
                                                        </button>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </div>

                                    {/* 描述 */}
                                    {model.description && (
                                        <p className="mt-4 text-xs text-foreground-secondary">
                                            {model.description}
                                        </p>
                                    )}
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>

            <ConfirmDialog
                isOpen={!!deleteTarget}
                onClose={() => setDeleteTarget(null)}
                onConfirm={() => deleteTarget ? deleteSource(deleteTarget.modelId, deleteTarget.sourceId) : undefined}
                title="确认删除"
                description="确定要删除这个来源绑定吗？删除后该模型将不再使用对应网关。"
                confirmText="确认删除"
                variant="danger"
                loading={!!deleteTarget && updating === deleteTarget.modelId}
            />

            <ConfirmDialog
                isOpen={!!deleteModelTarget}
                onClose={() => setDeleteModelTarget(null)}
                onConfirm={() => deleteModelTarget ? deleteModel(deleteModelTarget.modelId) : undefined}
                title="确认删除模型"
                description={`确定要删除 ${deleteModelTarget?.displayName || '该模型'} 吗？对应来源绑定也会一起删除。`}
                confirmText="确认删除"
                variant="danger"
                loading={!!deleteModelTarget && updating === deleteModelTarget.modelId}
            />
        </div>
    );
}
