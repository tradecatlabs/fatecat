/**
 * 对话分组组件（按类型分组的一个区块）
 *
 * 'use client' 标记说明：
 * - 需要处理用户交互事件（折叠/展开）
 */
'use client';

import { ChevronDown, ChevronRight } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import type { ConversationListItem, ConversationSourceType } from '@/types';
import { ConversationItem } from '@/components/chat/sidebar/ConversationItem';

interface ConversationGroupProps {
    type: ConversationSourceType;
    label: string;
    items: ConversationListItem[];
    showLabel?: boolean;
    isGroupCollapsed: boolean;
    onToggleGroup: (type: ConversationSourceType) => void;
    activeId?: string;
    actionConvId?: string;
    isSidebarCollapsed: boolean;
    onSelect: (id: string) => void;
    onOpenAction: (conv: ConversationListItem, e: React.MouseEvent) => void;
    editingId?: string | null;
    editTitle?: string;
    onEditTitleChange?: (value: string) => void;
    onSaveRename?: () => void;
    onCancelRename?: () => void;
    pendingTitle?: string | null;
    showPendingInGroup: boolean;
    /** 紧凑模式 — 内嵌侧边栏时使用更小间距 */
    compact?: boolean;
}

export function ConversationGroup({
    type,
    label,
    items,
    showLabel = true,
    isGroupCollapsed,
    onToggleGroup,
    activeId,
    actionConvId,
    isSidebarCollapsed,
    onSelect,
    onOpenAction,
    editingId,
    editTitle,
    onEditTitleChange,
    onSaveRename,
    onCancelRename,
    pendingTitle,
    showPendingInGroup,
    compact = false,
}: ConversationGroupProps) {
    const displayCount = items.length + (showPendingInGroup ? 1 : 0);
    const shouldShowContent = showLabel ? !isGroupCollapsed : true;

    return (
        <div className={compact ? 'mb-1' : 'mb-2'}>
            {/* 分组标题 */}
            {showLabel && (
                <button
                    onClick={(e) => {
                        e.stopPropagation();
                        onToggleGroup(type);
                    }}
                    className={`flex items-center w-full text-foreground-secondary hover:text-foreground transition-colors duration-150 ${compact ? 'px-3 py-1 text-[10px] gap-1' : 'px-3 py-1.5 text-xs gap-2'}`}
                >
                    {isGroupCollapsed ? (
                        <ChevronRight className={compact ? 'w-3 h-3' : 'w-3.5 h-3.5'} />
                    ) : (
                        <ChevronDown className={compact ? 'w-3 h-3' : 'w-3.5 h-3.5'} />
                    )}
                    <span className="font-bold uppercase tracking-wider">{label}</span>
                    <span className="ml-auto font-mono opacity-50">
                        {displayCount}
                    </span>
                </button>
            )}

            {/* 分组内容 */}
            {shouldShowContent && (
                <div className={compact ? 'space-y-px' : 'space-y-0.5 mt-1'}>
                    {showPendingInGroup && (
                        <div className={compact ? 'px-3 py-1 rounded-md bg-background-secondary' : 'px-3 py-2 rounded-md bg-background-secondary/70 border border-border/60'}>
                            <div className="flex items-center gap-1.5">
                                <SoundWaveLoader variant="inline" />
                                <span className={`font-medium text-foreground truncate ${compact ? 'text-[13px]' : 'text-sm'}`}>{pendingTitle}</span>
                            </div>
                        </div>
                    )}
                    {items.map(conv => (
                        <ConversationItem
                            key={conv.id}
                            conv={conv}
                            isActive={activeId === conv.id}
                            isActionActive={actionConvId === conv.id}
                            isSidebarCollapsed={isSidebarCollapsed}
                            onSelect={onSelect}
                            onOpenAction={onOpenAction}
                            isEditing={editingId === conv.id}
                            editTitle={editingId === conv.id ? editTitle : ''}
                            onEditTitleChange={editingId === conv.id ? onEditTitleChange : undefined}
                            onSaveRename={editingId === conv.id ? onSaveRename : undefined}
                            onCancelRename={editingId === conv.id ? onCancelRename : undefined}
                            compact={compact}
                        />
                    ))}
                </div>
            )}
        </div>
    );
}
