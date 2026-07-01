/**
 * MentionPopover 标题栏（含返回按钮和错误提示）
 *
 * 'use client' 标记说明：
 * - 有点击交互（返回按钮）
 */
'use client';

import { ArrowLeft } from 'lucide-react';
import type { Level, DataSourceLoadError } from '@/components/chat/mention/mention-constants';

interface MentionHeaderProps {
    title: string;
    activeLevel: Level;
    loadError: string | null;
    dataSourceErrors: DataSourceLoadError[];
    onGoBack: () => void;
}

export function MentionHeader({ title, activeLevel, loadError, dataSourceErrors, onGoBack }: MentionHeaderProps) {
    return (
        <>
            <div className="px-3 py-2 text-xs text-foreground-secondary border-b border-border/60 flex items-center gap-2">
                {activeLevel !== 'category' && activeLevel !== 'search' && (
                    <button
                        type="button"
                        onClick={onGoBack}
                        className="p-1 rounded hover:bg-background-secondary text-foreground-secondary hover:text-foreground"
                        aria-label="返回"
                    >
                        <ArrowLeft className="w-4 h-4" />
                    </button>
                )}
                <div className="truncate">{title}</div>
            </div>
            {!!loadError && (
                <div className="px-3 py-2 text-xs text-red-500 border-b border-border/60">
                    {loadError}
                </div>
            )}
            {!loadError && dataSourceErrors.length > 0 && (
                <div className="px-3 py-2 text-xs text-amber-500 border-b border-border/60">
                    数据源加载部分失败：{dataSourceErrors.slice(0, 2).map(e => e.type).join('、')}{dataSourceErrors.length > 2 ? '…' : ''}
                </div>
            )}
        </>
    );
}
