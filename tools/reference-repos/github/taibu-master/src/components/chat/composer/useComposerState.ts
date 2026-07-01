/**
 * ChatComposer 共享状态 hook
 *
 * 集中管理 ChatComposer 内部的 22 个 useState，
 * 按职责分组导出给各子组件使用。
 */
import { useState, useRef, useMemo, useCallback, useEffect } from 'react';
import type { Mention, PromptLayerDiagnostic } from '@/types';
import type { MembershipType } from '@/lib/user/membership';
import { DEFAULT_MODEL_ID } from '@/lib/ai/ai-config';
import { DATA_INDEX_INVALIDATED_EVENT } from '@/lib/browser-api';
import { readLocalCache, removeLocalCache, writeLocalCache } from '@/lib/cache/local-storage';
import { shouldRequestChatPreview } from '@/lib/chat/chat-preview';
import { formatPromptLayerLabel } from '@/lib/chat/prompt-labels';
import { mentionTypeLabels } from '@/components/chat/mentionStyles';
import {
    listKnowledgeBases,
    type KnowledgeBaseSummary as BrowserKnowledgeBaseSummary,
} from '@/lib/knowledge-base/browser-client';
import type { DataSourceType, DataSourceSummary, DataSourceLoadError } from '@/lib/data-sources/types';
import { filterMentionsByFeature } from '@/lib/data-sources/catalog';
import type { ChatMode } from '@/lib/chat/use-chat-state';

export type KnowledgeBaseSummary =
    Pick<BrowserKnowledgeBaseSummary, 'id' | 'name' | 'description'>
    & Partial<Omit<BrowserKnowledgeBaseSummary, 'id' | 'name' | 'description'>>;

/** 缓存 TTL：10 分钟 */
const MENTION_CACHE_TTL_MS = 10 * 60 * 1000;

function getMentionCacheKeys(userId: string) {
    return {
        dataKey: `taibu.data_sources.${userId}.v1`,
        legacyDataKey: `mingai.data_sources.${userId}.v1`,
        kbKey: `taibu.knowledge_bases.${userId}.v1`,
        legacyKbKey: `mingai.knowledge_bases.${userId}.v1`,
    };
}

export interface UseComposerStateOptions {
    userId?: string | null;
    membershipType?: MembershipType;
    selectedModel?: string;
    reasoningEnabled?: boolean;
    mentions?: Mention[];
    contextMessages?: Array<{ content?: string }>;
    isLoading: boolean;
    isSendingToList?: boolean;
    chatMode?: ChatMode;
    knowledgeBaseEnabled?: boolean;
    promptKnowledgeBases?: KnowledgeBaseSummary[];
    enabledDataSourceTypes?: readonly DataSourceType[];
}

export function useComposerState(opts: UseComposerStateOptions) {
    const {
        userId,
        membershipType = 'free',
        selectedModel = DEFAULT_MODEL_ID,
        reasoningEnabled = false,
        mentions = [],
        contextMessages = [],
        isLoading,
        isSendingToList = false,
        chatMode = 'normal',
        knowledgeBaseEnabled = true,
        promptKnowledgeBases = [],
        enabledDataSourceTypes = [],
    } = opts;

    // --- Refs ---
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const overlayRef = useRef<HTMLDivElement>(null);
    const previewRequestIdRef = useRef(0);

    // --- Menu state ---
    const [menuOpen, setMenuOpen] = useState(false);

    // --- Mention state ---
    const [mentionOpen, setMentionOpen] = useState(false);
    const [mentionQuery, setMentionQuery] = useState('');
    const [mentionStartIndex, setMentionStartIndex] = useState<number | null>(null);
    const [mentionDataSources, setMentionDataSources] = useState<DataSourceSummary[]>([]);
    const [mentionKnowledgeBases, setMentionKnowledgeBases] = useState<KnowledgeBaseSummary[]>([]);
    const [mentionLoadError, setMentionLoadError] = useState<string | null>(null);
    const [mentionDataSourceErrors, setMentionDataSourceErrors] = useState<DataSourceLoadError[]>([]);
    const [mentionLoading, setMentionLoading] = useState(false);
    const [mentionDefaultCategory, setMentionDefaultCategory] = useState<'knowledge' | 'data' | null>(null);

    // --- Knowledge base state ---
    const [knowledgeBaseOpen, setKnowledgeBaseOpen] = useState(false);
    const [knowledgeBaseSavingId, setKnowledgeBaseSavingId] = useState<string | null>(null);

    // --- Prompt preview state ---
    const [promptPreviewTokens, setPromptPreviewTokens] = useState(0);
    const [promptPreviewBudget, setPromptPreviewBudget] = useState(0);
    const [promptPreviewLoading, setPromptPreviewLoading] = useState(false);
    const [promptPreviewLayers, setPromptPreviewLayers] = useState<PromptLayerDiagnostic[]>([]);
    const [promptHistoryTokens, setPromptHistoryTokens] = useState(0);
    const [promptContextTotal, setPromptContextTotal] = useState(0);
    const [promptDiagnosticsOpen, setPromptDiagnosticsOpen] = useState(false);
    const [promptPreviewUserTokens, setPromptPreviewUserTokens] = useState(0);

    // --- Derived values ---
    const canUseWeb = membershipType !== 'free';
    const canUseBoth = membershipType === 'pro';
    const canUseKnowledgeBase = membershipType !== 'free' && knowledgeBaseEnabled;
    const canMentionDataSources = enabledDataSourceTypes.length > 0;
    const canMentionAnything = canMentionDataSources || canUseKnowledgeBase;

    const promptUsageProgress = promptPreviewBudget > 0
        ? Math.min(promptPreviewTokens / promptPreviewBudget, 1)
        : 0;
    const contextProgress = promptContextTotal > 0
        ? Math.min(promptHistoryTokens / promptContextTotal, 1)
        : 0;
    const promptProgressPercent = Math.round(promptUsageProgress * 100);
    const contextProgressPercent = Math.round(contextProgress * 100);
    const hasPromptDiagnostics = !!(promptPreviewLayers.length && promptPreviewBudget);
    const displayLayers = promptPreviewLayers;
    const displayUserMessageTokens = promptPreviewUserTokens;
    const promptUsageLabel = `提示词 ${promptProgressPercent}%`;

    const previewMentions = useMemo(
        () => filterMentionsByFeature(mentions, { knowledgeBaseEnabled: canUseKnowledgeBase, enabledDataSourceTypes }),
        [canUseKnowledgeBase, enabledDataSourceTypes, mentions]
    );
    const canRequestPreview = shouldRequestChatPreview({ userId, isLoading, isSendingToList });
    const promptKbIdSet = useMemo(() => new Set(promptKnowledgeBases.map(kb => kb.id)), [promptKnowledgeBases]);
    const mentionMap = useMemo(() => new Map(mentions.map(m => [m.id, m])), [mentions]);
    const kbNameMap = useMemo(() => new Map(promptKnowledgeBases.map(kb => [kb.id, kb.name])), [promptKnowledgeBases]);

    // --- Helpers ---
    const formatLayerLabel = useCallback((layerId: string) => {
        return formatPromptLayerLabel(layerId, (id) => {
            if (id.startsWith('mention_')) {
                const mentionId = id.replace('mention_', '');
                const mention = mentionMap.get(mentionId);
                if (!mention) return undefined;
                const typeLabel = mentionTypeLabels[mention.type] || mentionTypeLabels.default;
                return `提及·${typeLabel}${mention.name ? `·${mention.name}` : ''}`;
            }
            if (id.startsWith('kb_')) {
                const kbId = id.replace('kb_', '');
                const kbName = kbNameMap.get(kbId);
                return `知识库${kbName ? `·${kbName}` : ''}`;
            }
            return undefined;
        });
    }, [kbNameMap, mentionMap]);

    const readMentionCache = useCallback(<T,>(key: string): T | null => {
        return readLocalCache<T>(key, MENTION_CACHE_TTL_MS);
    }, []);

    const writeMentionCache = useCallback(<T,>(key: string, value: T) => {
        writeLocalCache(key, value);
    }, []);

    const refreshMentionData = useCallback(async (fresh = false) => {
        if (!userId) return;
        if (!canMentionAnything) {
            setMentionDataSources([]);
            setMentionKnowledgeBases([]);
            setMentionDataSourceErrors([]);
            setMentionLoadError(null);
            setMentionLoading(false);
            return;
        }
        const { dataKey, kbKey, legacyDataKey, legacyKbKey } = getMentionCacheKeys(userId);
        try {
            setMentionLoading(true);
            removeLocalCache(legacyDataKey);
            removeLocalCache(legacyKbKey);
            const [dsResp, kbResp] = await Promise.all([
                canMentionDataSources
                    ? fetch(`/api/data-sources?limit=50${fresh ? '&fresh=1' : ''}`)
                    : Promise.resolve(null),
                canUseKnowledgeBase
                    ? listKnowledgeBases()
                    : Promise.resolve(null)
            ]);

            setMentionLoadError(null);

            if (dsResp?.ok) {
                const ds = await dsResp.json() as { items?: DataSourceSummary[]; errors?: DataSourceLoadError[] };
                const items = ds.items || [];
                const errors = ds.errors || [];
                setMentionDataSources(items);
                setMentionDataSourceErrors(errors);
                writeMentionCache(dataKey, { items, errors });
            } else if (dsResp) {
                setMentionLoadError('数据加载失败');
            } else {
                setMentionDataSources([]);
                setMentionDataSourceErrors([]);
            }

            if (Array.isArray(kbResp)) {
                setMentionKnowledgeBases(kbResp);
                writeMentionCache(kbKey, kbResp);
            } else {
                setMentionKnowledgeBases([]);
            }
        } catch {
            setMentionLoadError('数据加载失败');
        } finally {
            setMentionLoading(false);
        }
    }, [canMentionAnything, canMentionDataSources, canUseKnowledgeBase, userId, writeMentionCache]);

    // --- Effects ---
    // Prompt preview fetch
    useEffect(() => {
        if (!userId) {
            setPromptPreviewTokens(0);
            setPromptPreviewBudget(0);
            setPromptPreviewLayers([]);
            setPromptPreviewUserTokens(0);
            setPromptHistoryTokens(0);
            setPromptContextTotal(0);
            setPromptPreviewLoading(false);
            return;
        }
        if (!canRequestPreview) {
            setPromptPreviewLoading(false);
            return;
        }

        const requestId = previewRequestIdRef.current + 1;
        previewRequestIdRef.current = requestId;
        const abortController = new AbortController();

        const loadPreview = async () => {
            setPromptPreviewLoading(true);
            try {
                const resp = await fetch('/api/chat/preview', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        model: selectedModel,
                        reasoning: reasoningEnabled,
                        mentions: previewMentions,
                        messages: contextMessages,
                        mangpaiMode: chatMode === 'mangpai' || undefined,
                        dreamMode: chatMode === 'dream' || undefined
                    }),
                    signal: abortController.signal
                });
                if (!resp.ok || previewRequestIdRef.current !== requestId) return;
                const data = await resp.json();
                if (previewRequestIdRef.current !== requestId) return;
                setPromptPreviewTokens(data.totalTokens || 0);
                setPromptPreviewBudget(data.budgetTotal || 0);
                setPromptPreviewLayers(data.diagnostics || []);
                setPromptPreviewUserTokens(data.userMessageTokens || 0);
                setPromptHistoryTokens(data.historyTokens || 0);
                setPromptContextTotal(data.contextTotal || 0);
            } catch (error) {
                if (error instanceof DOMException && error.name === 'AbortError') {
                    return;
                }
                console.warn('加载提示词预览失败:', error);
            } finally {
                if (previewRequestIdRef.current === requestId) {
                    setPromptPreviewLoading(false);
                }
            }
        };
        void loadPreview();

        return () => {
            abortController.abort();
        };
    }, [canRequestPreview, contextMessages, chatMode, previewMentions, reasoningEnabled, selectedModel, userId]);

    // Close diagnostics when no data
    useEffect(() => {
        if (!hasPromptDiagnostics) {
            setPromptDiagnosticsOpen(false);
        }
    }, [hasPromptDiagnostics]);

    // Mention data cache + fetch
    useEffect(() => {
        if (!userId) return;

        const { dataKey, kbKey, legacyDataKey, legacyKbKey } = getMentionCacheKeys(userId);

        removeLocalCache(legacyDataKey);
        removeLocalCache(legacyKbKey);

        const cachedDs = readMentionCache<{ items: DataSourceSummary[]; errors?: DataSourceLoadError[] }>(dataKey);
        if (canMentionDataSources && cachedDs?.items) {
            queueMicrotask(() => {
                setMentionDataSources(cachedDs.items);
                setMentionDataSourceErrors(cachedDs.errors || []);
            });
        } else if (!canMentionDataSources) {
            setMentionDataSources([]);
            setMentionDataSourceErrors([]);
        }

        if (canUseKnowledgeBase) {
            const cachedKb = readMentionCache<KnowledgeBaseSummary[]>(kbKey);
            if (cachedKb) {
                queueMicrotask(() => setMentionKnowledgeBases(cachedKb));
            }
        } else {
            setMentionKnowledgeBases([]);
        }

        let cancelled = false;
        const refresh = async (fresh = false) => {
            if (cancelled) return;
            await refreshMentionData(fresh);
        };

        void refresh(false);

        const onInvalidate = () => void refresh(true);
        window.addEventListener(DATA_INDEX_INVALIDATED_EVENT, onInvalidate as EventListener);
        return () => {
            cancelled = true;
            window.removeEventListener(DATA_INDEX_INVALIDATED_EVENT, onInvalidate as EventListener);
        };
    }, [canMentionDataSources, canUseKnowledgeBase, readMentionCache, refreshMentionData, userId]);

    return {
        // Refs
        textareaRef, fileInputRef, overlayRef, previewRequestIdRef,
        // Menu
        menuOpen, setMenuOpen,
        // Mention
        mentionOpen, setMentionOpen,
        mentionQuery, setMentionQuery,
        mentionStartIndex, setMentionStartIndex,
        mentionDataSources, setMentionDataSources,
        mentionKnowledgeBases, setMentionKnowledgeBases,
        mentionLoadError, setMentionLoadError,
        mentionDataSourceErrors, setMentionDataSourceErrors,
        mentionLoading, setMentionLoading,
        mentionDefaultCategory, setMentionDefaultCategory,
        // Knowledge base
        knowledgeBaseOpen, setKnowledgeBaseOpen,
        knowledgeBaseSavingId, setKnowledgeBaseSavingId,
        // Prompt preview
        promptPreviewTokens, setPromptPreviewTokens,
        promptPreviewBudget, setPromptPreviewBudget,
        promptPreviewLoading, setPromptPreviewLoading,
        promptPreviewLayers, setPromptPreviewLayers,
        promptHistoryTokens, setPromptHistoryTokens,
        promptContextTotal, setPromptContextTotal,
        promptDiagnosticsOpen, setPromptDiagnosticsOpen,
        promptPreviewUserTokens, setPromptPreviewUserTokens,
        // Derived
        canUseWeb, canUseBoth, canUseKnowledgeBase,
        canMentionAnything,
        promptUsageProgress, contextProgress,
        promptProgressPercent, contextProgressPercent,
        hasPromptDiagnostics, displayLayers, displayUserMessageTokens,
        promptUsageLabel, previewMentions, canRequestPreview,
        promptKbIdSet, mentionMap, kbNameMap,
        // Helpers
        formatLayerLabel, refreshMentionData, readMentionCache,
    };
}
