/**
 * 聊天消息项组件
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useState)
 * - 需要处理用户交互事件
 */
'use client';

import { memo, useState, useMemo, useCallback, useRef } from 'react';
import { Pencil, Check, X, RefreshCw, Copy, ChevronLeft, ChevronRight, FileText, BookOpenText, Globe, KeyRound } from 'lucide-react';
import type { AIMessageMetadata, ChatMessage, InjectedSource, Mention } from '@/types';
import { resolveClientModelName } from '@/lib/ai/model-name-cache';
import { getEnabledDataSourceTypes } from '@/lib/data-sources/catalog';
import { formatMentionsForDisplay } from '@/lib/format-mentions';
import { getVisibleSourcePanelState } from '@/lib/chat/feature-normalization';
import { useFeatureToggles } from '@/lib/hooks/useFeatureToggles';
import { extractMentionTokens, filterMentionsByTokens, removeMentionsByTokens } from '@/lib/mention-tokens';
import { MarkdownContent } from '@/components/ui/MarkdownContent';
import { ThinkingBlock } from '@/components/chat/ThinkingBlock';
import { SourcePanel } from '@/components/chat/SourcePanel';
import { buildMentionHighlightedParts } from '@/components/chat/mentionHighlight';
import { useKnowledgeBaseFeatureEnabled } from '@/components/knowledge-base/useKnowledgeBaseFeatureEnabled';
import { openSettingsCenter } from '@/lib/settings-center';

interface ChatMessageItemProps {
    message: ChatMessage;
    isStreamingAI: boolean;
    isLastMessage: boolean;
    disabled?: boolean;
    onEditMessage?: (messageId: string, newContent: string, mentions?: Mention[]) => void;
    onRegenerateResponse?: (messageId: string) => void;
    onSwitchVersion?: (messageId: string, versionIndex: number) => void;
    onArchiveMessage?: (message: ChatMessage) => void;
}

export const ChatMessageItem = memo(function ChatMessageItem({
    message,
    isStreamingAI,
    isLastMessage,
    disabled = false,
    onEditMessage,
    onRegenerateResponse,
    onSwitchVersion,
    onArchiveMessage,
}: ChatMessageItemProps) {
    const [editingId, setEditingId] = useState<string | null>(null);
    const [editContent, setEditContent] = useState('');
    const [editMentions, setEditMentions] = useState<Mention[]>([]);
    const [copiedId, setCopiedId] = useState<string | null>(null);
    const [hoveredAction, setHoveredAction] = useState<string | null>(null);
    const [expandedSources, setExpandedSources] = useState<Record<string, boolean>>({});
    const editTextareaRef = useRef<HTMLTextAreaElement | null>(null);
    const editOverlayRef = useRef<HTMLDivElement | null>(null);

    const highlightedUserContentParts = useMemo(() => {
        if (message.role !== 'user') return [];
        const displayContent = formatMentionsForDisplay(message.content);
        return buildMentionHighlightedParts(displayContent, message.mentions ?? []);
    }, [message.content, message.mentions, message.role]);

    const handleStartEdit = useCallback(() => {
        if (disabled) return;
        setEditingId(message.id);
        setEditContent(formatMentionsForDisplay(message.content));
        setEditMentions(message.mentions ?? []);
    }, [disabled, message.content, message.id, message.mentions]);

    const handleSaveEdit = useCallback(() => {
        const trimmed = editContent.trim();
        if (editingId && onEditMessage && trimmed) {
            const tokens = extractMentionTokens(trimmed, editMentions);
            const nextMentions = filterMentionsByTokens(editMentions, tokens);
            onEditMessage(editingId, trimmed, nextMentions);
        }
        setEditingId(null);
        setEditContent('');
        setEditMentions([]);
    }, [editingId, editContent, editMentions, onEditMessage]);

    const handleCancelEdit = useCallback(() => {
        setEditingId(null);
        setEditContent('');
        setEditMentions([]);
    }, []);

    const handleEditInputChange = useCallback((value: string) => {
        setEditContent(value);
        const tokens = extractMentionTokens(value, editMentions);
        const next = filterMentionsByTokens(editMentions, tokens);
        if (next.length !== editMentions.length) {
            setEditMentions(next);
        }
    }, [editMentions]);

    const handleEditKeyDown = useCallback((e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key !== 'Backspace' && e.key !== 'Delete') return;
        const textarea = editTextareaRef.current;
        if (!textarea) return;

        const tokens = extractMentionTokens(editContent, editMentions);
        if (tokens.length === 0) return;

        if (textarea.selectionStart !== textarea.selectionEnd) {
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const overlaps = tokens.filter(token => token.start < end && token.end > start);
            if (overlaps.length === 0) return;
            e.preventDefault();
            const removeStart = Math.min(start, ...overlaps.map(t => t.start));
            const removeEnd = Math.max(end, ...overlaps.map(t => t.end));
            const nextValue = `${editContent.slice(0, removeStart)}${editContent.slice(removeEnd)}`;
            setEditContent(nextValue);
            setEditMentions(removeMentionsByTokens(editMentions, tokens, overlaps));
            requestAnimationFrame(() => {
                editTextareaRef.current?.setSelectionRange(removeStart, removeStart);
            });
            return;
        }

        const caret = e.key === 'Backspace' ? textarea.selectionStart - 1 : textarea.selectionStart;
        if (caret < 0) return;
        const target = tokens.find(token => caret >= token.start && caret < token.end);
        if (!target) return;
        e.preventDefault();
        const nextValue = `${editContent.slice(0, target.start)}${editContent.slice(target.end)}`;
        setEditContent(nextValue);
        setEditMentions(removeMentionsByTokens(editMentions, tokens, [target]));
        requestAnimationFrame(() => {
            editTextareaRef.current?.setSelectionRange(target.start, target.start);
        });
    }, [editContent, editMentions]);

    const highlightedEditContentParts = useMemo(() => {
        if (!editContent) return [];
        return buildMentionHighlightedParts(editContent, editMentions);
    }, [editContent, editMentions]);

    const handleCopy = useCallback(async () => {
        try {
            await navigator.clipboard.writeText(message.content);
            setCopiedId(message.id);
            setTimeout(() => setCopiedId(null), 2000);
        } catch {
            // 复制失败
        }
    }, [message.content, message.id]);

    const isCurrentStreaming = isStreamingAI && isLastMessage;

    if (message.role === 'user') {
        return (
            <div className="group flex justify-end">
                {editingId === message.id ? (
                    <div className="w-full max-w-[85%] space-y-2">
                        <div className="relative w-full rounded-lg bg-background-secondary border border-border focus-within:ring-2 focus-within:ring-accent/30">
                            <div
                                ref={editOverlayRef}
                                className="pointer-events-none absolute inset-0 px-4 py-3 whitespace-pre-wrap break-words text-base leading-relaxed text-foreground overflow-y-auto"
                            >
                                {highlightedEditContentParts.map((part) => (
                                    part.kind === 'mention'
                                        ? (
                                            <span key={`${part.start}-${part.end}`} className={part.className}>
                                                {part.value}
                                            </span>
                                        )
                                        : part.value
                                ))}
                            </div>
                            <textarea
                                ref={editTextareaRef}
                                value={editContent}
                                onChange={(e) => handleEditInputChange(e.target.value)}
                                onKeyDown={handleEditKeyDown}
                                onScroll={(e) => {
                                    if (editOverlayRef.current) {
                                        editOverlayRef.current.scrollTop = e.currentTarget.scrollTop;
                                    }
                                }}
                                className="w-full bg-transparent px-4 py-3 rounded-lg text-base leading-relaxed resize-none text-transparent caret-foreground focus:outline-none overflow-y-auto"
                                rows={3}
                                autoFocus
                            />
                        </div>
                        <div className="flex gap-2 justify-end">
                            <button
                                onClick={handleSaveEdit}
                                className="flex items-center gap-1.5 px-4 py-1.5 rounded-md bg-accent text-white text-xs font-bold hover:bg-accent/90 active:bg-accent/80 transition-all duration-150"
                            >
                                <Check className="w-3.5 h-3.5" />
                                发送
                            </button>
                            <button
                                onClick={handleCancelEdit}
                                className="flex items-center gap-1.5 px-4 py-1.5 rounded-md border border-border bg-background text-xs font-bold text-foreground hover:bg-background-secondary active:bg-background-tertiary transition-all duration-150"
                            >
                                <X className="w-3.5 h-3.5" />
                                取消
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="flex flex-col items-end w-full max-w-[85%]">
                        {/* 附件信息显示 */}
                        {message.attachments && (message.attachments.fileName || message.attachments.webSearchEnabled) && (
                            <div className="flex items-center gap-2 mb-2">
                                {message.attachments.fileName && (
                                    <div className="flex items-center gap-3 px-3 py-2 bg-background border border-border rounded-md max-w-[240px] shadow-sm">
                                        <div className="flex-shrink-0 w-8 h-8 bg-accent/10 rounded flex items-center justify-center border border-accent/10">
                                            <FileText className="w-4 h-4 text-accent" />
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className="text-xs font-bold text-foreground truncate">
                                                {message.attachments.fileName}
                                            </p>
                                            <p className="text-[10px] font-bold text-foreground-secondary uppercase tracking-tight">文件</p>
                                        </div>
                                    </div>
                                )}
                                {message.attachments.webSearchEnabled && (
                                    <div className="flex items-center gap-2 px-3 py-1.5 bg-green-500/10 border border-green-500/20 rounded-md text-green-600 shadow-sm">
                                        <Globe className="w-3.5 h-3.5" />
                                        <span className="text-xs font-bold uppercase tracking-tight">网络搜索</span>
                                    </div>
                                )}
                            </div>
                        )}
                        {message.dreamInfo && (
                            <div className="flex items-center gap-2 mb-1.5 text-[10px] font-bold uppercase tracking-widest text-purple-500/70 dark:text-purple-400/70">
                                <span>解梦</span>
                                <span>·</span>
                                <span>{new Date(message.dreamInfo.dreamDate).toLocaleDateString('zh-CN')}</span>
                            </div>
                        )}
                        <div className={`px-4 py-1.5 rounded-xl rounded-tr-none shadow-sm text-foreground border ${message.dreamInfo
                            ? 'bg-purple-500/10 dark:bg-purple-500/15 border border-purple-500/20'
                            : 'bg-accent/10 border border-accent/20'
                        }`}>
                            <p className="whitespace-pre-wrap text-base leading-relaxed">
                                {highlightedUserContentParts.map((part) => (
                                    part.kind === 'mention'
                                        ? (
                                            <span key={`${part.start}-${part.end}`} className={part.className}>
                                                {part.value}
                                            </span>
                                        )
                                        : part.value
                                ))}
                            </p>
                        </div>
                        {/* 操作按钮和版本切换 */}
                        {!disabled && (
                            <UserMessageActions
                                message={message}
                                copiedId={copiedId}
                                hoveredAction={hoveredAction}
                                onCopy={handleCopy}
                                onStartEdit={handleStartEdit}
                                onSwitchVersion={onSwitchVersion}
                                setHoveredAction={setHoveredAction}
                            />
                        )}
                    </div>
                )}
            </div>
        );
    }

    // AI 消息
    const showCheckKeyAction = message.metadata?.customProviderErrorAction === 'check-key';
    return (
        <div className="group w-full">
            {/* 显示思考过程 */}
            {message.reasoning && (
                <ThinkingBlock
                    content={message.reasoning}
                    isStreaming={isCurrentStreaming && !message.content}
                    startTime={message.reasoningStartTime}
                    duration={message.reasoningDuration}
                />
            )}
            {message.dreamInfo && (
                <div className="mb-3 flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-purple-500/70 dark:text-purple-400/70">
                    <span>🌙</span>
                    <span>解梦</span>
                    <span>·</span>
                    <span>{message.dreamInfo.userName}</span>
                    <span>·</span>
                    <span>{new Date(message.dreamInfo.dreamDate).toLocaleDateString('zh-CN')}</span>
                    {message.dreamInfo.baziChartName && (
                        <>
                            <span>·</span>
                            <span className="text-foreground-secondary">📜 {message.dreamInfo.baziChartName}</span>
                        </>
                    )}
                </div>
            )}
            <MarkdownContent content={message.content} className="text-base text-foreground leading-relaxed" />
            {showCheckKeyAction && !isCurrentStreaming && (
                <button
                    type="button"
                    onClick={() => openSettingsCenter('personalization')}
                    className="mt-3 inline-flex items-center gap-2 rounded-lg border border-amber-300/60 bg-amber-500/5 px-3 py-1.5 text-sm text-amber-700 transition-colors hover:bg-amber-500/10 dark:border-amber-400/30 dark:text-amber-200"
                >
                    <KeyRound className="h-4 w-4" />
                    检查 Key
                </button>
            )}
            {isCurrentStreaming && !message.content && (
                <div className="mt-3 inline-flex items-center gap-[3px] h-4">
                    {[0, 1, 2, 3].map((i) => (
                        <span key={i} className="sound-wave-bar w-[3px] rounded-full bg-foreground/30" style={{ animationDelay: `${i * 0.15}s` }} />
                    ))}
                </div>
            )}
            {/* 来源面板 */}
            <SourcePanelSection
                message={message}
                isCurrentStreaming={isCurrentStreaming}
                expandedSources={expandedSources}
                setExpandedSources={setExpandedSources}
            />
            {/* 操作按钮 */}
            {message.content && !isCurrentStreaming && (
                <AIMessageActions
                    message={message}
                    disabled={disabled}
                    copiedId={copiedId}
                    hoveredAction={hoveredAction}
                    onCopy={handleCopy}
                    onRegenerateResponse={onRegenerateResponse}
                    onArchiveMessage={onArchiveMessage}
                    setHoveredAction={setHoveredAction}
                />
            )}
        </div>
    );
});

// 用户消息操作按钮
interface UserMessageActionsProps {
    message: ChatMessage;
    copiedId: string | null;
    hoveredAction: string | null;
    onCopy: () => void;
    onStartEdit: () => void;
    onSwitchVersion?: (messageId: string, versionIndex: number) => void;
    setHoveredAction: (action: string | null) => void;
}

function UserMessageActions({
    message,
    copiedId,
    hoveredAction,
    onCopy,
    onStartEdit,
    onSwitchVersion,
    setHoveredAction,
}: UserMessageActionsProps) {
    return (
        <div className="flex items-center mt-1.5 opacity-0 group-hover:opacity-100 transition-opacity duration-150">
            <button
                onClick={onCopy}
                onMouseEnter={() => setHoveredAction(`copy-user-${message.id}`)}
                onMouseLeave={() => setHoveredAction(null)}
                className="relative p-1.5 text-foreground-secondary hover:text-foreground hover:bg-background-secondary rounded-md transition-all duration-150"
            >
                {copiedId === message.id ? (
                    <Check className="w-4 h-4 text-green-600" />
                ) : (
                    <Copy className="w-4 h-4" />
                )}
                {hoveredAction === `copy-user-${message.id}` && (
                    <span className="absolute top-full mt-2 left-1/2 -translate-x-1/2 px-2 py-1 text-[10px] font-bold bg-foreground text-background rounded shadow-md whitespace-nowrap z-10 uppercase tracking-wider">
                        {copiedId === message.id ? '已复制' : '复制'}
                    </span>
                )}
            </button>
            <button
                onClick={onStartEdit}
                onMouseEnter={() => setHoveredAction(`edit-${message.id}`)}
                onMouseLeave={() => setHoveredAction(null)}
                className="relative p-1.5 text-foreground-secondary hover:text-foreground hover:bg-background-secondary rounded-md transition-all duration-150"
            >
                <Pencil className="w-4 h-4" />
                {hoveredAction === `edit-${message.id}` && (
                    <span className="absolute top-full mt-2 left-1/2 -translate-x-1/2 px-2 py-1 text-[10px] font-bold bg-foreground text-background rounded shadow-md whitespace-nowrap z-10 uppercase tracking-wider">
                        编辑消息
                    </span>
                )}
            </button>
            {message.versions && message.versions.length > 1 && onSwitchVersion && (
                <div className="flex items-center gap-1 text-foreground-secondary ml-1">
                    <button
                        onClick={() => {
                            const currentIdx = message.currentVersionIndex ?? message.versions!.length - 1;
                            if (currentIdx > 0) {
                                onSwitchVersion(message.id, currentIdx - 1);
                            }
                        }}
                        disabled={(message.currentVersionIndex ?? message.versions.length - 1) === 0}
                        className="p-1 hover:bg-background-secondary hover:text-foreground rounded-md disabled:opacity-20 disabled:cursor-not-allowed transition-all duration-150"
                    >
                        <ChevronLeft className="w-4 h-4" />
                    </button>
                    <span className="text-[10px] font-bold min-w-[1.5rem] text-center uppercase tracking-tighter">
                        {(message.currentVersionIndex ?? message.versions.length - 1) + 1} / {message.versions.length}
                    </span>
                    <button
                        onClick={() => {
                            const currentIdx = message.currentVersionIndex ?? message.versions!.length - 1;
                            if (currentIdx < message.versions!.length - 1) {
                                onSwitchVersion(message.id, currentIdx + 1);
                            }
                        }}
                        disabled={(message.currentVersionIndex ?? message.versions.length - 1) === message.versions.length - 1}
                        className="p-1 hover:bg-background-secondary hover:text-foreground rounded-md disabled:opacity-20 disabled:cursor-not-allowed transition-all duration-150"
                    >
                        <ChevronRight className="w-4 h-4" />
                    </button>
                </div>
            )}
        </div>
    );
}

// 来源面板区域
interface SourcePanelSectionProps {
    message: ChatMessage;
    isCurrentStreaming: boolean;
    expandedSources: Record<string, boolean>;
    setExpandedSources: React.Dispatch<React.SetStateAction<Record<string, boolean>>>;
}

function SourcePanelSection({
    message,
    isCurrentStreaming,
    expandedSources,
    setExpandedSources,
}: SourcePanelSectionProps) {
    const { knowledgeBaseEnabled } = useKnowledgeBaseFeatureEnabled();
    const { isFeatureEnabled } = useFeatureToggles();
    const meta = message.metadata as AIMessageMetadata | undefined;
    const enabledDataSourceTypes = useMemo(
        () => getEnabledDataSourceTypes(isFeatureEnabled),
        [isFeatureEnabled],
    );
    const { visibleSources, showKnowledgeBaseMiss } = useMemo(
        () => getVisibleSourcePanelState(meta, {
            knowledgeBaseEnabled,
            enabledDataSourceTypes,
        }),
        [enabledDataSourceTypes, knowledgeBaseEnabled, meta],
    );

    // 延迟到回复结束后再展示“参考了 n 个来源”，避免一开始就出现
    if (isCurrentStreaming) return null;

    if (!visibleSources.length && !showKnowledgeBaseMiss) return null;

    const isExpanded = !!expandedSources[message.id];
    if (showKnowledgeBaseMiss && !isCurrentStreaming) {
        return (
            <div className="mt-3 border-t border-border/50 pt-2 px-2 text-[10px] font-bold uppercase tracking-wider text-foreground-secondary">
                本次未命中知识库
            </div>
        );
    }
    return (
        <SourcePanel
            sources={visibleSources as InjectedSource[]}
            isExpanded={isExpanded}
            onToggle={() => setExpandedSources(prev => ({ ...prev, [message.id]: !isExpanded }))}
        />
    );
}

// AI 消息操作按钮
interface AIMessageActionsProps {
    message: ChatMessage;
    disabled: boolean;
    copiedId: string | null;
    hoveredAction: string | null;
    onCopy: () => void;
    onRegenerateResponse?: (messageId: string) => void;
    onArchiveMessage?: (message: ChatMessage) => void;
    setHoveredAction: (action: string | null) => void;
}

function AIMessageActions({
    message,
    disabled,
    copiedId,
    hoveredAction,
    onCopy,
    onRegenerateResponse,
    onArchiveMessage,
    setHoveredAction,
}: AIMessageActionsProps) {
    const { knowledgeBaseEnabled } = useKnowledgeBaseFeatureEnabled();
    const resolvedModelName = message.modelName || resolveClientModelName(message.model || '', message.model || '');

    return (
        <div className="flex gap-1 mt-3">
            <button
                onClick={onCopy}
                onMouseEnter={() => setHoveredAction(`copy-${message.id}`)}
                onMouseLeave={() => setHoveredAction(null)}
                className="relative p-1.5 text-foreground-secondary hover:text-foreground hover:bg-background-secondary rounded-md transition-all duration-150"
            >
                {copiedId === message.id ? (
                    <Check className="w-4 h-4 text-green-600" />
                ) : (
                    <Copy className="w-4 h-4" />
                )}
                {hoveredAction === `copy-${message.id}` && (
                    <span className="absolute top-full mt-2 left-1/2 -translate-x-1/2 px-2 py-1 text-[10px] font-bold bg-foreground text-background rounded shadow-md whitespace-nowrap z-10 uppercase tracking-wider">
                        {copiedId === message.id ? '已复制' : '复制'}
                    </span>
                )}
            </button>
            {!disabled && onRegenerateResponse && (
                <button
                    onClick={() => onRegenerateResponse(message.id)}
                    onMouseEnter={() => setHoveredAction(`regen-${message.id}`)}
                    onMouseLeave={() => setHoveredAction(null)}
                    className="relative p-1.5 text-foreground-secondary hover:text-foreground hover:bg-background-secondary rounded-md transition-all duration-150"
                >
                    <RefreshCw className="w-4 h-4" />
                    {hoveredAction === `regen-${message.id}` && (
                        <span className="absolute top-full mt-2 left-1/2 -translate-x-1/2 px-3 py-2 text-[10px] font-bold bg-foreground text-background rounded shadow-md whitespace-nowrap z-10 uppercase tracking-widest leading-tight">
                            <div>重新生成</div>
                            {resolvedModelName && (
                                <div className="text-background/70 mt-1 lowercase font-medium">{resolvedModelName}</div>
                            )}
                        </span>
                    )}
                </button>
            )}
            {knowledgeBaseEnabled && !!onArchiveMessage && (
                <button
                    onClick={() => onArchiveMessage(message)}
                    onMouseEnter={() => setHoveredAction(`archive-${message.id}`)}
                    onMouseLeave={() => setHoveredAction(null)}
                    className="relative p-1.5 text-foreground-secondary hover:text-foreground hover:bg-background-secondary rounded-md transition-all duration-150"
                >
                    <BookOpenText className="w-4 h-4" />
                    {hoveredAction === `archive-${message.id}` && (
                        <span className="absolute top-full mt-2 left-1/2 -translate-x-1/2 px-2 py-1 text-[10px] font-bold bg-foreground text-background rounded shadow-md whitespace-nowrap z-10 uppercase tracking-wider">
                            加入知识库
                        </span>
                    )}
                </button>
            )}
            {/* 命盘信息显示 */}
            {(message.chartInfo?.baziName || message.chartInfo?.ziweiName) && (
                <div className="flex items-center gap-2 ml-2 text-[10px] font-bold uppercase tracking-widest text-foreground-secondary">
                    <span className="opacity-60">|</span>
                    {message.chartInfo.baziName && (
                        <span className="flex items-center gap-1 px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-600 dark:text-amber-400">
                            八字: {message.chartInfo.baziName}
                        </span>
                    )}
                    {message.chartInfo.ziweiName && (
                        <span className="flex items-center gap-1 px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-600 dark:text-purple-400">
                            紫薇: {message.chartInfo.ziweiName}
                        </span>
                    )}
                </div>
            )}
        </div>
    );
}
