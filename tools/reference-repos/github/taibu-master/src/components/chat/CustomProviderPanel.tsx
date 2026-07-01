'use client';

import { useEffect, useMemo, useState } from 'react';
import { ChevronDown, Eye, EyeOff, PencilLine } from 'lucide-react';
import { useToast } from '@/components/ui/Toast';
import type { CustomProviderConfig } from '@/types';
import {
    buildByokProviderOptions,
    getByokProviderLabel,
    isOtherByokProviderKey,
    normalizeByokProviderKey,
    type ByokProviderOption,
} from '@/lib/ai/byok-catalog';
import {
    clearCustomProvider,
    CUSTOM_PROVIDER_CHANGED_EVENT,
    getCustomProvider,
    getLastCustomProvider,
    setCustomProvider,
} from '@/lib/chat/custom-provider';
import { useByokModelCatalog } from '@/lib/hooks/useByokModelCatalog';
import { validateCustomProviderInput } from '@/lib/ai/custom-provider-url';

type CustomProviderDraft = {
    providerKey: string;
    apiUrl: string;
    apiKey: string;
    modelId: string;
    modelName: string;
};

type CustomProviderFormErrors = {
    providerKey?: string;
    apiUrl?: string;
    apiKey?: string;
    modelId?: string;
};

interface CustomProviderPanelProps {
    embedded?: boolean;
    onClose?: () => void;
    onChange?: (config: CustomProviderConfig | null) => void;
    title?: string;
    description?: string | null;
    showByokBadge?: boolean;
}

const EMPTY_DRAFT: CustomProviderDraft = {
    providerKey: '',
    apiUrl: '',
    apiKey: '',
    modelId: '',
    modelName: '',
};

function draftFromConfig(config: CustomProviderConfig | null): CustomProviderDraft {
    if (!config) return EMPTY_DRAFT;
    return {
        providerKey: normalizeByokProviderKey(config.providerKey) || 'other',
        apiUrl: config.apiUrl,
        apiKey: config.apiKey,
        modelId: config.modelId,
        modelName: config.modelName ?? '',
    };
}

function InputError({ message }: { message?: string }) {
    if (!message) return null;
    return <p className="text-xs text-red-500">{message}</p>;
}

function formatProviderUrl(apiUrl?: string | null) {
    if (!apiUrl) return '未设置';
    try {
        return new URL(apiUrl).toString();
    } catch {
        return apiUrl;
    }
}

function maskSecret(value?: string | null) {
    if (!value) return '********';
    return '*'.repeat(Math.max(8, Math.min(value.length, 14)));
}

function SummaryField({ label, value }: { label: string; value: string }) {
    return (
        <div className="min-w-0 rounded-xl border border-[#e7e2d9] bg-white/85 px-3 py-2">
            <p className="text-[10px] font-semibold uppercase tracking-[0.12em] text-[#37352f]/35">{label}</p>
            <p className="mt-1 break-all text-[12px] leading-5 text-[#37352f]" title={value}>{value}</p>
        </div>
    );
}

function SelectField({
    label,
    value,
    options,
    placeholder,
    onChange,
    error,
    disabled = false,
}: {
    label: string;
    value: string;
    options: Array<{ value: string; label: string }>;
    placeholder: string;
    onChange: (value: string) => void;
    error?: string;
    disabled?: boolean;
}) {
    return (
        <div className="space-y-1">
            <label className="text-[11px] font-bold text-[#37352f]/40 uppercase tracking-wider">{label}</label>
            <div className="relative">
                <select
                    value={value}
                    onChange={(event) => onChange(event.target.value)}
                    disabled={disabled}
                    className="w-full appearance-none rounded-xl border border-[#e7e2d9] bg-white px-3 py-2 pr-10 text-[13px] outline-none transition-all duration-150 focus:border-[#cdbb8b] focus:bg-white disabled:cursor-not-allowed disabled:bg-[#f7f3eb] disabled:text-[#37352f]/35"
                >
                    <option value="">{placeholder}</option>
                    {options.map((option) => (
                        <option key={option.value} value={option.value}>
                            {option.label}
                        </option>
                    ))}
                </select>
                <ChevronDown className="pointer-events-none absolute inset-y-0 right-3 my-auto h-4 w-4 text-[#37352f]/35" />
            </div>
            <InputError message={error} />
        </div>
    );
}

function resolveDraftConfig(
    draft: CustomProviderDraft,
    providers: ByokProviderOption[],
): CustomProviderConfig | null {
    const apiKey = draft.apiKey.trim();

    if (isOtherByokProviderKey(draft.providerKey)) {
        return {
            providerKey: 'other',
            providerLabel: '其他',
            apiUrl: draft.apiUrl.trim(),
            apiKey,
            modelId: draft.modelId.trim(),
            modelName: draft.modelName.trim() || undefined,
        };
    }

    const provider = providers.find((item) => item.key === draft.providerKey);
    if (!provider) {
        return null;
    }

    const selectedModel = provider.models.find((item) => item.id === draft.modelId.trim());
    return {
        providerKey: provider.key,
        providerLabel: provider.label,
        apiUrl: provider.defaultApiUrl ?? '',
        apiKey,
        modelId: draft.modelId.trim(),
        modelName: selectedModel?.name || draft.modelName.trim() || undefined,
    };
}

function buildFormErrors(
    draft: CustomProviderDraft,
    providers: ByokProviderOption[],
): CustomProviderFormErrors {
    const errors: CustomProviderFormErrors = {};

    if (isOtherByokProviderKey(draft.providerKey)) {
        return validateCustomProviderInput({
            apiUrl: draft.apiUrl,
            apiKey: draft.apiKey,
            modelId: draft.modelId,
        });
    }

    if (!draft.providerKey) {
        errors.providerKey = '请选择模型供应商';
        return errors;
    }

    const provider = providers.find((item) => item.key === draft.providerKey);
    if (!provider) {
        errors.providerKey = '请选择模型供应商';
        return errors;
    }

    const validation = validateCustomProviderInput({
        apiUrl: provider.defaultApiUrl ?? '',
        apiKey: draft.apiKey,
        modelId: draft.modelId,
    });

    if (!draft.modelId.trim()) {
        errors.modelId = '请选择模型';
    } else if (validation.modelId) {
        errors.modelId = validation.modelId;
    }

    if (!provider.defaultApiUrl || validation.apiUrl) {
        errors.providerKey = '当前供应商预设地址不可用';
    }

    if (validation.apiKey) {
        errors.apiKey = validation.apiKey;
    }

    return errors;
}

export function CustomProviderPanel({
    embedded = false,
    onClose,
    onChange,
    title = '自定义模型',
    description = 'Key不会保存到服务器，不消耗本站积分，关闭页面自动失效',
    showByokBadge = true,
}: CustomProviderPanelProps) {
    const { showToast } = useToast();
    const byokCatalog = useByokModelCatalog();
    const fallbackProviders = useMemo(() => buildByokProviderOptions([]), []);
    const providers = byokCatalog.providers;
    const safeProviders = providers.length > 0 ? providers : fallbackProviders;

    const [activeConfig, setActiveConfig] = useState<CustomProviderConfig | null>(() => getCustomProvider());
    const [draft, setDraft] = useState<CustomProviderDraft>(() => draftFromConfig(getCustomProvider()));
    const [lastConfig, setLastConfig] = useState<CustomProviderConfig | null>(() => getLastCustomProvider());
    const [isEditing, setIsEditing] = useState(() => !getCustomProvider());
    const [showApiKey, setShowApiKey] = useState(false);
    const [submitted, setSubmitted] = useState(false);

    useEffect(() => {
        if (typeof window === 'undefined') return;
        const sync = () => {
            const nextConfig = getCustomProvider();
            const nextLastConfig = getLastCustomProvider();
            setActiveConfig(nextConfig);
            setLastConfig(nextLastConfig);
            setDraft(draftFromConfig(nextConfig));
            setShowApiKey(false);
            setIsEditing((prev) => (nextConfig ? prev : true));
            setSubmitted(false);
        };
        sync();
        window.addEventListener(CUSTOM_PROVIDER_CHANGED_EVENT, sync);
        window.addEventListener('storage', sync);
        return () => {
            window.removeEventListener(CUSTOM_PROVIDER_CHANGED_EVENT, sync);
            window.removeEventListener('storage', sync);
        };
    }, []);

    const selectedProvider = useMemo(
        () => safeProviders.find((item) => item.key === draft.providerKey) ?? null,
        [safeProviders, draft.providerKey],
    );
    const isOtherProvider = isOtherByokProviderKey(draft.providerKey);
    const activeProviderLabel = getByokProviderLabel(activeConfig?.providerKey, activeConfig?.providerLabel);
    const activeUrl = formatProviderUrl(activeConfig?.apiUrl);
    const errors = useMemo(() => buildFormErrors(draft, safeProviders), [draft, safeProviders]);
    const hasErrors = Object.keys(errors).length > 0;

    const providerOptions = useMemo(
        () => safeProviders.map((item) => ({ value: item.key, label: item.label })),
        [safeProviders],
    );
    const modelOptions = useMemo(
        () => (selectedProvider?.models ?? []).map((item) => ({ value: item.id, label: item.name })),
        [selectedProvider],
    );

    const handleFieldChange = (field: keyof CustomProviderDraft, value: string) => {
        setDraft((prev) => ({ ...prev, [field]: value }));
    };

    const handleProviderChange = (providerKey: string) => {
        setSubmitted(false);
        if (!providerKey) {
            setDraft((prev) => ({
                ...prev,
                providerKey: '',
                apiUrl: '',
                modelId: '',
                modelName: '',
            }));
            return;
        }

        if (isOtherByokProviderKey(providerKey)) {
            setDraft((prev) => ({
                ...prev,
                providerKey,
                apiUrl: prev.providerKey === providerKey ? prev.apiUrl : '',
                modelId: '',
                modelName: '',
            }));
            return;
        }

        const provider = safeProviders.find((item) => item.key === providerKey);
        const firstModel = provider?.models[0];
        setDraft((prev) => ({
            ...prev,
            providerKey,
            apiUrl: provider?.defaultApiUrl ?? '',
            modelId: firstModel?.id ?? '',
            modelName: firstModel?.name ?? '',
        }));
    };

    const handleModelChange = (modelId: string) => {
        const selectedModel = selectedProvider?.models.find((item) => item.id === modelId);
        setSubmitted(false);
        setDraft((prev) => ({
            ...prev,
            modelId,
            modelName: selectedModel?.name ?? '',
        }));
    };

    const handleManualModelIdChange = (modelId: string) => {
        const selectedModel = selectedProvider?.models.find((item) => item.id === modelId.trim());
        setSubmitted(false);
        setDraft((prev) => ({
            ...prev,
            modelId,
            modelName: selectedModel?.name ?? '',
        }));
    };

    const handleStartEdit = () => {
        setDraft(draftFromConfig(activeConfig));
        setShowApiKey(false);
        setSubmitted(false);
        setIsEditing(true);
    };

    const handleCancelEdit = () => {
        setDraft(draftFromConfig(activeConfig));
        setShowApiKey(false);
        setSubmitted(false);
        setIsEditing(false);
    };

    const handleActivate = () => {
        setSubmitted(true);
        if (hasErrors) return;

        const nextConfig = resolveDraftConfig(draft, safeProviders);
        if (!nextConfig) return;

        setCustomProvider(nextConfig);
        setActiveConfig(nextConfig);
        setLastConfig(nextConfig);
        setShowApiKey(false);
        setSubmitted(false);
        setIsEditing(false);
        onChange?.(nextConfig);
        showToast('success', activeConfig ? '已更新自定义模型配置' : '已启用自定义模型');
        if (!embedded) {
            onClose?.();
        }
    };

    const handleDeactivate = () => {
        clearCustomProvider();
        setActiveConfig(null);
        setDraft(EMPTY_DRAFT);
        setShowApiKey(false);
        setSubmitted(false);
        setIsEditing(true);
        onChange?.(null);
        showToast('success', '已停用自定义模型');
        if (!embedded) {
            onClose?.();
        }
    };

    const handleReactivateLastConfig = () => {
        if (!lastConfig) return;

        setCustomProvider(lastConfig);
        setActiveConfig(lastConfig);
        setDraft(draftFromConfig(lastConfig));
        setShowApiKey(false);
        setSubmitted(false);
        setIsEditing(false);
        onChange?.(lastConfig);
        showToast('success', '已恢复上次启用的自定义模型');
        if (!embedded) {
            onClose?.();
        }
    };

    const modelSelectDisabled = !selectedProvider || isOtherProvider || modelOptions.length === 0;

    return (
        <div className={embedded
            ? 'rounded-xl border border-[#e7e2d9] bg-[#fcfbf8] px-4 py-4 shadow-[0_1px_2px_rgba(0,0,0,0.06)]'
            : 'rounded-xl border border-[#e7e2d9] bg-[#fcfbf8] p-4 shadow-[0_10px_30px_rgba(34,30,20,0.12)] md:w-[392px]'
        }>
            <div className="space-y-3.5">
                <div className="space-y-2">
                    <div className="flex items-start justify-between gap-3">
                        <div className="space-y-1">
                            <div className="flex flex-wrap items-center gap-2">
                                <h3 id={embedded ? undefined : 'custom-provider-panel-title'} className="text-[14px] font-semibold text-[#37352f]">
                                    {title}
                                </h3>
                                {showByokBadge ? (
                                    <span className="rounded-full border border-[#e8dcc0] bg-[#f4efe2] px-2 py-0.5 text-[10px] font-semibold tracking-[0.08em] text-[#8a6b00]">
                                        BYOK
                                    </span>
                                ) : null}
                            </div>
                            {description ? (
                                <p className="text-[12px] leading-tight text-[#37352f]/60">
                                    {description}
                                </p>
                            ) : null}
                        </div>
                    </div>
                </div>

                {activeConfig && !isEditing ? (
                    <div className="space-y-2.5">
                        <div className="rounded-xl border border-[#e7e2d9] bg-[#f7f3eb] p-3">
                            <div className="grid grid-cols-2 gap-2">
                                <SummaryField label="PROVIDER" value={activeProviderLabel} />
                                <SummaryField label="URL" value={activeUrl} />
                                <SummaryField label="MODEL" value={activeConfig.modelId} />
                                <div className="min-w-0 rounded-xl border border-[#e7e2d9] bg-white/85 px-3 py-2">
                                    <div className="flex items-center justify-between gap-2">
                                        <p className="text-[10px] font-semibold uppercase tracking-[0.12em] text-[#37352f]/35">KEY</p>
                                        <button
                                            type="button"
                                            onClick={() => setShowApiKey((prev) => !prev)}
                                            className="flex h-5 w-5 items-center justify-center rounded-md text-[#37352f]/35 transition-colors duration-150 hover:bg-[#f3f0ea] hover:text-[#37352f]"
                                            title={showApiKey ? '隐藏 API Key' : '查看 API Key'}
                                        >
                                            {showApiKey ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
                                        </button>
                                    </div>
                                    <p
                                        className="mt-1 break-all text-[12px] leading-5 text-[#37352f]"
                                        title={showApiKey ? activeConfig.apiKey : maskSecret(activeConfig.apiKey)}
                                    >
                                        {showApiKey ? activeConfig.apiKey : maskSecret(activeConfig.apiKey)}
                                    </p>
                                </div>
                                {activeConfig.modelName ? (
                                    <SummaryField label="NAME" value={activeConfig.modelName} />
                                ) : null}
                            </div>
                        </div>

                        <div className="flex gap-2">
                            <button
                                type="button"
                                onClick={handleStartEdit}
                                className="flex h-9 flex-1 items-center justify-center gap-1.5 rounded-xl bg-[#37352f] text-[12px] font-medium text-white transition-colors duration-150 hover:bg-[#2b2925]"
                            >
                                <PencilLine className="h-3.5 w-3.5" />
                                编辑
                            </button>
                            <button
                                type="button"
                                onClick={handleDeactivate}
                                className="flex h-9 items-center justify-center rounded-xl border border-[#e7e2d9] bg-white px-3 text-[12px] font-medium text-[#37352f]/65 transition-colors duration-150 hover:bg-[#f3f0ea] hover:text-[#37352f]"
                            >
                                停用
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="space-y-3">
                        <div className="grid gap-3 md:grid-cols-2">
                            <SelectField
                                label="模型供应商"
                                value={draft.providerKey}
                                options={providerOptions}
                                placeholder="选择供应商"
                                onChange={handleProviderChange}
                                error={submitted ? errors.providerKey : undefined}
                            />

                            {!isOtherProvider ? (
                                <SelectField
                                    label="预设模型"
                                    value={draft.modelId}
                                    options={modelOptions}
                                    placeholder={selectedProvider ? '选择模型' : '先选择供应商'}
                                    onChange={handleModelChange}
                                    disabled={modelSelectDisabled}
                                />
                            ) : null}

                            <div className={isOtherProvider ? '' : 'md:col-span-2'}>
                                <div className="space-y-1">
                                    <label className="text-[11px] font-bold text-[#37352f]/40 uppercase tracking-wider">API Key</label>
                                    <div className="relative">
                                        <input
                                            value={draft.apiKey}
                                            onChange={(event) => handleFieldChange('apiKey', event.target.value)}
                                            type={showApiKey ? 'text' : 'password'}
                                            className="w-full rounded-xl border border-[#e7e2d9] bg-white px-3 py-2 pr-10 text-[13px] outline-none transition-all duration-150 focus:border-[#cdbb8b] focus:bg-white"
                                            placeholder="sk-..."
                                            autoComplete="off"
                                        />
                                        <button
                                            type="button"
                                            onClick={() => setShowApiKey((prev) => !prev)}
                                            className="absolute inset-y-0 right-0 flex items-center px-3 text-[#37352f]/30 hover:text-[#37352f]"
                                        >
                                            {showApiKey ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
                                        </button>
                                    </div>
                                    <InputError message={submitted ? errors.apiKey : undefined} />
                                </div>
                            </div>

                            {isOtherProvider ? (
                                <>
                                    <div className="space-y-1">
                                        <label className="text-[11px] font-bold text-[#37352f]/40 uppercase tracking-wider">API URL</label>
                                        <input
                                            value={draft.apiUrl}
                                            onChange={(event) => handleFieldChange('apiUrl', event.target.value)}
                                            className="w-full rounded-xl border border-[#e7e2d9] bg-white px-3 py-2 text-[13px] outline-none transition-all duration-150 focus:border-[#cdbb8b] focus:bg-white"
                                            placeholder="https://api.example.com/v1"
                                            autoComplete="off"
                                        />
                                        <InputError message={submitted ? errors.apiUrl : undefined} />
                                    </div>

                                    <div className="space-y-1">
                                        <label className="text-[11px] font-bold text-[#37352f]/40 uppercase tracking-wider">Model ID</label>
                                        <input
                                            value={draft.modelId}
                                            onChange={(event) => handleFieldChange('modelId', event.target.value)}
                                            className="w-full rounded-xl border border-[#e7e2d9] bg-white px-3 py-2 text-[13px] outline-none transition-all duration-150 focus:border-[#cdbb8b] focus:bg-white"
                                            placeholder="gpt-4.1-mini"
                                            autoComplete="off"
                                        />
                                        <InputError message={submitted ? errors.modelId : undefined} />
                                    </div>

                                    <div className="space-y-1 md:col-span-2">
                                        <label className="text-[11px] font-bold text-[#37352f]/40 uppercase tracking-wider">显示名称</label>
                                        <input
                                            value={draft.modelName}
                                            onChange={(event) => handleFieldChange('modelName', event.target.value)}
                                            className="w-full rounded-xl border border-[#e7e2d9] bg-white px-3 py-2 text-[13px] outline-none transition-all duration-150 focus:border-[#cdbb8b] focus:bg-white"
                                            placeholder="显示名称 (可选)"
                                            autoComplete="off"
                                        />
                                    </div>
                                </>
                            ) : (
                                <div className="space-y-1 md:col-span-2">
                                    <label className="text-[11px] font-bold text-[#37352f]/40 uppercase tracking-wider">Model ID</label>
                                    <input
                                        value={draft.modelId}
                                        onChange={(event) => handleManualModelIdChange(event.target.value)}
                                        className="w-full rounded-xl border border-[#e7e2d9] bg-white px-3 py-2 text-[13px] outline-none transition-all duration-150 focus:border-[#cdbb8b] focus:bg-white"
                                        placeholder={selectedProvider?.models[0]?.id ?? '输入自定义 Model ID'}
                                        autoComplete="off"
                                    />
                                    <InputError message={submitted ? errors.modelId : undefined} />
                                </div>
                            )}
                        </div>

                        <div className="flex gap-2 pt-1">
                            <button
                                type="button"
                                onClick={handleActivate}
                                className="flex h-9 flex-1 items-center justify-center rounded-xl bg-[#37352f] text-[12px] font-semibold text-white transition-colors duration-150 hover:bg-[#2b2925]"
                            >
                                {activeConfig ? '保存并启用' : '启用服务'}
                            </button>
                            {activeConfig ? (
                                <button
                                    type="button"
                                    onClick={handleCancelEdit}
                                    className="flex h-9 items-center justify-center rounded-xl border border-[#e7e2d9] bg-white px-3 text-[12px] font-medium text-[#37352f]/55 transition-colors duration-150 hover:bg-[#f3f0ea] hover:text-[#37352f]"
                                >
                                    取消
                                </button>
                            ) : lastConfig ? (
                                <button
                                    type="button"
                                    onClick={handleReactivateLastConfig}
                                    className="flex h-9 flex-1 items-center justify-center rounded-xl border border-[#e7e2d9] bg-white px-3 text-[12px] font-medium text-[#37352f]/65 transition-colors duration-150 hover:bg-[#f3f0ea] hover:text-[#37352f]"
                                >
                                    上次启用
                                </button>
                            ) : null}
                        </div>
                    </div>
                )}

            </div>
        </div>
    );
}
