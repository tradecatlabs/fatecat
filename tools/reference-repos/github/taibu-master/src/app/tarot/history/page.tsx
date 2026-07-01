/**
 * 塔罗历史记录页面 - 使用 HistoryPageTemplate
 */
'use client';

import { Sparkles, Calendar } from 'lucide-react';
import { HistoryPageTemplate, type CardActions } from '@/components/history/HistoryPageTemplate';
import type { HistorySummaryItem } from '@/lib/history/registry';

function TarotCard({ item, actions }: { item: HistorySummaryItem; actions: CardActions }) {
    return (
        <div
            className="group relative bg-background-secondary rounded-2xl p-5 border border-border hover:border-purple-500/30 hover:shadow-lg hover:shadow-purple-500/5 transition-all duration-300 cursor-pointer flex flex-col"
            onClick={actions.onView}
        >
            <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                    <span className="px-2.5 py-1 text-xs font-medium rounded-lg bg-purple-500/10 text-purple-500 border border-purple-500/10">
                        {item.title}
                    </span>
                    {item.modelName && (
                        <span className="px-2 py-0.5 text-[10px] rounded-md bg-background text-foreground-secondary border border-border">
                            {item.modelName}
                        </span>
                    )}
                </div>
                <span className="text-xs text-foreground-tertiary font-mono">{actions.formatDate(item.createdAt)}</span>
            </div>
            <div className="mb-3">
                <div className="flex flex-wrap gap-1.5">
                    {(item.badges || []).slice(0, 3).map((badge, i) => (
                        <div key={i} className={`px-2 py-1 text-xs rounded-md border ${badge.includes('(逆)') ? 'bg-rose-500/5 border-rose-500/20 text-rose-500' : 'bg-emerald-500/5 border-emerald-500/20 text-emerald-500'}`}>
                            {badge}
                        </div>
                    ))}
                    {(item.badges || []).length > 3 && (
                        <span className="px-2 py-1 text-xs rounded-md bg-background border border-border text-foreground-secondary">+{(item.badges || []).length - 3}</span>
                    )}
                </div>
            </div>
            <div className="flex-1">
                {item.question && <p className="text-xs text-foreground-secondary line-clamp-2">{item.question}</p>}
            </div>
            <div className="pt-3 mt-auto border-t border-border flex items-center justify-between opacity-60 group-hover:opacity-100 transition-opacity">
                <div className="text-xs text-foreground-secondary flex items-center gap-1"><Calendar className="w-3 h-3" />查看详情</div>
                <HistoryCardActions actions={actions} />
            </div>
        </div>
    );
}

function HistoryCardActions({ actions }: { actions: CardActions }) {
    return (
        <div className="flex items-center gap-1">
            {actions.canAddToKnowledgeBase && (
                <button type="button" onClick={e => { e.stopPropagation(); actions.onAddToKb(); }}
                    className="p-1.5 rounded-lg hover:bg-emerald-500/10 text-foreground-secondary hover:text-emerald-500 transition-colors" title="加入知识库">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                </button>
            )}
            <button type="button" onClick={e => { e.stopPropagation(); actions.onDelete(); }}
                className="p-1.5 rounded-lg hover:bg-red-500/10 text-foreground-secondary hover:text-red-500 transition-colors" title="删除">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
            </button>
        </div>
    );
}

export default function TarotHistoryPage() {
    return (
        <HistoryPageTemplate
            sourceType="tarot"
            title="塔罗占卜历史"
            subtitle="回顾你的心灵指引记录"
            icon={Sparkles}
            iconColor="text-purple-500"
            searchPlaceholder="搜索问题或牌阵..."
            emptyActionLabel="开始新的占卜"
            deleteMessage="确定要删除这条占卜记录吗？此操作无法撤销。"
            kbSourceType="tarot_reading"
            themeColor="purple-500"
            invalidateTypes={['tarot_reading']}
            kbTitleFn={item => item.question || `塔罗 - ${item.title}`}
            filterFn={(item, query) => {
                const q = query.toLowerCase();
                return !!(item.question?.toLowerCase().includes(q))
                    || item.title.toLowerCase().includes(q)
                    || (item.badges || []).join(' ').toLowerCase().includes(q);
            }}
            renderCard={(item, actions) => <TarotCard item={item} actions={actions} />}
        />
    );
}
