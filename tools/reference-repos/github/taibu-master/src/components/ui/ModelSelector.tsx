/**
 * AI 模型选择器组件
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useState, useEffect, useMemo)
 * - 有下拉选择交互功能
 */
'use client';

import { useMemo, useEffect, useState } from 'react';
import { ChevronDown, Cpu, Lightbulb } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { getVendorIcon } from '@/lib/ai/vendor-config';
import { DEFAULT_MODEL_ID } from '@/lib/ai/ai-config';
import { useAvailableModels } from '@/lib/hooks/useAvailableModels';
import {
    CUSTOM_PROVIDER_CHANGED_EVENT,
    getCustomProvider,
    getCustomProviderDisplayName,
} from '@/lib/chat/custom-provider';
import type { AIVendor } from '@/types';
import type { MembershipType } from '@/lib/user/membership';

interface ClientModelConfig {
    id: string;
    name: string;
    vendor: AIVendor;
    supportsReasoning: boolean;
    isReasoningDefault?: boolean;
    allowed?: boolean;
    blockedReason?: string | null;
    reasoningAllowed?: boolean;
}

interface ModelSelectorProps {
    selectedModel?: string;
    onModelChange?: (modelId: string) => void;
    reasoningEnabled?: boolean;
    onReasoningChange?: (enabled: boolean) => void;
    userId?: string | null;
    membershipType?: MembershipType;
    disabled?: boolean;
    compact?: boolean;
    toolbarStyle?: boolean;
}

export function ModelSelector({
    selectedModel = DEFAULT_MODEL_ID,
    onModelChange,
    reasoningEnabled = false,
    onReasoningChange,
    userId,
    membershipType = 'free',
    disabled = false,
    compact = false,
    toolbarStyle = false,
}: ModelSelectorProps) {
    const [modelDropdownOpen, setModelDropdownOpen] = useState(false);
    const modelsQuery = useAvailableModels(userId ?? null, {
        enabled: !!onModelChange,
        membershipType,
    });
    const [customProviderConfig, setCustomProviderConfig] = useState(() => getCustomProvider());
    const models = useMemo(() => (modelsQuery.data ?? []) as ClientModelConfig[], [modelsQuery.data]);
    const modelsLoading = modelsQuery.isLoading;
    const modelsError = modelsQuery.error instanceof Error ? modelsQuery.error.message : null;

    useEffect(() => {
        if (typeof window === 'undefined') return;
        const syncCustomProvider = () => {
            setCustomProviderConfig(getCustomProvider());
        };
        syncCustomProvider();
        window.addEventListener(CUSTOM_PROVIDER_CHANGED_EVENT, syncCustomProvider);
        window.addEventListener('storage', syncCustomProvider);
        return () => {
            window.removeEventListener(CUSTOM_PROVIDER_CHANGED_EVENT, syncCustomProvider);
            window.removeEventListener('storage', syncCustomProvider);
        };
    }, []);

    useEffect(() => {
        if (!models.length || !onModelChange) return;
        const selected = models.find(model => model.id === selectedModel);
        if (selected && selected.allowed !== false) return;
        const nextModel = models.find(model => model.allowed !== false) || models[0];
        if (nextModel && nextModel.id !== selectedModel) {
            onModelChange(nextModel.id);
        }
    }, [models, onModelChange, selectedModel]);

    const currentModelConfig = useMemo(() => {
        const config = models.find(m => m.id === selectedModel) || models[0];
        if (!config) {
            return {
                id: 'none',
                name: '未配置模型',
                vendor: 'deepseek' as const,
                supportsReasoning: false,
            };
        }
        return config;
    }, [selectedModel, models]);

    const modelSelectorDisabled = disabled || modelsLoading || models.length === 0;

    const reasoningAllowed = currentModelConfig?.reasoningAllowed ?? currentModelConfig?.supportsReasoning;
    const canToggleReasoning = reasoningAllowed && currentModelConfig?.supportsReasoning && !currentModelConfig?.isReasoningDefault;
    const isReasoningForced = reasoningAllowed && currentModelConfig?.isReasoningDefault;
    const reasoningTooltip = membershipType === 'free'
        ? '请升级会员使用'
        : !currentModelConfig?.supportsReasoning
            ? '当前模型不支持推理模式'
            : !reasoningAllowed
                ? (currentModelConfig?.blockedReason || '当前会员等级无法使用推理模式')
                : isReasoningForced
                    ? '此模型默认开启推理'
                    : reasoningEnabled
                        ? '关闭推理模式'
                        : '开启推理模式';

    useEffect(() => {
        if (!onReasoningChange) return;
        if (!currentModelConfig?.supportsReasoning || !reasoningAllowed) {
            if (reasoningEnabled) onReasoningChange(false);
            return;
        }
        if (currentModelConfig.isReasoningDefault && !reasoningEnabled) {
            onReasoningChange(true);
        }
    }, [currentModelConfig, onReasoningChange, reasoningAllowed, reasoningEnabled]);

    const handleReasoningToggle = () => {
        if (canToggleReasoning && onReasoningChange) {
            onReasoningChange(!reasoningEnabled);
        }
    };

    if (!onModelChange && !onReasoningChange) return null;

    const buttonPadding = compact ? 'px-2 py-1' : 'px-2 py-1.5';
    const textSize = compact ? 'text-xs' : 'text-sm';
    const selectorButtonClass = toolbarStyle
        ? `h-9 rounded-xl px-2 ${textSize}`
        : `${buttonPadding} rounded-lg ${textSize}`;
    const selectorActiveClass = toolbarStyle
        ? 'bg-transparent text-[#37352f]/70 hover:bg-[#f3f0ea] hover:text-[#37352f]'
        : 'hover:bg-background-tertiary text-foreground-secondary hover:text-foreground';
    const selectorDisabledClass = toolbarStyle
        ? 'bg-transparent text-[#37352f]/35 opacity-60 cursor-not-allowed'
        : 'opacity-50 cursor-not-allowed text-foreground-secondary';
    const reasoningBaseClass = toolbarStyle
        ? `h-9 w-10 rounded-xl ${textSize}`
        : `${buttonPadding} rounded-lg ${textSize}`;
    const reasoningIdleClass = toolbarStyle
        ? 'bg-transparent text-[#37352f]/72 hover:bg-[#f3f0ea] hover:text-[#37352f]'
        : 'hover:bg-background-tertiary text-foreground-secondary hover:text-foreground';
    const reasoningActiveClass = toolbarStyle
        ? 'bg-[#f4efe2] text-[#8a6b00]'
        : 'text-yellow-600';
    const reasoningDisabledClass = toolbarStyle
        ? 'bg-transparent text-[#37352f]/30 opacity-60 cursor-not-allowed'
        : 'opacity-30 cursor-not-allowed text-foreground-secondary';

    if (customProviderConfig && !toolbarStyle) {
        const directLabel = getCustomProviderDisplayName(customProviderConfig) || customProviderConfig.modelId;
        return (
            <div className="flex items-center">
                <div
                    className={`flex items-center gap-2 border border-border/70 bg-background-secondary/40 text-foreground-secondary ${selectorButtonClass}`}
                    title="当前已启用 BYOK 浏览器直连"
                >
                    <Cpu className={compact ? 'w-4 h-4' : 'w-4.5 h-4.5'} />
                    <span className={`${compact ? 'max-w-[132px]' : 'max-w-[180px]'} truncate`}>
                        {directLabel}
                    </span>
                </div>
            </div>
        );
    }

    return (
        <div className={`flex items-center ${toolbarStyle ? 'gap-1' : ''}`}>
            {onReasoningChange && toolbarStyle && (
                <button
                    type="button"
                    onClick={handleReasoningToggle}
                    disabled={disabled || !canToggleReasoning}
                    className={`flex items-center justify-center transition-all ${reasoningBaseClass} ${disabled || !currentModelConfig?.supportsReasoning || !reasoningAllowed
                        ? reasoningDisabledClass
                        : isReasoningForced
                            ? `${reasoningActiveClass} cursor-default`
                            : reasoningEnabled
                                ? reasoningActiveClass
                                : reasoningIdleClass
                        }`}
                    title={reasoningTooltip}
                >
                    <Lightbulb className={`${compact ? 'w-4 h-4' : 'w-4.5 h-4.5'} ${(reasoningEnabled || isReasoningForced) ? 'fill-yellow-500' : ''}`} />
                </button>
            )}

            {onModelChange && (
                <div className="relative">
                    <button
                        type="button"
                        onClick={() => setModelDropdownOpen(!modelDropdownOpen)}
                        className={`flex items-center gap-1.5 transition-all ${selectorButtonClass} ${
                            modelSelectorDisabled
                                ? selectorDisabledClass
                                : toolbarStyle && modelDropdownOpen
                                    ? 'bg-[#f3f0ea] text-[#37352f]'
                                    : selectorActiveClass
                        }`}
                        disabled={modelSelectorDisabled}
                    >
                        {modelsLoading ? (
                            <SoundWaveLoader variant="inline" />
                        ) : (
                            getVendorIcon(currentModelConfig.vendor)
                        )}
                        <span className={`${compact ? 'max-w-[104px]' : 'max-w-[125px]'} truncate`}>
                            {modelsLoading
                                ? ''
                                : models.length === 0
                                    ? '暂无可用模型'
                                    : currentModelConfig.name}
                        </span>
                        <ChevronDown className={`w-4 h-4 transition-transform ${modelDropdownOpen ? 'rotate-180' : ''}`} />
                    </button>
                    {modelDropdownOpen && !modelSelectorDisabled && (
                        <>
                            <div
                                className="fixed inset-0 z-10"
                                onClick={() => setModelDropdownOpen(false)}
                            />
                            <div className="absolute bottom-full left-0 mb-2 w-56 max-h-80 overflow-y-auto bg-background border border-border rounded-lg shadow-lg z-20">
                                {models.map((model) => {
                                    const isAllowed = model.allowed !== false;
                                    return (
                                        <button
                                            key={model.id}
                                            type="button"
                                            onClick={() => {
                                                onModelChange(model.id);
                                                setModelDropdownOpen(false);
                                            }}
                                            className={`w-full px-3 py-2 text-left text-sm transition-colors flex items-center gap-2 ${isAllowed ? 'hover:bg-background-secondary' : 'opacity-50 cursor-not-allowed'} ${selectedModel === model.id ? 'bg-accent/10 text-accent' : ''}`}
                                            disabled={!isAllowed}
                                        >
                                            {getVendorIcon(model.vendor)}
                                            <div className="flex-1 min-w-0">
                                                <div className="font-medium truncate">{model.name}</div>
                                            </div>
                                            {!isAllowed && model.blockedReason && (
                                                <span className="text-xs text-amber-600 whitespace-nowrap">{model.blockedReason}</span>
                                            )}
                                        </button>
                                    );
                                })}
                            </div>
                        </>
                    )}
                    {modelsError && !modelsLoading && (
                        <div className="mt-1 text-xs text-rose-500">{modelsError}</div>
                    )}
                </div>
            )}

            {onReasoningChange && !toolbarStyle && (
                <>
                    {onModelChange && !compact}
                    <button
                        type="button"
                        onClick={handleReasoningToggle}
                        disabled={disabled || !canToggleReasoning}
                        className={`flex items-center gap-1.5 transition-all ${reasoningBaseClass} ${disabled || !currentModelConfig?.supportsReasoning || !reasoningAllowed
                            ? reasoningDisabledClass
                            : isReasoningForced
                                ? `${reasoningActiveClass} cursor-default`
                                : reasoningEnabled
                                    ? reasoningActiveClass
                                    : reasoningIdleClass
                            }`}
                        title={reasoningTooltip}
                    >
                        <Lightbulb className={`${compact ? 'w-4 h-4' : 'w-4.5 h-4.5'} ${(reasoningEnabled || isReasoningForced) ? 'fill-yellow-500' : ''}`} />
                        <span className={compact ? 'hidden sm:inline' : 'hidden md:inline'}>
                            推理
                        </span>
                    </button>
                </>
            )}
        </div>
    );
}
