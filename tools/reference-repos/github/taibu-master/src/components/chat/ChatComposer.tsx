/**
 * 消息输入框组件（主壳）
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useEffect, useCallback, useMemo)
 * - 有文本输入、@mention、附件上传等交互功能
 */
'use client';

import { useEffect, useCallback, useMemo, useRef } from 'react';
import type { AttachmentState, Mention } from '@/types';
import { DEFAULT_MODEL_ID } from '@/lib/ai/ai-config';
import type { MembershipType } from '@/lib/user/membership';
import { useToast } from '@/components/ui/Toast';
import { buildMentionHighlightedParts } from '@/components/chat/mentionHighlight';
import { buildMentionToken, extractMentionTokens, filterMentionsByTokens, removeMentionsByTokens, type MentionToken } from '@/lib/mention-tokens';
import { updateCurrentUserSettings } from '@/lib/user/settings';
import { useFeatureToggles } from '@/lib/hooks/useFeatureToggles';
import { filterDataSourceItemsByFeature, filterMentionsByFeature, getDataSourceFeatureId, getEnabledDataSourceTypes } from '@/lib/data-sources/catalog';
import { useComposerState, type KnowledgeBaseSummary } from '@/components/chat/composer/useComposerState';
import { MentionManager } from '@/components/chat/composer/MentionManager';
import { AttachmentBar } from '@/components/chat/composer/AttachmentBar';
import { ComposerToolbar } from '@/components/chat/composer/ComposerToolbar';
import type { ChatMode } from '@/lib/chat/use-chat-state';

const findLastAtOutsideTokens = (value: string, tokens: MentionToken[]): number => {
    for (let i = value.length - 1; i >= 0; i -= 1) {
        if (value[i] !== '@') continue;
        const inToken = tokens.some(token => i >= token.start && i < token.end);
        if (!inToken) return i;
    }
    return -1;
};

interface ChatComposerProps {
    inputValue: string;
    isLoading: boolean;
    isSendingToList?: boolean;
    onInputChange: (value: string) => void;
    onSend: () => void;
    onStop?: () => void;
    onAuthRequired?: () => void;
    disabled?: boolean;
    chatMode?: ChatMode;
    onChatModeChange?: (mode: ChatMode) => void;
    selectedModel?: string;
    onModelChange?: (modelId: string) => void;
    reasoningEnabled?: boolean;
    onReasoningChange?: (enabled: boolean) => void;
    customProviderActive?: boolean;
    customProviderLabel?: string | null;
    userId?: string | null;
    membershipType?: MembershipType;
    attachmentState?: AttachmentState;
    onAttachmentChange?: (state: AttachmentState) => void;
    mentions?: Mention[];
    onMentionsChange?: (mentions: Mention[]) => void;
    promptKnowledgeBases?: KnowledgeBaseSummary[];
    contextMessages?: Array<{ content?: string }>;
    hideDisclaimer?: boolean;
    dreamContext?: { baziChartName?: string; dailyFortune?: string };
    dreamContextLoading?: boolean;
    knowledgeBaseEnabled?: boolean;
}

export function ChatComposer({
    inputValue,
    isLoading,
    isSendingToList = false,
    onInputChange,
    onSend,
    onStop,
    onAuthRequired,
    disabled = false,
    chatMode = 'normal',
    onChatModeChange,
    selectedModel = DEFAULT_MODEL_ID,
    onModelChange,
    reasoningEnabled = false,
    onReasoningChange,
    customProviderActive = false,
    customProviderLabel = null,
    userId,
    membershipType = 'free',
    attachmentState,
    onAttachmentChange,
    mentions = [],
    onMentionsChange,
    promptKnowledgeBases = [],
    contextMessages = [],
    hideDisclaimer = false,
    dreamContext,
    dreamContextLoading = false,
    knowledgeBaseEnabled = true,
}: ChatComposerProps) {
    const { showToast } = useToast();
    const { isFeatureEnabled } = useFeatureToggles();
    const canUseBaziChart = isFeatureEnabled('bazi');
    const enabledMentionDataSourceTypes = useMemo(
        () => getEnabledDataSourceTypes(isFeatureEnabled),
        [isFeatureEnabled]
    );

    // 防止 mention 选中后 state 还未同步就触发发送
    const mentionSettlingRef = useRef(false);
    const isDreamMode = chatMode === 'dream';

    const state = useComposerState({
        userId, membershipType, selectedModel, reasoningEnabled,
        mentions, contextMessages,
        isLoading, isSendingToList, chatMode,
        knowledgeBaseEnabled, promptKnowledgeBases,
        enabledDataSourceTypes: enabledMentionDataSourceTypes,
    });

    const {
        textareaRef, fileInputRef, overlayRef,
        menuOpen, setMenuOpen,
        mentionOpen, setMentionOpen,
        mentionQuery, setMentionQuery,
        mentionStartIndex, setMentionStartIndex,
        mentionDataSources, mentionKnowledgeBases,
        mentionLoadError, mentionDataSourceErrors,
        mentionLoading, mentionDefaultCategory, setMentionDefaultCategory,
        knowledgeBaseOpen, setKnowledgeBaseOpen,
        knowledgeBaseSavingId,
        promptDiagnosticsOpen, setPromptDiagnosticsOpen,
        canUseWeb, canUseBoth, canUseKnowledgeBase,
        promptProgressPercent, contextProgressPercent,
        hasPromptDiagnostics, displayLayers, displayUserMessageTokens,
        promptUsageLabel, promptPreviewLoading,
        promptPreviewTokens, promptPreviewBudget,
        canMentionAnything,
        promptKbIdSet,
        formatLayerLabel, refreshMentionData,
    } = state;

    const hasFile = !!attachmentState?.file;
    const hasWebSearch = !!attachmentState?.webSearchEnabled;
    const filteredMentionDataSources = useMemo(
        () => filterDataSourceItemsByFeature(mentionDataSources, isFeatureEnabled),
        [isFeatureEnabled, mentionDataSources]
    );
    const filteredMentionDataSourceErrors = useMemo(
        () => filterDataSourceItemsByFeature(mentionDataSourceErrors, isFeatureEnabled),
        [isFeatureEnabled, mentionDataSourceErrors]
    );
    const normalizedMentions = useMemo(
        () => filterMentionsByFeature(mentions ?? [], {
            knowledgeBaseEnabled: canUseKnowledgeBase,
            enabledDataSourceTypes: enabledMentionDataSourceTypes,
        }),
        [canUseKnowledgeBase, enabledMentionDataSourceTypes, mentions]
    );

    useEffect(() => {
        if (!onMentionsChange) return;
        if (normalizedMentions.length !== mentions.length) {
            onMentionsChange(normalizedMentions);
            return;
        }
        for (let i = 0; i < mentions.length; i += 1) {
            const current = mentions[i];
            const normalized = normalizedMentions[i];
            if (!normalized
                || current.type !== normalized.type
                || current.id !== normalized.id
                || current.name !== normalized.name
                || current.preview !== normalized.preview) {
                onMentionsChange(normalizedMentions);
                return;
            }
        }
    }, [mentions, normalizedMentions, onMentionsChange]);

    // --- Event handlers ---
    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file || !onAttachmentChange) return;
        if (!canUseBoth && attachmentState?.webSearchEnabled) {
            onAttachmentChange({ file, webSearchEnabled: false });
            showToast('info', '同时使用搜索和附件仅限 Pro 用户，已自动关闭搜索');
        } else {
            onAttachmentChange({ ...attachmentState, file, webSearchEnabled: attachmentState?.webSearchEnabled ?? false });
        }
        e.target.value = '';
    };

    const handleWebToggle = () => {
        if (!onAttachmentChange) return;
        if (!canUseWeb) {
            showToast('info', '网络搜索仅限 Plus 以上用户使用');
            return;
        }
        const newWebSearch = !attachmentState?.webSearchEnabled;
        if (!canUseBoth && attachmentState?.file && newWebSearch) {
            onAttachmentChange({ file: undefined, webSearchEnabled: true });
            showToast('info', '同时使用搜索和附件仅限 Pro 用户，已自动清除附件');
        } else {
            onAttachmentChange({ file: attachmentState?.file, webSearchEnabled: newWebSearch });
        }
    };

    const handleKnowledgeBaseOpen = async () => {
        if (!canUseKnowledgeBase) {
            showToast('info', '知识库仅限 Plus 以上会员使用');
            return;
        }
        setKnowledgeBaseOpen(true);
        state.setMentionLoadError(null);
        setMenuOpen(false);
        textareaRef.current?.focus();
        await refreshMentionData(true);
    };

    const toggleKnowledgeBaseSearch = useCallback(async (kbId: string) => {
        if (!userId) return;
        if (membershipType === 'free') {
            showToast('info', '仅限 Plus 以上会员使用');
            return;
        }
        const nextPromptIds = promptKbIdSet.has(kbId)
            ? Array.from(promptKbIdSet).filter(id => id !== kbId)
            : Array.from(new Set([...promptKbIdSet, kbId]));
        state.setKnowledgeBaseSavingId(kbId);
        const saved = await updateCurrentUserSettings({ promptKbIds: nextPromptIds });
        state.setKnowledgeBaseSavingId(null);
        if (!saved) {
            showToast('error', '保存知识库失败');
            return;
        }
        showToast('success', promptKbIdSet.has(kbId) ? '已关闭知识库搜索' : '已启用知识库搜索');
    }, [membershipType, promptKbIdSet, showToast, userId, state]);

    // Auto-resize textarea
    useEffect(() => {
        const textarea = textareaRef.current;
        if (!textarea) return;
        textarea.style.height = 'auto';
        const newHeight = Math.min(Math.max(textarea.scrollHeight, 24), 236);
        textarea.style.height = `${newHeight}px`;
        if (overlayRef.current) {
            overlayRef.current.scrollTop = textarea.scrollTop;
        }
    }, [inputValue, mentions, textareaRef, overlayRef]);

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (mentionOpen) return;
        if (e.key === 'Backspace' || e.key === 'Delete') {
            const textarea = textareaRef.current;
            if (textarea) {
                const tokens = extractMentionTokens(inputValue, mentions);
                if (textarea.selectionStart !== textarea.selectionEnd) {
                    const start = textarea.selectionStart;
                    const end = textarea.selectionEnd;
                    const overlaps = tokens.filter(token => token.start < end && token.end > start);
                    if (overlaps.length > 0) {
                        e.preventDefault();
                        const removeStart = Math.min(start, ...overlaps.map(t => t.start));
                        const removeEnd = Math.max(end, ...overlaps.map(t => t.end));
                        const nextValue = `${inputValue.slice(0, removeStart)}${inputValue.slice(removeEnd)}`;
                        onInputChange(nextValue);
                        if (onMentionsChange) {
                            onMentionsChange(removeMentionsByTokens(mentions, tokens, overlaps));
                        }
                        requestAnimationFrame(() => {
                            textareaRef.current?.setSelectionRange(removeStart, removeStart);
                        });
                        return;
                    }
                } else {
                    const caret = e.key === 'Backspace' ? textarea.selectionStart - 1 : textarea.selectionStart;
                    if (caret >= 0) {
                        const target = tokens.find(token => caret >= token.start && caret < token.end);
                        if (target) {
                            e.preventDefault();
                            const nextValue = `${inputValue.slice(0, target.start)}${inputValue.slice(target.end)}`;
                            onInputChange(nextValue);
                            if (onMentionsChange) {
                                onMentionsChange(removeMentionsByTokens(mentions, tokens, [target]));
                            }
                            requestAnimationFrame(() => {
                                textareaRef.current?.setSelectionRange(target.start, target.start);
                            });
                            return;
                        }
                    }
                }
            }
        }
        if (e.key === 'Enter' && !e.shiftKey && !disabled && !isLoading && !isSendingToList && !dreamContextLoading && !mentionSettlingRef.current && inputValue.trim()) {
            e.preventDefault();
            if (!userId && onAuthRequired) {
                onAuthRequired();
                return;
            }
            onSend();
        }
    };

    const handleInputChange = (value: string) => {
        onInputChange(value);
        const tokens = extractMentionTokens(value, mentions);
        if (onMentionsChange) {
            const nextMentions = filterMentionsByTokens(mentions, tokens);
            if (nextMentions.length !== mentions.length) {
                onMentionsChange(nextMentions);
            }
        }
        const atIndex = findLastAtOutsideTokens(value, tokens);
        if (!canMentionAnything) {
            setMentionOpen(false);
            setMentionQuery('');
            setMentionStartIndex(null);
            return;
        }
        if (atIndex >= 0) {
            const prev = atIndex > 0 ? value[atIndex - 1] : '';
            const isEmailLike = !!prev && /[A-Za-z0-9._-]/.test(prev);
            const tail = value.slice(atIndex + 1);
            const hasSpaceInTail = /\s/.test(tail);
            if (!isEmailLike && !hasSpaceInTail) {
                setMentionOpen(true);
                setMentionQuery(tail || '');
                setMentionStartIndex(atIndex);
                return;
            }
        }
        setMentionOpen(false);
        setMentionQuery('');
        setMentionStartIndex(null);
    };

    const handleSelectMention = (mention: Mention) => {
        if (!onMentionsChange) return;
        if (mention.type === 'knowledge_base' && !canUseKnowledgeBase) {
            showToast('info', '知识库仅限 Plus 以上会员使用');
            return;
        }
        if (mention.type !== 'knowledge_base' && !isFeatureEnabled(getDataSourceFeatureId(mention.type))) {
            showToast('info', '该数据来源已关闭');
            return;
        }
        const isDuplicate = mentions.some(m => m.id === mention.id && m.type === mention.type);
        if (isDuplicate) {
            showToast('info', '已添加过该项');
            return;
        }
        const next = [...mentions, mention].slice(0, 10);
        onMentionsChange(next);
        // 标记 mention 正在同步，阻止在 state 更新前触发发送
        mentionSettlingRef.current = true;
        queueMicrotask(() => { mentionSettlingRef.current = false; });
        const token = buildMentionToken(mention);
        if (mentionStartIndex != null) {
            const prefix = inputValue.slice(0, mentionStartIndex).trimEnd();
            const nextValue = `${prefix} ${token} `;
            onInputChange(nextValue.trimStart());
        } else {
            const nextValue = inputValue.trim() ? `${inputValue.trim()} ${token} ` : `${token} `;
            onInputChange(nextValue);
        }
        setMentionOpen(false);
        setMentionQuery('');
        setMentionStartIndex(null);
        setMentionDefaultCategory(null);
        textareaRef.current?.focus();
    };

    const highlightedInput = useMemo(() => {
        return buildMentionHighlightedParts(inputValue, mentions);
    }, [inputValue, mentions]);

    const handleButtonClick = () => {
        if (isSendingToList || mentionSettlingRef.current) return;
        if (isLoading && onStop) {
            onStop();
        } else if (inputValue.trim()) {
            if (!userId && onAuthRequired) {
                onAuthRequired();
                return;
            }
            onSend();
        }
    };

    return (
        <div className={`fixed left-0 right-0 bottom-[calc(3.5rem+var(--sab))] ${knowledgeBaseOpen ? 'z-[60]' : 'z-30'} md:sticky md:bottom-0 md:left-auto md:right-auto border-border bg-gradient-to-t from-background/95 to-transparent backdrop-blur-[2px] md:backdrop-blur-none pb-3 ${disabled ? 'opacity-50' : ''}`}>
            <div className="relative max-w-3xl mx-auto md:p-0 p-2">
                <MentionManager
                    userId={userId}
                    mentionOpen={mentionOpen}
                    setMentionOpen={setMentionOpen}
                    mentionQuery={mentionQuery}
                    mentionDataSources={filteredMentionDataSources}
                    mentionKnowledgeBases={mentionKnowledgeBases}
                    enabledDataSourceTypes={enabledMentionDataSourceTypes}
                    mentionLoadError={mentionLoadError}
                    mentionDataSourceErrors={filteredMentionDataSourceErrors}
                    mentionLoading={mentionLoading}
                    mentionDefaultCategory={mentionDefaultCategory}
                    setMentionDefaultCategory={setMentionDefaultCategory}
                    canUseKnowledgeBase={canUseKnowledgeBase}
                    handleSelectMention={handleSelectMention}
                    knowledgeBaseOpen={knowledgeBaseOpen}
                    setKnowledgeBaseOpen={setKnowledgeBaseOpen}
                    knowledgeBaseSavingId={knowledgeBaseSavingId}
                    promptKbIdSet={promptKbIdSet}
                    toggleKnowledgeBaseSearch={toggleKnowledgeBaseSearch}
                />

                {/* 输入框容器 */}
                <div className="relative flex flex-col gap-1 p-3 rounded-4xl bg-background/90 border border-border transition-all duration-300">
                    <AttachmentBar
                        hasFile={hasFile}
                        attachmentState={attachmentState}
                        onAttachmentChange={onAttachmentChange}
                        disabled={disabled}
                        canUseKnowledgeBase={canUseKnowledgeBase}
                        promptKnowledgeBases={promptKnowledgeBases}
                        isDreamMode={isDreamMode}
                        dreamContextLoading={dreamContextLoading}
                        dreamContext={dreamContext}
                    />

                    {/* 输入框区域 */}
                    <div className="relative">
                        <div className="relative">
                            <div ref={overlayRef} className="pointer-events-none absolute inset-0 text-base py-2 px-2 whitespace-pre-wrap break-words text-foreground overflow-y-auto">
                                {inputValue ? (
                                    <span>
                                        {highlightedInput.map((part) => (
                                            part.kind === 'mention'
                                                ? (
                                                    <span key={`${part.start}-${part.end}`} className={part.className}>
                                                        {part.value}
                                                    </span>
                                                )
                                                : part.value
                                        ))}
                                    </span>
                                ) : (
                                    <span className="text-foreground-secondary/80">
                                        {disabled ? "请先获取积分" : isDreamMode ? "\u{1F319} 做了什么梦" : "尽管问"}
                                    </span>
                                )}
                            </div>
                            <textarea
                                ref={textareaRef}
                                value={inputValue}
                                onChange={(e) => handleInputChange(e.target.value)}
                                onKeyDown={handleKeyDown}
                                onScroll={(e) => {
                                    if (overlayRef.current) {
                                        overlayRef.current.scrollTop = e.currentTarget.scrollTop;
                                    }
                                }}
                                placeholder=""
                                className="w-full bg-transparent resize-none text-base py-2 px-2 text-transparent caret-foreground focus:outline-none placeholder:text-foreground-secondary/80 disabled:cursor-not-allowed overflow-y-auto"
                                disabled={disabled}
                                rows={1}
                            />
                        </div>
                        <div className="pointer-events-none absolute inset-x-0 bottom-0 h-8 bg-gradient-to-t from-background/60 to-transparent" />
                    </div>

                    {/* 底部按钮栏 */}
                    <ComposerToolbar
                        menuOpen={menuOpen}
                        setMenuOpen={setMenuOpen}
                        fileInputRef={fileInputRef}
                        hasFile={hasFile}
                        handleFileChange={handleFileChange}
                        hasWebSearch={hasWebSearch}
                        canUseWeb={canUseWeb}
                        handleWebToggle={handleWebToggle}
                        chatMode={chatMode}
                        onChatModeChange={onChatModeChange}
                        canUseBazi={canUseBaziChart}
                        userId={userId}
                        canMentionAnything={canMentionAnything}
                        knowledgeBaseEnabled={knowledgeBaseEnabled}
                        canUseKnowledgeBase={canUseKnowledgeBase}
                        handleKnowledgeBaseOpen={handleKnowledgeBaseOpen}
                        textareaRef={textareaRef}
                        inputValue={inputValue}
                        onInputChange={onInputChange}
                        setMentionOpen={setMentionOpen}
                        setMentionQuery={setMentionQuery}
                        setMentionStartIndex={setMentionStartIndex}
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
                        selectedModel={selectedModel}
                        onModelChange={onModelChange}
                        reasoningEnabled={reasoningEnabled}
                        onReasoningChange={onReasoningChange}
                        membershipType={membershipType}
                        customProviderActive={customProviderActive}
                        customProviderLabel={customProviderLabel}
                        disabled={disabled}
                        isLoading={isLoading}
                        isSendingToList={isSendingToList}
                        dreamContextLoading={dreamContextLoading}
                        handleButtonClick={handleButtonClick}
                    />
                </div>

                {!hideDisclaimer && (
                    <p className="text-center text-xs text-foreground-secondary/90 mt-1">
                        AI 回复仅供参考，请理性看待命理分析结果
                    </p>
                )}
            </div>
        </div>
    );
}
