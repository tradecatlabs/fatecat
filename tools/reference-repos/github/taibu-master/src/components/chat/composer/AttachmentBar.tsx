/**
 * 附件和知识库引用显示栏
 *
 * 'use client' 标记说明：
 * - 需要处理用户交互事件
 */
'use client';

import { FileText, X, BookOpenText, Moon } from 'lucide-react';
import type { AttachmentState } from '@/types';
import { mentionStyleMap } from '@/components/chat/mentionStyles';
import type { KnowledgeBaseSummary } from '@/components/chat/composer/useComposerState';

interface AttachmentBarProps {
    hasFile: boolean;
    attachmentState?: AttachmentState;
    onAttachmentChange?: (state: AttachmentState) => void;
    disabled: boolean;
    canUseKnowledgeBase: boolean;
    promptKnowledgeBases: KnowledgeBaseSummary[];
    isDreamMode: boolean;
    dreamContextLoading: boolean;
    dreamContext?: { baziChartName?: string; dailyFortune?: string };
}

export function AttachmentBar({
    hasFile,
    attachmentState,
    onAttachmentChange,
    disabled,
    canUseKnowledgeBase,
    promptKnowledgeBases,
    isDreamMode,
    dreamContextLoading,
    dreamContext,
}: AttachmentBarProps) {
    const showKbBadges = canUseKnowledgeBase && promptKnowledgeBases.length > 0;
    const showDreamBadges = isDreamMode;

    return (
        <>
            {/* 已上传文件显示卡片 */}
            {hasFile && (
                <div className="flex items-start gap-2 mb-2">
                    <div className="flex items-center gap-3 px-3 py-2.5 bg-background border border-border rounded-xl max-w-[280px]">
                        <div className="flex-shrink-0 w-9 h-9 bg-blue-500 rounded-lg flex items-center justify-center">
                            <FileText className="w-5 h-5 text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-foreground truncate">
                                {attachmentState?.file?.name}
                            </p>
                            <p className="text-xs text-foreground-secondary">文件</p>
                        </div>
                        {!disabled && (
                            <button
                                type="button"
                                onClick={() => onAttachmentChange?.({ ...attachmentState, file: undefined, webSearchEnabled: attachmentState?.webSearchEnabled ?? false })}
                                className="flex-shrink-0 ml-1 p-0.5 rounded-full bg-foreground-secondary/20 hover:bg-foreground-secondary/40 text-foreground-secondary hover:text-foreground transition-colors"
                                title="移除文件"
                            >
                                <X className="w-3.5 h-3.5" />
                            </button>
                        )}
                    </div>
                </div>
            )}

            {(showKbBadges || showDreamBadges) && (
                <div className="flex flex-wrap items-center gap-2 mb-2 px-2">
                    <span className="text-xs text-foreground-secondary">已参考</span>
                    {canUseKnowledgeBase && promptKnowledgeBases.map(kb => (
                        <span
                            key={kb.id}
                            className={`inline-flex items-center gap-1 px-2 py-1 rounded-lg border text-xs ${mentionStyleMap.knowledge_base.className}`}
                            title={kb.description || kb.name}
                        >
                            <BookOpenText className="w-3.5 h-3.5" />
                            <span className="max-w-[160px] truncate">{kb.name}</span>
                        </span>
                    ))}
                    {isDreamMode && (
                        <>
                            {dreamContextLoading && (
                                <span className="inline-flex items-center gap-1 px-2 py-1 rounded-lg border border-purple-500/30 bg-purple-500/10 text-purple-600 text-xs">
                                    <Moon className="w-3.5 h-3.5" />
                                    <span>正在加载</span>
                                </span>
                            )}
                            {dreamContext?.baziChartName && (
                                <span className="inline-flex items-center gap-1 px-2 py-1 rounded-lg border border-purple-500/30 bg-purple-500/10 text-purple-600 text-xs">
                                    <Moon className="w-3.5 h-3.5" />
                                    <span className="max-w-[160px] truncate">{dreamContext.baziChartName}</span>
                                </span>
                            )}
                            {dreamContext?.dailyFortune && (
                                <span className="inline-flex items-center gap-1 px-2 py-1 rounded-lg border border-purple-500/30 bg-purple-500/10 text-purple-600 text-xs">
                                    <Moon className="w-3.5 h-3.5" />
                                    <span>今日运势</span>
                                </span>
                            )}
                        </>
                    )}
                </div>
            )}
        </>
    );
}
