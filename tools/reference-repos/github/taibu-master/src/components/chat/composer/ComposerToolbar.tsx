/**
 * Composer 底部工具栏
 *
 * 'use client' 标记说明：
 * - 需要处理用户交互事件
 */
'use client';

import { useState } from 'react';
import {
    ArrowUp,
    Atom,
    AtSign,
    BookOpenText,
    Globe,
    KeyRound,
    Moon,
    Orbit,
    Paperclip,
    Plus,
    Square,
} from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import type { MembershipType } from '@/lib/user/membership';
import { ModelSelector } from '@/components/ui/ModelSelector';
import { PromptPreview } from '@/components/chat/composer/PromptPreview';
import { CustomProviderPanel } from '@/components/chat/CustomProviderPanel';
import type { PromptLayerDiagnostic } from '@/types';
import { getNavItemById } from '@/lib/navigation/registry';
import type { ChatMode } from '@/lib/chat/use-chat-state';

interface ComposerToolbarProps {
    // Menu
    menuOpen: boolean;
    setMenuOpen: (open: boolean) => void;
    // File
    fileInputRef: React.RefObject<HTMLInputElement | null>;
    hasFile: boolean;
    handleFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    // Web search
    hasWebSearch: boolean;
    canUseWeb: boolean;
    handleWebToggle: () => void;
    // Charts & Dream (unified mode)
    chatMode: ChatMode;
    onChatModeChange?: (mode: ChatMode) => void;
    canUseBazi: boolean;
    userId?: string | null;
    // Knowledge base
    knowledgeBaseEnabled: boolean;
    canUseKnowledgeBase: boolean;
    handleKnowledgeBaseOpen: () => void;
    // Mention
    textareaRef: React.RefObject<HTMLTextAreaElement | null>;
    inputValue: string;
    onInputChange: (value: string) => void;
    canMentionAnything: boolean;
    setMentionOpen: (open: boolean) => void;
    setMentionQuery: (query: string) => void;
    setMentionStartIndex: (index: number | null) => void;
    // Prompt preview
    promptPreviewLoading: boolean;
    hasPromptDiagnostics: boolean;
    promptDiagnosticsOpen: boolean;
    setPromptDiagnosticsOpen: (open: boolean | ((prev: boolean) => boolean)) => void;
    contextProgressPercent: number;
    promptProgressPercent: number;
    promptUsageLabel: string;
    promptPreviewTokens: number;
    promptPreviewBudget: number;
    displayLayers: PromptLayerDiagnostic[];
    displayUserMessageTokens: number;
    formatLayerLabel: (layerId: string) => string;
    // Model
    selectedModel: string;
    onModelChange?: (modelId: string) => void;
    reasoningEnabled: boolean;
    onReasoningChange?: (enabled: boolean) => void;
    membershipType: MembershipType;
    customProviderActive: boolean;
    customProviderLabel: string | null;
    // Send
    disabled: boolean;
    isLoading: boolean;
    isSendingToList: boolean;
    dreamContextLoading: boolean;
    handleButtonClick: () => void;
}

export function ComposerToolbar(props: ComposerToolbarProps) {
    const {
        menuOpen, setMenuOpen,
        fileInputRef, hasFile, handleFileChange,
        hasWebSearch, canUseWeb, handleWebToggle,
        chatMode, onChatModeChange, canUseBazi,
        userId,
        knowledgeBaseEnabled, canUseKnowledgeBase, handleKnowledgeBaseOpen,
        textareaRef, inputValue, onInputChange, canMentionAnything,
        setMentionOpen, setMentionQuery, setMentionStartIndex,
        promptPreviewLoading, hasPromptDiagnostics, promptDiagnosticsOpen,
        setPromptDiagnosticsOpen, contextProgressPercent, promptProgressPercent,
        promptUsageLabel, displayLayers, displayUserMessageTokens, formatLayerLabel,
        promptPreviewTokens, promptPreviewBudget,
        selectedModel, onModelChange, reasoningEnabled, onReasoningChange, membershipType,
        customProviderActive, customProviderLabel,
        disabled, isLoading, isSendingToList, dreamContextLoading, handleButtonClick,
    } = props;
    const BaziNavIcon = getNavItemById('bazi')?.icon ?? Orbit;
    const isDreamMode = chatMode === 'dream';
    const isMangpaiMode = chatMode === 'mangpai';
    const [customProviderOpen, setCustomProviderOpen] = useState(false);

    return (
        <div className="flex items-center justify-between gap-3 border-border/50">
            {/* 左侧按钮组 */}
            <div className="flex min-w-0 items-center gap-1.5 flex-shrink">
                <div className="relative">
                    <button
                        type="button"
                        onClick={() => setMenuOpen(!menuOpen)}
                        className={`h-9 w-9 rounded-xl transition-all flex items-center justify-center ${menuOpen
                            ? 'bg-[#f3f0ea] text-[#37352f]'
                            : 'text-[#37352f]/60 hover:bg-[#f3f0ea] hover:text-[#37352f]'
                            }`}
                        title="更多选项"
                    >
                        <Plus className={`w-5.5 h-5.5 transition-transform duration-200 ${menuOpen ? 'rotate-45' : ''}`} />
                    </button>

                    {menuOpen && (
                        <>
                            <div className="fixed inset-0 z-10" onClick={() => setMenuOpen(false)} />
                            <div className="absolute bottom-full left-0 mb-2 w-38 bg-background border border-border rounded-xl shadow-lg z-20 overflow-hidden p-1 flex flex-col gap-1">
                                {/* 附件选项 */}
                                <button
                                    type="button"
                                    onClick={() => {
                                        if (isDreamMode) return;
                                        fileInputRef.current?.click();
                                        setMenuOpen(false);
                                    }}
                                    className={`flex items-center gap-2 w-full px-3 py-2 text-sm rounded-lg transition-all ${hasFile
                                        ? 'bg-blue-500/10 text-blue-600'
                                        : isDreamMode
                                            ? 'opacity-40 text-foreground-secondary cursor-not-allowed'
                                            : 'hover:bg-background-secondary text-foreground-secondary'
                                        }`}
                                    disabled={disabled || isDreamMode}
                                >
                                    <Paperclip className="w-4.5 h-4.5" />
                                    <span>{hasFile ? '更换附件' : '上传附件'}</span>
                                </button>
                                {/* 搜索选项 */}
                                <div className={`flex items-center w-full rounded-lg transition-all ${hasWebSearch
                                    ? 'bg-green-500/10 text-green-600'
                                    : (!canUseWeb || isDreamMode)
                                        ? 'opacity-40 text-foreground-secondary cursor-not-allowed'
                                        : 'hover:bg-background-secondary text-foreground-secondary'
                                    }`}>
                                    <button
                                        type="button"
                                        onClick={() => {
                                            if (isDreamMode) return;
                                            handleWebToggle();
                                            setMenuOpen(false);
                                        }}
                                        className="flex-1 flex items-center gap-2 px-3 py-2 text-sm"
                                        disabled={disabled || isDreamMode}
                                    >
                                        <Globe className="w-4.5 h-4.5" />
                                        <span>{!canUseWeb ? '搜索' : '搜索'}</span>
                                    </button>
                                </div>
                                {canUseBazi && !!userId && onChatModeChange && (
                                    <button
                                        type="button"
                                        onClick={() => {
                                            if (isDreamMode) return;
                                            onChatModeChange(isMangpaiMode ? 'normal' : 'mangpai');
                                            setMenuOpen(false);
                                            textareaRef.current?.focus();
                                        }}
                                        className={`flex items-center gap-2 w-full px-3 py-2 text-sm rounded-lg transition-all ${isMangpaiMode
                                            ? 'bg-orange-500/10 text-orange-600'
                                            : isDreamMode
                                                ? 'opacity-40 text-foreground-secondary cursor-not-allowed'
                                                : 'hover:bg-background-secondary text-foreground-secondary'
                                            }`}
                                        disabled={disabled || isDreamMode}
                                    >
                                        <BaziNavIcon className="w-4.5 h-4.5" />
                                        <span>盲派分析</span>
                                    </button>
                                )}
                                {!!userId && onChatModeChange && (
                                    <button
                                        type="button"
                                        onClick={() => {
                                            onChatModeChange(isDreamMode ? 'normal' : 'dream');
                                            setMenuOpen(false);
                                            textareaRef.current?.focus();
                                        }}
                                        className={`flex items-center gap-2 w-full px-3 py-2 text-sm rounded-lg transition-all ${isDreamMode
                                            ? 'bg-purple-500/10 text-purple-600'
                                            : 'hover:bg-background-secondary text-foreground-secondary'
                                            }`}
                                        disabled={disabled}
                                    >
                                        <Moon className="w-4.5 h-4.5" />
                                        <span>周公解梦</span>
                                    </button>
                                )}
                                {!!userId && knowledgeBaseEnabled && (
                                    <div className={`flex items-center w-full rounded-lg transition-all ${canUseKnowledgeBase
                                        ? 'hover:bg-background-secondary text-foreground-secondary'
                                        : 'opacity-50 text-foreground-secondary hover:bg-background-secondary'
                                        }`}>
                                        <button
                                            type="button"
                                            onClick={handleKnowledgeBaseOpen}
                                            className="flex-1 flex items-center gap-2 w-full px-3 py-2 text-sm"
                                            disabled={disabled}
                                        >
                                            <BookOpenText className="w-4.5 h-4.5" />
                                            <span>{canUseKnowledgeBase ? '知识库' : '知识库 (Plus+)'}</span>
                                        </button>
                                    </div>
                                )}
                                {!!userId && canMentionAnything && (
                                    <button
                                        type="button"
                                        onClick={() => {
                                            const textarea = textareaRef.current;
                                            const caret = textarea?.selectionStart ?? inputValue.length;
                                            const before = inputValue.slice(0, caret);
                                            const after = inputValue.slice(caret);
                                            const nextValue = `${before}@${after}`;
                                            onInputChange(nextValue);
                                            setMentionOpen(true);
                                            setMentionQuery('');
                                            setMentionStartIndex(caret);
                                            setMenuOpen(false);
                                            requestAnimationFrame(() => {
                                                textareaRef.current?.focus();
                                                textareaRef.current?.setSelectionRange(caret + 1, caret + 1);
                                            });
                                        }}
                                        className="flex items-center gap-2 w-full px-3 py-2 text-sm rounded-lg transition-all hover:bg-background-secondary text-foreground-secondary"
                                        disabled={disabled}
                                    >
                                        <AtSign className="w-4.5 h-4.5" />
                                        <span className="truncate flex flex-col items-start text-left">
                                            <span className="truncate w-full">提及</span>
                                        </span>
                                    </button>
                                )}
                            </div>
                        </>
                    )}

                    {/* 隐藏的文件输入 */}
                    <input
                        ref={fileInputRef}
                        type="file"
                        className="hidden"
                        accept=".pdf,.txt,.md,.doc,.docx,.xlsx,.xls,.csv"
                        onChange={handleFileChange}
                    />
                </div>

                <div className="flex h-9 w-9 items-center justify-center">
                    <PromptPreview
                        promptPreviewLoading={promptPreviewLoading}
                        hasPromptDiagnostics={hasPromptDiagnostics}
                        promptDiagnosticsOpen={promptDiagnosticsOpen}
                        setPromptDiagnosticsOpen={setPromptDiagnosticsOpen}
                        contextProgressPercent={contextProgressPercent}
                        promptProgressPercent={promptProgressPercent}
                        promptUsageLabel={promptUsageLabel}
                        promptPreviewTokens={promptPreviewTokens}
                        promptPreviewBudget={promptPreviewBudget}
                        displayLayers={displayLayers}
                        displayUserMessageTokens={displayUserMessageTokens}
                        formatLayerLabel={formatLayerLabel}
                    />
                </div>

                <div className="relative ml-0.5 flex items-center gap-1">
                    <button
                        type="button"
                        onClick={() => setCustomProviderOpen((prev) => !prev)}
                        className={`flex h-9 w-9 items-center justify-center rounded-xl transition-colors duration-150 ${
                            customProviderOpen
                                ? 'bg-[#f3f0ea] text-[#37352f]'
                                : 'text-[#37352f]/60 hover:bg-[#f3f0ea] hover:text-[#37352f]'
                        }`}
                        title="自定义模型"
                    >
                        <KeyRound className="h-4.5 w-4.5" />
                    </button>

                    <div className="relative min-h-[36px] min-w-[136px]">
                        <div
                            className={`transition-opacity duration-150 ${
                                customProviderActive
                                    ? 'pointer-events-none absolute inset-0 opacity-0'
                                    : 'opacity-100'
                            }`}
                        >
                            <ModelSelector
                                selectedModel={selectedModel}
                                onModelChange={onModelChange}
                                reasoningEnabled={reasoningEnabled}
                                onReasoningChange={onReasoningChange}
                                userId={userId}
                                membershipType={membershipType}
                                disabled={disabled}
                                toolbarStyle
                            />
                        </div>
                        <div
                            className={`transition-opacity duration-150 ${
                                customProviderActive
                                    ? 'opacity-100'
                                    : 'pointer-events-none absolute inset-0 opacity-0'
                            }`}
                        >
                            <button
                                type="button"
                                onClick={() => setCustomProviderOpen(true)}
                                className="flex min-w-0 items-center gap-2 rounded-xl px-3 py-1.5 text-left text-[#37352f] transition-colors duration-150 hover:bg-[#f3f0ea]"
                                title="查看或修改自定义模型"
                            >
                                <span className="flex h-7 w-4.5 flex-shrink-0 items-center justify-center rounded-lg text-foreground-secondary">
                                    <Atom className="h-4.5 w-4.5" />
                                </span>
                                <span className="min-w-0">
                                    <span className="block max-w-[132px] truncate text-sm font-medium text-[#37352f]">
                                        {customProviderLabel || '自定义模型'}
                                    </span>
                                </span>
                            </button>
                        </div>
                    </div>

                    {customProviderOpen && (
                        <>
                            <div className="fixed inset-0 z-20" onClick={() => setCustomProviderOpen(false)} />
                            <div className="hidden md:block absolute bottom-full right-[-4rem] mb-2 z-30 origin-bottom-right">
                                <CustomProviderPanel onClose={() => setCustomProviderOpen(false)} />
                            </div>
                            <div className="fixed inset-x-0 bottom-0 z-30 px-3 pb-[calc(var(--sab)+0.75rem)] md:hidden">
                                <CustomProviderPanel onClose={() => setCustomProviderOpen(false)} />
                            </div>
                        </>
                    )}
                </div>
            </div>

            {/* 发送/停止按钮 */}
            <button
                onClick={handleButtonClick}
                disabled={disabled || isSendingToList || (!isLoading && (!inputValue.trim() || dreamContextLoading))}
                className={`
                    px-2 py-2 rounded-full transition-all duration-200 flex items-center gap-2 flex-shrink-0
                    ${isSendingToList
                        ? 'bg-background-tertiary text-foreground-secondary cursor-wait'
                        : isLoading
                        ? 'bg-red-500 text-white hover:bg-red-600'
                        : inputValue.trim() && !disabled && !dreamContextLoading
                            ? 'bg-foreground text-background hover:bg-foreground/90'
                            : 'bg-background-tertiary text-foreground-secondary cursor-not-allowed'
                    }
                `}
            >
                {isSendingToList ? (
                    <SoundWaveLoader variant="inline" />
                ) : isLoading ? (
                    <Square className="w-4.5 h-4.5" strokeWidth={2.5} />
                ) : (
                    <ArrowUp className="w-5 h-5" strokeWidth={2.5} />
                )}
            </button>
        </div>
    );
}
