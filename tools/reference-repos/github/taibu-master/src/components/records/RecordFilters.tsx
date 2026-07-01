/**
 * 记录搜索与筛选栏
 *
 * 'use client' 标记说明：
 * - 使用受控输入（onChange）
 */
'use client';

import { Search, Filter } from 'lucide-react';
import { RecordCategory, RECORD_CATEGORIES } from '@/lib/records';

interface RecordFiltersProps {
    search: string;
    onSearchChange: (value: string) => void;
    category: RecordCategory | '';
    onCategoryChange: (value: RecordCategory | '') => void;
}

export function RecordFilters({
    search,
    onSearchChange,
    category,
    onCategoryChange,
}: RecordFiltersProps) {
    return (
        <div className="sticky top-4 z-30 bg-background/80 backdrop-blur-md rounded-2xl border border-border shadow-sm p-2 flex flex-col sm:flex-row gap-2">
            <div className="flex-1 relative group">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground-secondary group-focus-within:text-emerald-500 transition-colors" />
                <input
                    type="text"
                    value={search}
                    onChange={(e) => onSearchChange(e.target.value)}
                    placeholder="搜索关键词..."
                    className="w-full bg-transparent hover:bg-background-secondary/50 focus:bg-background border-none rounded-xl pl-10 pr-4 py-2.5 text-foreground placeholder:text-foreground-secondary/50 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none"
                />
            </div>
            <div className="w-px h-8 bg-border hidden sm:block self-center" />
            <div className="relative min-w-[160px]">
                <Filter className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground-secondary pointer-events-none" />
                <select
                    value={category}
                    onChange={(e) => onCategoryChange(e.target.value as RecordCategory | '')}
                    className="w-full bg-transparent hover:bg-background-secondary/50 focus:bg-background border-none rounded-xl pl-10 pr-8 py-2.5 text-foreground focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none appearance-none cursor-pointer"
                >
                    <option value="">全部分类</option>
                    {RECORD_CATEGORIES.map(cat => (
                        <option key={cat.value} value={cat.value}>
                            {cat.label}
                        </option>
                    ))}
                </select>
                <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-foreground-secondary">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
                </div>
            </div>
        </div>
    );
}
