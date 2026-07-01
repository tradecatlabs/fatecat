/**
 * Mention 弹出层管理组件
 *
 * 'use client' 标记说明：
 * - 需要处理用户交互事件
 */
'use client';

import { SettingsCenterLink } from '@/components/settings/SettingsCenterLink';
import { X, BookOpenText, Check, Settings } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import type { Mention } from '@/types';
import { MentionPopover } from '@/components/chat/MentionPopover';
import type { DataSourceSummary, DataSourceLoadError } from '@/lib/data-sources/types';
import type { KnowledgeBaseSummary } from '@/components/chat/composer/useComposerState';
import type { DataSourceType } from '@/lib/data-sources/types';

interface MentionManagerProps {
    userId?: string | null;
    // Mention popover
    mentionOpen: boolean;
    setMentionOpen: (open: boolean) => void;
    mentionQuery: string;
    mentionDataSources: DataSourceSummary[];
    mentionKnowledgeBases: KnowledgeBaseSummary[];
    enabledDataSourceTypes: DataSourceType[];
    mentionLoadError: string | null;
    mentionDataSourceErrors: DataSourceLoadError[];
    mentionLoading: boolean;
    mentionDefaultCategory: 'knowledge' | 'data' | null;
    setMentionDefaultCategory: (cat: 'knowledge' | 'data' | null) => void;
    canUseKnowledgeBase: boolean;
    handleSelectMention: (mention: Mention) => void;
    // Knowledge base panel
    knowledgeBaseOpen: boolean;
    setKnowledgeBaseOpen: (open: boolean) => void;
    knowledgeBaseSavingId: string | null;
    promptKbIdSet: Set<string>;
    toggleKnowledgeBaseSearch: (kbId: string) => Promise<void>;
}

export function MentionManager({
    userId,
    mentionOpen, setMentionOpen,
    mentionQuery,
    mentionDataSources, mentionKnowledgeBases,
    enabledDataSourceTypes,
    mentionLoadError, mentionDataSourceErrors,
    mentionLoading, mentionDefaultCategory, setMentionDefaultCategory,
    canUseKnowledgeBase, handleSelectMention,
    knowledgeBaseOpen, setKnowledgeBaseOpen,
    knowledgeBaseSavingId, promptKbIdSet,
    toggleKnowledgeBaseSearch,
}: MentionManagerProps) {
    return (
        <>
            {/* 知识库弹窗 */}
            {knowledgeBaseOpen && userId && (
                <>
                    <div
                        className="fixed inset-0 z-[70] bg-background/20 backdrop-blur-[1px]"
                        onClick={() => setKnowledgeBaseOpen(false)}
                    />
                    <div className="absolute bottom-full left-0 right-0 mb-4 z-[80] px-4 md:px-0">
                        <div className="bg-background border border-border shadow-2xl rounded-2xl overflow-hidden flex flex-col max-h-[60vh] w-full animate-in slide-in-from-bottom-2 fade-in duration-200">
                            <div className="flex items-center justify-between p-3 px-4 border-b border-border/50 bg-muted/30">
                                <div className="flex items-center gap-2">
                                    <div className="text-sm font-semibold">启用知识库搜索</div>
                                    <SettingsCenterLink
                                        tab="knowledge-base"
                                        className="flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
                                        onClick={() => setKnowledgeBaseOpen(false)}
                                    >
                                        <span>更多设置</span>
                                        <Settings className="w-3 h-3" />
                                    </SettingsCenterLink>
                                </div>
                                <button
                                    onClick={() => setKnowledgeBaseOpen(false)}
                                    className="p-1.5 rounded-full hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
                                >
                                    <X className="w-4 h-4" />
                                </button>
                            </div>
                            <div className="overflow-y-auto p-2 space-y-1 min-h-[120px]">
                                {mentionKnowledgeBases.length === 0 ? (
                                    <div className="flex flex-col items-center justify-center py-8 text-muted-foreground gap-2">
                                        <BookOpenText className="w-8 h-8 opacity-20" />
                                        <div className="text-sm">暂无知识库</div>
                                        <SettingsCenterLink
                                            tab="knowledge-base"
                                            className="text-xs text-primary hover:underline mt-1"
                                            onClick={() => setKnowledgeBaseOpen(false)}
                                        >
                                            去创建第一个知识库
                                        </SettingsCenterLink>
                                    </div>
                                ) : (
                                    mentionKnowledgeBases.map((kb) => {
                                        const enabled = promptKbIdSet.has(kb.id);
                                        return (
                                            <div
                                                key={kb.id}
                                                onClick={() => toggleKnowledgeBaseSearch(kb.id)}
                                                className={`
                                                    group flex items-center justify-between p-3 rounded-xl border transition-all cursor-pointer
                                                    ${enabled
                                                        ? 'bg-primary/5 border-primary/20 hover:bg-primary/10'
                                                        : 'bg-card border-border hover:border-primary/30 hover:shadow-sm'
                                                    }
                                                `}
                                            >
                                                <div className="min-w-0 flex-1 mr-3">
                                                    <div className={`text-sm font-medium truncate transition-colors ${enabled ? 'text-primary' : 'text-foreground'}`}>
                                                        {kb.name}
                                                    </div>
                                                    <div className="text-xs text-muted-foreground truncate mt-0.5">
                                                        {kb.description || '暂无描述'}
                                                    </div>
                                                </div>
                                                <div className={`
                                                    flex-shrink-0 w-5 h-5 rounded-full border flex items-center justify-center transition-all
                                                    ${enabled
                                                        ? 'bg-primary border-primary text-primary-foreground'
                                                        : 'border-muted-foreground/30 group-hover:border-primary/50'
                                                    }
                                                `}>
                                                    {enabled && !knowledgeBaseSavingId && <Check className="w-3 h-3" strokeWidth={3} />}
                                                    {knowledgeBaseSavingId === kb.id && <SoundWaveLoader variant="inline" />}
                                                </div>
                                            </div>
                                        );
                                    })
                                )}
                            </div>
                        </div>
                    </div>
                </>
            )}

            {/* Mention 弹出层 */}
            {mentionOpen && userId && (
                <>
                    <div
                        className="fixed inset-0 z-30"
                        onClick={() => setMentionOpen(false)}
                    />
                    <MentionPopover
                        query={mentionQuery}
                        dataSources={mentionDataSources}
                        knowledgeBases={mentionKnowledgeBases}
                        enabledDataSourceTypes={enabledDataSourceTypes}
                        loadError={mentionLoadError}
                        dataSourceErrors={mentionDataSourceErrors}
                        loading={mentionLoading}
                        defaultCategory={mentionDefaultCategory || undefined}
                        knowledgeBaseLocked={!canUseKnowledgeBase}
                        onSelect={handleSelectMention}
                        onClose={() => {
                            setMentionOpen(false);
                            setMentionDefaultCategory(null);
                        }}
                    />
                </>
            )}
        </>
    );
}
