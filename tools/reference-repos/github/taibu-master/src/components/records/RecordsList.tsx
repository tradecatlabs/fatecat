/**
 * 记录列表组件：包含记录卡片、列表网格和分页
 *
 * 'use client' 标记说明：
 * - 使用交互回调（onClick）
 */
'use client';

import {
    Pin,
    Archive,
    Edit2,
    Trash2,
    Calendar,
    FileText,
    BookOpenText,
    ChevronLeft,
    ChevronRight,
} from 'lucide-react';
import { MingRecord, RECORD_CATEGORIES } from '@/lib/records';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import { useKnowledgeBaseFeatureEnabled } from '@/components/knowledge-base/useKnowledgeBaseFeatureEnabled';

// =====================================================
// 记录卡片组件
// =====================================================
function RecordCard({
    record,
    onEdit,
    onDelete,
    onTogglePin,
    onAddToKnowledgeBase,
    showKnowledgeBaseAction,
}: {
    record: MingRecord;
    onEdit: () => void;
    onDelete: () => void;
    onTogglePin: () => void;
    onAddToKnowledgeBase: () => void;
    showKnowledgeBaseAction: boolean;
}) {
    const categoryInfo = RECORD_CATEGORIES.find(c => c.value === record.category);

    return (
        <div className={`group bg-background-secondary/40 backdrop-blur-sm rounded-xl p-5 border transition-all duration-300 ${record.is_pinned
            ? 'border-yellow-500/30 bg-yellow-500/5 shadow-[0_0_15px_-3px_rgba(234,179,8,0.1)]'
            : 'border-border/50 hover:border-emerald-500/30 hover:bg-background-secondary/60 hover:shadow-lg hover:shadow-emerald-500/5'
            }`}>
            <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-2">
                        {record.is_pinned && (
                            <span className="flex items-center gap-1 text-[10px] uppercase font-bold text-yellow-600 dark:text-yellow-500 bg-yellow-500/10 px-1.5 py-0.5 rounded border border-yellow-500/20">
                                <Pin className="w-3 h-3" /> 置顶
                            </span>
                        )}
                        {record.is_archived && (
                            <span
                                className="flex items-center gap-1 text-[10px] uppercase font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/20"
                                title={
                                    Array.isArray(record.archived_kb_ids) && record.archived_kb_ids.length
                                        ? `已归档到 ${record.archived_kb_ids.length} 个知识库`
                                        : '已归档到知识库'
                                }
                            >
                                <Archive className="w-3 h-3" /> 归档
                            </span>
                        )}
                        <span className={`text-xs px-2 py-0.5 rounded-full border flex items-center gap-1.5 ${record.is_pinned
                            ? 'text-yellow-600 dark:text-yellow-500 border-yellow-500/20 bg-yellow-500/5'
                            : 'text-foreground-secondary border-border/50 bg-background/50'
                            }`}>
                            {categoryInfo?.icon} {categoryInfo?.label}
                        </span>
                        {record.event_date && (
                            <span className="text-xs text-foreground-secondary/70 flex items-center gap-1">
                                <Calendar className="w-3 h-3" />
                                {record.event_date}
                            </span>
                        )}
                    </div>

                    <h3 className="font-bold text-lg text-foreground mb-2 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors line-clamp-1">
                        {record.title}
                    </h3>

                    {record.content && (
                        <p className="text-sm text-foreground-secondary/80 leading-relaxed line-clamp-2 mb-3">
                            {record.content}
                        </p>
                    )}

                    {record.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 mt-2">
                            {record.tags.slice(0, 3).map((tag, i) => (
                                <span key={i} className="text-xs px-2 py-0.5 bg-emerald-500/5 text-emerald-600 dark:text-emerald-400 rounded-md border border-emerald-500/10">
                                    #{tag}
                                </span>
                            ))}
                            {record.tags.length > 3 && (
                                <span className="text-xs text-foreground-secondary/50 self-center">+{record.tags.length - 3}</span>
                            )}
                        </div>
                    )}
                </div>

                <div className="flex flex-col gap-1 opacity-100 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
                    <button
                        onClick={onTogglePin}
                        className={`p-2 rounded-lg transition-colors ${record.is_pinned
                            ? 'text-yellow-500 bg-yellow-500/10 hover:bg-yellow-500/20'
                            : 'text-foreground-secondary hover:text-yellow-500 hover:bg-yellow-500/10'
                            }`}
                        title={record.is_pinned ? '取消置顶' : '置顶'}
                    >
                        <Pin className="w-4 h-4" />
                    </button>
                    {showKnowledgeBaseAction && (
                        <button
                            onClick={onAddToKnowledgeBase}
                            className="p-2 text-foreground-secondary hover:text-emerald-500 hover:bg-emerald-500/10 rounded-lg transition-colors"
                            title="加入知识库"
                        >
                            <BookOpenText className="w-4 h-4" />
                        </button>
                    )}
                    <button
                        onClick={onEdit}
                        className="p-2 text-foreground-secondary hover:text-emerald-500 hover:bg-emerald-500/10 rounded-lg transition-colors"
                        title="编辑"
                    >
                        <Edit2 className="w-4 h-4" />
                    </button>
                    <button
                        onClick={onDelete}
                        className="p-2 text-foreground-secondary hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-colors"
                        title="删除"
                    >
                        <Trash2 className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
}

// =====================================================
// 记录列表（含分页）
// =====================================================
interface RecordsListProps {
    loading: boolean;
    records: MingRecord[];
    page: number;
    totalPages: number;
    onPageChange: (page: number) => void;
    onEdit: (record: MingRecord) => void;
    onDelete: (id: string) => void;
    onTogglePin: (id: string) => void;
    onAddToKnowledgeBase: (record: MingRecord) => void;
    onCreateNew: () => void;
}

export function RecordsList({
    loading,
    records,
    page,
    totalPages,
    onPageChange,
    onEdit,
    onDelete,
    onTogglePin,
    onAddToKnowledgeBase,
    onCreateNew,
}: RecordsListProps) {
    const { knowledgeBaseEnabled } = useKnowledgeBaseFeatureEnabled();

    const pagination = totalPages > 1 ? (
        <div className="flex items-center justify-center gap-3 pt-8 pb-4">
            <button
                onClick={() => onPageChange(Math.max(1, page - 1))}
                disabled={page === 1}
                className="p-2 rounded-lg hover:bg-background-secondary disabled:opacity-50 disabled:hover:bg-transparent transition-colors text-foreground-secondary"
            >
                <ChevronLeft className="w-5 h-5" />
            </button>
            <span className="text-sm font-medium text-foreground px-4 py-1.5 bg-background-secondary rounded-lg">
                {page} / {totalPages}
            </span>
            <button
                onClick={() => onPageChange(Math.min(totalPages, page + 1))}
                disabled={page === totalPages}
                className="p-2 rounded-lg hover:bg-background-secondary disabled:opacity-50 disabled:hover:bg-transparent transition-colors text-foreground-secondary"
            >
                <ChevronRight className="w-5 h-5" />
            </button>
        </div>
    ) : null;

    if (loading) {
        return <SoundWaveLoader variant="block" text="加载记录中" />;
    }

    if (records.length === 0) {
        return (
            <>
                <div className="py-20 text-center">
                    <div className="w-24 h-24 bg-background-secondary/50 rounded-full flex items-center justify-center mx-auto mb-6">
                        <FileText className="w-10 h-10 text-foreground-secondary/50" />
                    </div>
                    <h3 className="text-lg font-medium text-foreground mb-2">
                        {totalPages > 1 ? '当前页暂无记录' : '暂无记录'}
                    </h3>
                    <p className="text-foreground-secondary mb-6 max-w-xs mx-auto">
                        {totalPages > 1
                            ? '这一页已经空了，可以切换到上一页继续查看。'
                            : '还没有添加任何命理记录。开始记录你的第一次感悟吧！'}
                    </p>
                    {totalPages > 1 ? null : (
                        <button
                            onClick={onCreateNew}
                            className="px-6 py-2.5 bg-background border border-border hover:border-emerald-500/50 hover:text-emerald-500 rounded-xl transition-all shadow-sm hover:shadow-md"
                        >
                            立即添加
                        </button>
                    )}
                </div>
                {pagination}
            </>
        );
    }

    return (
        <>
            <div className="grid gap-4">
                {records.map(record => (
                    <RecordCard
                        key={record.id}
                        record={record}
                        onEdit={() => onEdit(record)}
                        onDelete={() => onDelete(record.id)}
                        onTogglePin={() => onTogglePin(record.id)}
                        onAddToKnowledgeBase={() => onAddToKnowledgeBase(record)}
                        showKnowledgeBaseAction={knowledgeBaseEnabled}
                    />
                ))}
            </div>

            {pagination}
        </>
    );
}
