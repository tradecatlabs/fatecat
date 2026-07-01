/**
 * 合盘历史记录页面 - 使用 HistoryPageTemplate
 */
'use client';

import { Heart, Briefcase, Users, Clock } from 'lucide-react';
import { HistoryPageTemplate, type CardActions } from '@/components/history/HistoryPageTemplate';
import type { HistorySummaryItem } from '@/lib/history/registry';

const TYPE_CONFIG: Record<string, { label: string; icon: typeof Heart; color: string; bg: string; border: string; badge: string }> = {
    love: { label: '情侣合盘', icon: Heart, color: 'text-rose-500', bg: 'bg-rose-500', border: 'group-hover:border-rose-500/50', badge: 'bg-rose-500/10 text-rose-500' },
    business: { label: '商业合伙', icon: Briefcase, color: 'text-blue-500', bg: 'bg-blue-500', border: 'group-hover:border-blue-500/50', badge: 'bg-blue-500/10 text-blue-500' },
    family: { label: '亲子关系', icon: Users, color: 'text-emerald-500', bg: 'bg-emerald-500', border: 'group-hover:border-emerald-500/50', badge: 'bg-emerald-500/10 text-emerald-500' },
};

function HepanCard({ item, actions }: { item: HistorySummaryItem; actions: CardActions }) {
    const chartType = item.subType === 'business' || item.subType === 'family' ? item.subType : 'love';
    const config = TYPE_CONFIG[chartType];
    const Icon = config.icon;
    const [person1Name = item.title, person2Name = ''] = (item.question || '')
        .split(/\s*&\s*/u).map(s => s.trim()).filter(Boolean);

    return (
        <div
            className={`group relative bg-background/5 backdrop-blur-md rounded-2xl p-5 border border-white/10 hover:bg-background/10 hover:shadow-xl transition-all duration-300 cursor-pointer ${config.border}`}
            onClick={actions.onView}
        >
            <div className="flex items-start gap-5">
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 ${config.bg} shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1 min-w-0 pt-1">
                    <div className="flex items-center justify-between gap-4 mb-2">
                        <h3 className="text-lg font-bold text-foreground truncate flex items-center gap-2">
                            {person1Name}<span className="text-foreground-secondary/40 text-sm font-normal">&</span>{person2Name}
                        </h3>
                        <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${config.badge}`}>{item.title || config.label}</span>
                    </div>
                    <div className="mt-4 flex items-center justify-between border-t border-white/5 pt-3">
                        <div className="flex items-center gap-3">
                            <span className="flex items-center gap-1.5 text-xs text-foreground-tertiary"><Clock className="w-3.5 h-3.5" />{actions.formatDate(item.createdAt)}</span>
                            {item.modelName && <span className="text-xs px-2 py-0.5 rounded-md bg-background/5 text-foreground-secondary border border-white/5">{item.modelName}</span>}
                        </div>
                        {item.metric && (
                            <div className="flex items-center gap-2">
                                <span className="text-sm text-foreground-secondary">契合度</span>
                                <span className={`text-lg font-bold ${config.color}`}>{item.metric}</span>
                            </div>
                        )}
                    </div>
                </div>
                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    {actions.canAddToKnowledgeBase && (
                        <button type="button" onClick={e => { e.stopPropagation(); actions.onAddToKb(); }}
                            className="p-2 rounded-xl text-foreground-tertiary hover:text-emerald-500 hover:bg-emerald-500/10 transition-colors" title="加入知识库">
                            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
                        </button>
                    )}
                    <button type="button" onClick={e => { e.stopPropagation(); actions.onDelete(); }}
                        className="p-2 rounded-xl text-foreground-tertiary hover:text-red-500 hover:bg-red-500/10 transition-colors" title="删除">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                    </button>
                </div>
            </div>
        </div>
    );
}

export default function HepanHistoryPage() {
    return (
        <HistoryPageTemplate
            sourceType="hepan"
            title="合盘分析历史"
            subtitle="查看您的历史合盘记录"
            layout="list"
            searchPlaceholder="搜索姓名或类型..."
            emptyActionLabel="开始分析"
            deleteMessage="确定要删除这条合盘记录吗？此操作无法撤销。"
            kbSourceType="hepan_chart"
            themeColor="rose-500"
            invalidateTypes={['hepan_chart']}
            kbTitleFn={item => item.question || item.title}
            renderCard={(item, actions) => <HepanCard item={item} actions={actions} />}
        />
    );
}
