/**
 * MentionPopover 列表项渲染
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useEffect, useRef)
 * - 有鼠标交互和滚动行为
 */
'use client';

import { useEffect, useRef } from 'react';
import { ChevronRight } from 'lucide-react';
import type { Mention } from '@/types';
import type {
    ViewItem, ViewModel, Level, MentionPopoverState,
    DataSourceSummary, KnowledgeBaseSummary,
} from '@/components/chat/mention/mention-constants';
import { DATA_SUBCATEGORY_DIVIDE } from '@/components/chat/mention/mention-data-catalog';

interface MentionItemListProps {
    view: ViewModel;
    activeLevel: Level;
    state: MentionPopoverState;
    loading: boolean;
    loadError: string | null;
    knowledgeBaseLocked: boolean;
    onActiveIndexChange: (index: number) => void;
    onNavigate: (nextState: MentionPopoverState) => void;
    onSelect: (mention: Mention) => void;
    onClose: () => void;
}

export function MentionItemList({
    view,
    activeLevel,
    state,
    loading,
    loadError,
    knowledgeBaseLocked,
    onActiveIndexChange,
    onNavigate,
    onSelect,
    onClose,
}: MentionItemListProps) {
    const listRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        const list = listRef.current;
        if (!list) return;
        const active = list.querySelector<HTMLElement>('[data-active="true"]');
        if (!active) return;
        active.scrollIntoView({ block: 'nearest' });
    }, [state.activeIndex, view.items]);

    const handleItemClick = (item: ViewItem) => {
        if (item.disabled) return;

        if (activeLevel === 'search') {
            selectRawItem(item);
            return;
        }

        if (activeLevel === 'category') {
            if (item.key === 'data') {
                onNavigate({ level: 'subcategory', selectedCategory: 'data', activeIndex: 0 });
            } else if (!knowledgeBaseLocked) {
                onNavigate({ level: 'item', selectedCategory: 'knowledge', activeIndex: 0 });
            }
            return;
        }

        if (activeLevel === 'subcategory') {
            if (DATA_SUBCATEGORY_DIVIDE.has(item.key)) {
                onNavigate({ level: 'type', selectedCategory: 'data', selectedSubcategory: item.key, activeIndex: 0 });
            } else {
                onNavigate({ level: 'item', selectedCategory: 'data', selectedSubcategory: item.key, activeIndex: 0 });
            }
            return;
        }

        if (activeLevel === 'type') {
            onNavigate({ level: 'item', selectedCategory: 'data', selectedSubcategory: state.selectedSubcategory, selectedType: item.key, activeIndex: 0 });
            return;
        }

        if (activeLevel === 'item' && state.selectedCategory === 'data') {
            const raw = item.raw;
            if (!raw || !('type' in raw)) return;
            onSelect({ type: (raw as DataSourceSummary).type, id: raw.id, name: raw.name, preview: (raw as DataSourceSummary).preview });
            onClose();
            return;
        }

        // knowledge base item
        const raw = item.raw;
        if (!raw || 'type' in raw) return;
        if (knowledgeBaseLocked) return;
        onSelect({ type: 'knowledge_base', id: raw.id, name: raw.name, preview: (raw as KnowledgeBaseSummary).description || '知识库' });
        onClose();
    };

    const selectRawItem = (item: ViewItem) => {
        const raw = item.raw;
        if (!raw) return;
        if ('type' in raw) {
            onSelect({ type: (raw as DataSourceSummary).type, id: raw.id, name: raw.name, preview: (raw as DataSourceSummary).preview });
            onClose();
            return;
        }
        if (knowledgeBaseLocked) return;
        onSelect({ type: 'knowledge_base', id: raw.id, name: raw.name, preview: (raw as KnowledgeBaseSummary).description || '知识库' });
        onClose();
    };

    const emptyMessage = loadError
        ? loadError
        : activeLevel === 'item' && state.selectedCategory === 'knowledge'
            ? (knowledgeBaseLocked ? '仅限 Plus 以上会员使用' : '你还没有知识库')
            : activeLevel === 'item' && state.selectedCategory === 'data'
                ? '该分类暂无数据'
                : '没有匹配项';

    return (
        <div ref={listRef} className="max-h-48 overflow-auto">
            {loading ? (
                <div className="space-y-1 p-2">
                    {[1, 2, 3].map(i => (
                        <div key={i} className="flex items-center gap-2 px-2 py-2">
                            <div className="w-5 h-5 rounded bg-foreground/10 animate-pulse" />
                            <div className="h-4 w-24 rounded bg-foreground/10 animate-pulse" />
                        </div>
                    ))}
                </div>
            ) : view.items.length === 0 ? (
                <div className="px-3 py-3 text-sm text-foreground-secondary">
                    {emptyMessage}
                </div>
            ) : (
                view.items.map((item, idx) => (
                    <button
                        key={item.key}
                        type="button"
                        data-active={idx === state.activeIndex ? 'true' : 'false'}
                        className={`w-full flex items-center gap-2 px-3 py-2 text-left text-sm ${item.disabled ? 'opacity-60 cursor-not-allowed' : 'hover:bg-background-secondary'} ${idx === state.activeIndex ? 'bg-background-secondary' : ''}`}
                        onMouseEnter={() => onActiveIndexChange(idx)}
                        onClick={() => handleItemClick(item)}
                    >
                        <span className="text-foreground-secondary">{item.icon}</span>
                        <div className="flex-1 min-w-0">
                            <div className="truncate">{item.label}</div>
                            {!!item.hint && <div className="truncate text-xs text-foreground-secondary">{item.hint}</div>}
                        </div>
                        {(activeLevel === 'category' || activeLevel === 'subcategory') && <ChevronRight className="w-4 h-4 text-foreground-secondary" />}
                    </button>
                ))
            )}
        </div>
    );
}
