/**
 * 历史页面通用模板
 *
 * 封装: loadHistorySummariesPage, deleteHistorySummary, 搜索过滤, 删除确认弹窗, KB 模态框
 * 各历史页面只需提供配置即可复用全部逻辑。
 *
 * 'use client' - 需要 useState/useEffect/useRouter
 */
'use client';

import { useState, useEffect, useCallback, useRef, type ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Calendar, Trash2, Search, BookOpenText, MessageSquare } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { AddToKnowledgeBaseModal } from '@/components/knowledge-base/AddToKnowledgeBaseModal';
import { useKnowledgeBaseFeatureEnabled } from '@/components/knowledge-base/useKnowledgeBaseFeatureEnabled';
import { useSessionSafe } from '@/components/providers/ClientProviders';
import { ConfirmDeleteModal } from '@/components/common/ConfirmDeleteModal';
import { useToast } from '@/components/ui/Toast';
import {
    DATA_INDEX_INVALIDATED_EVENT,
    HISTORY_SUMMARY_DELETED_EVENT,
    KNOWLEDGE_BASE_SYNC_EVENT,
} from '@/lib/browser-api';
import {
    applyHistoryRestorePayload,
    deleteHistorySummary,
    loadHistoryRestore,
    loadHistorySummariesPage,
} from '@/lib/history/client';
import type { HistorySummaryItem, HistoryType } from '@/lib/history/registry';

/* ---------- 公共 formatDate ---------- */
function formatDate(dateStr: string): string {
    return new Date(dateStr).toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
    });
}

/* ---------- 类型定义 ---------- */
export type HistoryLayout = 'list' | 'grid';

export interface HistoryPageConfig {
    /** 历史类型 key */
    sourceType: HistoryType;
    /** 页面标题 */
    title: string;
    /** 副标题 */
    subtitle?: string;
    /** 标题图标 */
    icon?: LucideIcon;
    /** 图标颜色 class */
    iconColor?: string;
    /** 搜索框 placeholder */
    searchPlaceholder?: string;
    /** 空状态文案 */
    emptyMessage?: string;
    /** 空状态搜索无结果文案 */
    emptySearchMessage?: string;
    /** 空状态 CTA 文案 */
    emptyActionLabel?: string;
    /** 空状态 CTA 链接 */
    emptyActionHref?: string;
    /** 删除确认文案 */
    deleteMessage?: string;
    /** KB sourceType (默认与 sourceType 相同) */
    kbSourceType?: string;
    /** 布局模式 */
    layout?: HistoryLayout;
    /** 骨架屏数量 */
    skeletonCount?: number;
    /** 主题色 class (用于 hover border 等) */
    themeColor?: string;
    /** 自定义搜索过滤 */
    filterFn?: (item: HistorySummaryItem, query: string) => boolean;
    /** 自定义 KB 标题 */
    kbTitleFn?: (item: HistorySummaryItem) => string;
    /** 自定义卡片渲染 */
    renderCard?: (item: HistorySummaryItem, actions: CardActions) => ReactNode;
    /** loadHistoryRestore 的额外参数 (如 timezone) */
    restoreTimezone?: string;
    /** 数据变更时的 invalidate types */
    invalidateTypes?: string[];
}

export interface CardActions {
    onView: () => void;
    onDelete: () => void;
    onAddToKb: () => void;
    canAddToKnowledgeBase: boolean;
    formatDate: (dateStr: string) => string;
}

const HISTORY_PAGE_BATCH_SIZE = 12;

function mergeHistoryItems(current: HistorySummaryItem[], incoming: HistorySummaryItem[]) {
    if (incoming.length === 0) {
        return current;
    }

    const merged = new Map(current.map((item) => [item.id, item] as const));
    for (const item of incoming) {
        merged.set(item.id, item);
    }
    return Array.from(merged.values());
}

const HISTORY_THEME_STYLES: Record<string, {
    cardBorder: string;
    badge: string;
}> = {
    accent: {
        cardBorder: 'hover:border-accent/30',
        badge: 'bg-accent/10 text-accent border-accent/10',
    },
    'amber-500': {
        cardBorder: 'hover:border-amber-500/30',
        badge: 'bg-amber-500/10 text-amber-500 border-amber-500/10',
    },
    'indigo-500': {
        cardBorder: 'hover:border-indigo-500/30',
        badge: 'bg-indigo-500/10 text-indigo-500 border-indigo-500/10',
    },
    'purple-500': {
        cardBorder: 'hover:border-purple-500/30',
        badge: 'bg-purple-500/10 text-purple-500 border-purple-500/10',
    },
    'emerald-500': {
        cardBorder: 'hover:border-emerald-500/30',
        badge: 'bg-emerald-500/10 text-emerald-500 border-emerald-500/10',
    },
    'rose-500': {
        cardBorder: 'hover:border-rose-500/30',
        badge: 'bg-rose-500/10 text-rose-500 border-rose-500/10',
    },
    'cyan-500': {
        cardBorder: 'hover:border-cyan-500/30',
        badge: 'bg-cyan-500/10 text-cyan-500 border-cyan-500/10',
    },
};

function resolveHistoryTheme(themeColor: string) {
    return HISTORY_THEME_STYLES[themeColor] || HISTORY_THEME_STYLES.accent;
}

/* ---------- 默认卡片 (grid 布局) ---------- */
function DefaultGridCard({ item, actions, themeColor }: { item: HistorySummaryItem; actions: CardActions; themeColor: string }) {
    const theme = resolveHistoryTheme(themeColor);
    return (
        <div
            className={`group relative bg-background-secondary rounded-2xl p-5 border border-border ${theme.cardBorder} hover:shadow-lg transition-all duration-300 cursor-pointer flex flex-col`}
            onClick={actions.onView}
        >
            <div className="flex items-center justify-between mb-3">
                <span className={`px-2.5 py-1 text-xs font-medium rounded-lg border ${theme.badge}`}>
                    {item.title}
                </span>
                <span className="text-xs text-foreground-tertiary font-mono">
                    {actions.formatDate(item.createdAt)}
                </span>
            </div>
            {item.modelName && (
                <div className="mb-3">
                    <span className="text-[10px] text-foreground-secondary px-2 py-0.5 rounded-md bg-background border border-border inline-block">
                        {item.modelName}
                    </span>
                </div>
            )}
            <div className="flex-1">
                {item.question && <p className="text-xs text-foreground-secondary line-clamp-2">{item.question}</p>}
            </div>
            <div className="pt-3 mt-4 border-t border-border flex items-center justify-between opacity-60 group-hover:opacity-100 transition-opacity">
                <div className="text-xs text-foreground-secondary flex items-center gap-1">
                    <Calendar className="w-3 h-3" />查看详情
                </div>
                <div className="flex items-center gap-1">
                    {actions.canAddToKnowledgeBase && (
                        <button type="button" onClick={e => { e.stopPropagation(); actions.onAddToKb(); }}
                            className="p-1.5 rounded-lg hover:bg-emerald-500/10 text-foreground-secondary hover:text-emerald-500 transition-colors" title="加入知识库">
                            <BookOpenText className="w-4 h-4" />
                        </button>
                    )}
                    <button type="button" onClick={e => { e.stopPropagation(); actions.onDelete(); }}
                        className="p-1.5 rounded-lg hover:bg-red-500/10 text-foreground-secondary hover:text-red-500 transition-colors" title="删除">
                        <Trash2 className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
}

/* ---------- 默认卡片 (list 布局) ---------- */
function DefaultListCard({ item, actions, themeColor }: { item: HistorySummaryItem; actions: CardActions; themeColor: string }) {
    const theme = resolveHistoryTheme(themeColor);
    return (
        <div
            className={`bg-background-secondary rounded-xl p-4 border border-border ${theme.cardBorder} transition-colors cursor-pointer`}
            onClick={actions.onView}
        >
            <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-2">
                        <span className={`px-2 py-0.5 text-xs rounded-full border ${theme.badge}`}>
                            {item.badges?.[0] || item.title}
                        </span>
                        <div className="flex items-center gap-2 ml-auto">
                            <span className="flex items-center gap-1 text-xs text-foreground-secondary">
                                <Calendar className="w-3 h-3" />{actions.formatDate(item.createdAt)}
                            </span>
                            {item.modelName && (
                                <span className="text-xs text-foreground-secondary px-2 py-0.5 rounded bg-background">{item.modelName}</span>
                            )}
                        </div>
                    </div>
                    <p className="text-sm font-medium">{item.title}</p>
                </div>
                <div className="flex items-center gap-1">
                    {actions.canAddToKnowledgeBase && (
                        <button type="button" onClick={e => { e.stopPropagation(); actions.onAddToKb(); }}
                            className="p-2 rounded-lg hover:bg-emerald-500/10 text-foreground-secondary hover:text-emerald-500 transition-colors" title="加入知识库">
                            <BookOpenText className="w-4 h-4" />
                        </button>
                    )}
                    <button type="button" onClick={e => { e.stopPropagation(); actions.onDelete(); }}
                        className="p-2 rounded-lg hover:bg-red-500/10 text-foreground-secondary hover:text-red-500 transition-colors" title="删除">
                        <Trash2 className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
}

/* ---------- 骨架屏 ---------- */
function SkeletonGrid({ count }: { count: number }) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Array.from({ length: count }, (_, i) => (
                <div key={i} className="bg-background-secondary rounded-2xl p-5 border border-border">
                    <div className="flex items-center justify-between mb-3">
                        <div className="h-6 w-20 rounded-lg bg-foreground/10 animate-pulse" />
                        <div className="h-4 w-24 rounded bg-foreground/5 animate-pulse" />
                    </div>
                    <div className="h-3 w-full rounded bg-foreground/5 animate-pulse mb-2" />
                    <div className="h-3 w-2/3 rounded bg-foreground/5 animate-pulse" />
                    <div className="pt-3 mt-4 border-t border-border flex justify-between">
                        <div className="h-3 w-16 rounded bg-foreground/5 animate-pulse" />
                        <div className="flex gap-1">
                            <div className="w-7 h-7 rounded-lg bg-foreground/5 animate-pulse" />
                            <div className="w-7 h-7 rounded-lg bg-foreground/5 animate-pulse" />
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}

function SkeletonList({ count }: { count: number }) {
    return (
        <div className="space-y-3">
            {Array.from({ length: count }, (_, i) => (
                <div key={i} className="bg-background-secondary rounded-xl p-4 border border-border">
                    <div className="flex items-start justify-between gap-4">
                        <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-2">
                                <div className="h-5 w-20 rounded-full bg-foreground/10 animate-pulse" />
                                <div className="ml-auto h-4 w-28 rounded bg-foreground/5 animate-pulse" />
                            </div>
                            <div className="h-5 w-32 rounded bg-foreground/10 animate-pulse" />
                        </div>
                        <div className="flex items-center gap-1">
                            <div className="w-8 h-8 rounded-lg bg-foreground/5 animate-pulse" />
                            <div className="w-8 h-8 rounded-lg bg-foreground/5 animate-pulse" />
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}

/* ---------- 主组件 ---------- */
export function HistoryPageTemplate(config: HistoryPageConfig) {
    const {
        sourceType, title, subtitle, icon: Icon, iconColor,
        searchPlaceholder = '搜索...', emptyMessage = '暂无历史记录',
        emptySearchMessage = '未找到匹配的记录', emptyActionLabel = '开始新的',
        emptyActionHref, deleteMessage, kbSourceType, layout = 'grid',
        skeletonCount = layout === 'grid' ? 6 : 4, themeColor = 'accent',
        filterFn, kbTitleFn, renderCard, restoreTimezone, invalidateTypes,
    } = config;

    const router = useRouter();
    const { showToast } = useToast();
    const { user, loading: sessionLoading } = useSessionSafe();
    const { knowledgeBaseEnabled } = useKnowledgeBaseFeatureEnabled();
    const [items, setItems] = useState<HistorySummaryItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [loadingMore, setLoadingMore] = useState(false);
    const [hasMore, setHasMore] = useState(false);
    const [nextOffset, setNextOffset] = useState<number | null>(null);
    const [appendError, setAppendError] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);
    const [kbModalOpen, setKbModalOpen] = useState(false);
    const [kbTarget, setKbTarget] = useState<HistorySummaryItem | null>(null);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const loadMoreSentinelRef = useRef<HTMLDivElement | null>(null);
    const appendRequestKeyRef = useRef<string | null>(null);
    const basePath = `/${sourceType}`;
    const resolvedKbSourceType = kbSourceType || `${sourceType}_reading`;

    const removeHistoryItem = useCallback((id: string) => {
        let removed = false;
        setItems((prev) => {
            const next = prev.filter((item) => item.id !== id);
            removed = next.length !== prev.length;
            return removed ? next : prev;
        });
        if (removed) {
            setNextOffset((prev) => prev == null ? null : Math.max(prev - 1, 0));
        }
        return removed;
    }, []);

    const loadItems = useCallback(async (options?: { append?: boolean; offset?: number }) => {
        if (!user?.id) {
            router.push(basePath);
            return;
        }

        const append = options?.append === true;
        const targetOffset = options?.offset ?? 0;
        const requestKey = append ? `append:${targetOffset}` : 'initial:0';
        if (append && appendRequestKeyRef.current === requestKey) {
            return;
        }
        if (append) {
            appendRequestKeyRef.current = requestKey;
            setLoadingMore(true);
            setAppendError(null);
        } else {
            setLoading(true);
        }

        try {
            const page = await loadHistorySummariesPage(sourceType, {
                limit: HISTORY_PAGE_BATCH_SIZE,
                offset: targetOffset,
            });

            setErrorMessage(null);
            setAppendError(null);
            setItems((prev) => append ? mergeHistoryItems(prev, page.items) : page.items);
            setHasMore(page.pagination.hasMore);
            setNextOffset(page.pagination.nextOffset);
        } catch (error) {
            const message = error instanceof Error ? error.message : '加载历史记录失败';
            if (append) {
                setAppendError(message);
            } else {
                setErrorMessage(message);
                setHasMore(false);
                setNextOffset(null);
                setItems([]);
            }
            showToast('error', message);
        } finally {
            if (append) {
                appendRequestKeyRef.current = null;
                setLoadingMore(false);
            } else {
                setLoading(false);
            }
        }
    }, [basePath, router, showToast, sourceType, user?.id]);

    useEffect(() => {
        if (sessionLoading) {
            return;
        }

        const timer = setTimeout(() => { void loadItems(); }, 0);
        return () => clearTimeout(timer);
    }, [loadItems, sessionLoading]);

    useEffect(() => {
        if (
            loading
            || loadingMore
            || !!appendError
            || !hasMore
            || nextOffset == null
            || !loadMoreSentinelRef.current
        ) {
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            if (entries.some((entry) => entry.isIntersecting)) {
                void loadItems({ append: true, offset: nextOffset });
            }
        }, {
            rootMargin: '160px 0px',
        });

        observer.observe(loadMoreSentinelRef.current);
        return () => observer.disconnect();
    }, [appendError, hasMore, loadItems, loading, loadingMore, nextOffset]);

    const handleDelete = async (id: string) => {
        try {
            await deleteHistorySummary(sourceType, id);
            setErrorMessage(null);
            setAppendError(null);
            removeHistoryItem(id);
            if (invalidateTypes?.length) {
                window.dispatchEvent(new CustomEvent(DATA_INDEX_INVALIDATED_EVENT, { detail: { types: invalidateTypes } }));
            }
        } catch (error) {
            const message = error instanceof Error ? error.message : '删除历史记录失败';
            setErrorMessage(message);
            showToast('error', message);
        } finally {
            setDeleteConfirmId(null);
        }
    };

    const handleView = async (item: HistorySummaryItem) => {
        try {
            const payload = await loadHistoryRestore(sourceType, item.id, restoreTimezone);
            if (!payload) {
                throw new Error('未找到历史记录');
            }
            setErrorMessage(null);
            router.push(applyHistoryRestorePayload(payload));
        } catch (error) {
            const message = error instanceof Error ? error.message : '加载历史记录失败';
            setErrorMessage(message);
            showToast('error', message);
        }
    };

    const defaultFilter = (item: HistorySummaryItem, query: string) => {
        const q = query.toLowerCase();
        return (item.title || '').toLowerCase().includes(q)
            || (item.question || '').toLowerCase().includes(q)
            || (item.badges || []).join(' ').toLowerCase().includes(q);
    };

    const filteredItems = items.filter(item => {
        if (!searchQuery.trim()) return true;
        return (filterFn || defaultFilter)(item, searchQuery);
    });

    useEffect(() => {
        if (
            !searchQuery.trim()
            || loading
            || loadingMore
            || !!appendError
            || !hasMore
            || nextOffset == null
            || filteredItems.length > 0
        ) {
            return;
        }

        void loadItems({ append: true, offset: nextOffset });
    }, [appendError, filteredItems.length, hasMore, loadItems, loading, loadingMore, nextOffset, searchQuery]);

    useEffect(() => {
        if (typeof window === 'undefined') {
            return;
        }

        const handleHistorySummaryDeleted = (event: Event) => {
            const detail = (event as CustomEvent<{ type?: string | null; id?: string | null }>).detail;
            if (detail?.type !== sourceType || !detail.id) {
                return;
            }
            removeHistoryItem(detail.id);
        };

        const handleArchiveChanged = (event: Event) => {
            const detail = (event as CustomEvent<{
                pathname?: string;
                requestBody?: Record<string, unknown> | null;
                responseData?: Record<string, unknown> | null;
            }>).detail;
            const pathname = detail?.pathname ?? '';
            const isArchiveMutation = pathname.startsWith('/api/knowledge-base/archive');
            const kbSourceType = detail?.pathname?.startsWith('/api/knowledge-base/ingest')
                ? detail.requestBody?.sourceType
                : detail?.responseData?.sourceType;
            if (!isArchiveMutation && kbSourceType !== resolvedKbSourceType) {
                return;
            }
            void loadItems();
        };

        window.addEventListener(HISTORY_SUMMARY_DELETED_EVENT, handleHistorySummaryDeleted as EventListener);
        window.addEventListener(KNOWLEDGE_BASE_SYNC_EVENT, handleArchiveChanged as EventListener);
        return () => {
            window.removeEventListener(HISTORY_SUMMARY_DELETED_EVENT, handleHistorySummaryDeleted as EventListener);
            window.removeEventListener(KNOWLEDGE_BASE_SYNC_EVENT, handleArchiveChanged as EventListener);
        };
    }, [loadItems, removeHistoryItem, resolvedKbSourceType, sourceType]);

    const makeActions = (item: HistorySummaryItem): CardActions => ({
        onView: () => void handleView(item),
        onDelete: () => setDeleteConfirmId(item.id),
        onAddToKb: () => {
            if (!knowledgeBaseEnabled) return;
            setKbTarget(item);
            setKbModalOpen(true);
        },
        canAddToKnowledgeBase: knowledgeBaseEnabled,
        formatDate,
    });

    const resolvedEmptyHref = emptyActionHref || basePath;

    return (
        <div className="min-h-screen bg-background">
            <div className={`${layout === 'grid' ? 'max-w-6xl' : 'max-w-4xl'} mx-auto px-4 py-4 md:py-8`}>
                <div className="hidden md:flex items-center justify-between gap-4 mb-8">
                    <div>
                        <h1 className="text-2xl font-bold flex items-center gap-2">
                            {Icon && <Icon className={`w-6 h-6 ${iconColor || ''}`} />}
                            {title}
                        </h1>
                        {subtitle && <p className="text-foreground-secondary text-sm mt-1">{subtitle}</p>}
                    </div>
                </div>

                <div className="flex items-center gap-3 mb-6 bg-background-secondary/50 p-2 rounded-2xl border border-border">
                    <div className="relative flex-1">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground-secondary" />
                        <input type="text" value={searchQuery} onChange={e => setSearchQuery(e.target.value)}
                            placeholder={searchPlaceholder}
                            className="w-full pl-9 pr-4 py-2 rounded-xl bg-background border-none focus:outline-none focus:ring-2 focus:ring-accent/20 text-sm placeholder:text-foreground-tertiary" />
                    </div>
                </div>

                {errorMessage && !loading && (
                    <div className="mb-6 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
                        {errorMessage}
                    </div>
                )}

                {loading ? (
                    layout === 'grid' ? <SkeletonGrid count={skeletonCount} /> : <SkeletonList count={skeletonCount} />
                ) : errorMessage && filteredItems.length === 0 ? (
                    <div className="flex flex-col items-center justify-center gap-4 py-20 bg-background-secondary/30 rounded-3xl border border-red-200 border-dashed">
                        <div className="text-sm text-red-600">{errorMessage}</div>
                        <button
                            type="button"
                            onClick={() => { void loadItems(); }}
                            className="px-5 py-2 rounded-xl bg-accent text-white hover:bg-accent/90 transition-colors text-sm font-medium"
                        >
                            重试
                        </button>
                    </div>
                ) : filteredItems.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-20 bg-background-secondary/30 rounded-3xl border border-border border-dashed">
                        <div className="w-16 h-16 rounded-full bg-background-secondary flex items-center justify-center mb-4">
                            <MessageSquare className="w-8 h-8 text-foreground-tertiary" />
                        </div>
                        <h3 className="text-lg font-medium mb-1">{searchQuery ? emptySearchMessage : emptyMessage}</h3>
                        {!searchQuery && (
                            <Link href={resolvedEmptyHref}
                                className="mt-6 px-6 py-2.5 bg-accent text-white rounded-xl hover:bg-accent/90 transition-all shadow-lg shadow-accent/20 font-medium text-sm">
                                {emptyActionLabel}
                            </Link>
                        )}
                    </div>
                ) : layout === 'grid' ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {filteredItems.map(item => {
                            const actions = makeActions(item);
                            return renderCard
                                ? <div key={item.id}>{renderCard(item, actions)}</div>
                                : <DefaultGridCard key={item.id} item={item} actions={actions} themeColor={themeColor} />;
                        })}
                    </div>
                ) : (
                    <div className="space-y-3">
                        {filteredItems.map(item => {
                            const actions = makeActions(item);
                            return renderCard
                                ? <div key={item.id}>{renderCard(item, actions)}</div>
                                : <DefaultListCard key={item.id} item={item} actions={actions} themeColor={themeColor} />;
                        })}
                    </div>
                )}

                {!loading && hasMore && (
                    <div ref={loadMoreSentinelRef} className="mt-8 py-4 flex justify-center">
                        {loadingMore ? (
                            <div className="flex items-center gap-2 text-sm text-foreground-secondary">
                                <SoundWaveLoader variant="inline" />
                            </div>
                        ) : appendError ? (
                            <button
                                type="button"
                                onClick={() => { void loadItems({ append: true, offset: nextOffset ?? 0 }); }}
                                className="rounded-xl border border-border px-4 py-2 text-sm text-foreground-secondary transition-colors hover:bg-background-secondary"
                            >
                                重试加载更多
                            </button>
                        ) : (
                            <div className="text-sm text-foreground-secondary">
                                继续下滑加载更多
                            </div>
                        )}
                    </div>
                )}
            </div>

            <ConfirmDeleteModal open={!!deleteConfirmId} onClose={() => setDeleteConfirmId(null)}
                onConfirm={() => deleteConfirmId && handleDelete(deleteConfirmId)} message={deleteMessage} />

            {knowledgeBaseEnabled && kbTarget && (
                <AddToKnowledgeBaseModal open={kbModalOpen}
                    onClose={() => { setKbModalOpen(false); setKbTarget(null); }}
                    sourceTitle={kbTitleFn ? kbTitleFn(kbTarget) : kbTarget.question || kbTarget.title}
                    sourceType={resolvedKbSourceType} sourceId={kbTarget.id} />
            )}
        </div>
    );
}
