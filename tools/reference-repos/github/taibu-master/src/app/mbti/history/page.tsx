/**
 * MBTI 历史记录页面 - 使用 HistoryPageTemplate
 */
'use client';

import { Brain, Calendar, BookOpenText, Trash2 } from 'lucide-react';
import { HistoryPageTemplate, type CardActions } from '@/components/history/HistoryPageTemplate';
import type { HistorySummaryItem } from '@/lib/history/registry';
import { PERSONALITY_BASICS, type MBTIType } from '@/lib/divination/mbti';

function resolveMbtiTypeLabel(title: string) {
  return title.replace(/\s*人格$/u, '').trim();
}

function MBTIHistoryCard({ item, actions }: { item: HistorySummaryItem; actions: CardActions }) {
  const mbtiType = resolveMbtiTypeLabel(item.title) as MBTIType;
  const info = PERSONALITY_BASICS[mbtiType];
  const dimensionBadges = item.badges?.filter((badge) => typeof badge === 'string' && badge.trim().length > 0) ?? [];

  return (
    <div
      className="bg-background-secondary rounded-xl p-4 border border-border hover:border-accent/30 transition-colors cursor-pointer"
      onClick={actions.onView}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2">
            <span className="px-3 py-1 text-sm font-bold rounded-lg bg-accent/10 text-accent">
              {mbtiType}
            </span>
            <span className="text-sm font-medium text-foreground">
              {item.question || info?.title || item.title}
            </span>
            {item.modelName ? (
              <span className="text-[10px] text-foreground-secondary px-2 py-0.5 rounded bg-background border border-border">
                {item.modelName}
              </span>
            ) : null}
            <div className="ml-auto flex items-center gap-2">
              <span className="flex items-center gap-1 text-xs text-foreground-secondary">
                <Calendar className="w-3 h-3" />
                {actions.formatDate(item.createdAt)}
              </span>
            </div>
          </div>
          {dimensionBadges.length > 0 ? (
            <div className="flex flex-wrap gap-2 mt-2">
              {dimensionBadges.map((badge) => (
                <span key={badge} className="text-xs px-2 py-0.5 rounded bg-background text-foreground-secondary">
                  {badge}
                </span>
              ))}
            </div>
          ) : info?.description ? (
            <p className="text-xs text-foreground-secondary mt-1 line-clamp-2">{info.description}</p>
          ) : null}
        </div>
        <div className="flex items-center gap-1">
          {actions.canAddToKnowledgeBase ? (
            <button
              type="button"
              onClick={(event) => {
                event.stopPropagation();
                actions.onAddToKb();
              }}
              className="p-2 rounded-lg hover:bg-emerald-500/10 text-foreground-secondary hover:text-emerald-500 transition-colors"
              title="加入知识库"
            >
              <BookOpenText className="w-4 h-4" />
            </button>
          ) : null}
          <button
            type="button"
            onClick={(event) => {
              event.stopPropagation();
              actions.onDelete();
            }}
            className="p-2 rounded-lg hover:bg-red-500/10 text-foreground-secondary hover:text-red-500 transition-colors"
            title="删除"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default function MBTIHistoryPage() {
  return (
    <HistoryPageTemplate
      sourceType="mbti"
      title="MBTI 测试历史"
      subtitle="查看您的历史测试结果"
      icon={Brain}
      iconColor="text-accent"
      layout="list"
      searchPlaceholder="搜索人格类型..."
      emptyActionLabel="开始测试"
      emptyActionHref="/mbti"
      deleteMessage="确定要删除这条 MBTI 测试记录吗？此操作无法撤销。"
      kbSourceType="mbti_reading"
      themeColor="accent"
      invalidateTypes={['mbti_reading']}
      kbTitleFn={(item) => `MBTI - ${resolveMbtiTypeLabel(item.title)}`}
      filterFn={(item, query) => {
        const normalizedQuery = query.toLowerCase();
        const mbtiType = resolveMbtiTypeLabel(item.title).toLowerCase();
        const title = item.question?.toLowerCase() || PERSONALITY_BASICS[resolveMbtiTypeLabel(item.title) as MBTIType]?.title.toLowerCase() || '';
        return mbtiType.includes(normalizedQuery) || title.includes(normalizedQuery);
      }}
      renderCard={(item, actions) => <MBTIHistoryCard item={item} actions={actions} />}
    />
  );
}
