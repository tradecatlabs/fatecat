/**
 * 64卦选择器
 *
 * 显示64卦网格，支持搜索筛选
 */
'use client';

import { useState } from 'react';
import { Search } from 'lucide-react';
import { HEXAGRAMS } from '@/lib/divination/liuyao';

interface HexagramSelectorProps {
    value?: string;
    onChange: (code: string) => void;
}

export function HexagramSelector({ value, onChange }: HexagramSelectorProps) {
    const [search, setSearch] = useState('');

    const filtered = search
        ? HEXAGRAMS.filter(h =>
            h.name.includes(search) ||
            h.upperTrigram.includes(search) ||
            h.lowerTrigram.includes(search) ||
            h.nature.includes(search)
        )
        : HEXAGRAMS;

    const selectedHexagram = value ? HEXAGRAMS.find(h => h.code === value) : null;

    return (
        <div className="space-y-3">
            {/* 搜索框 */}
            <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground-secondary" />
                <input
                    type="text"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    placeholder="搜索卦名、卦象..."
                    className="w-full pl-9 pr-4 py-2 bg-background border border-border rounded-lg text-sm
                        focus:border-accent focus:outline-none focus:ring-0
                        placeholder:text-foreground-tertiary"
                />
            </div>

            {/* 已选显示 */}
            {selectedHexagram && (
                <div className="flex items-center gap-2 px-3 py-2 bg-accent/10 border border-accent/30 rounded-lg text-sm">
                    <span className="text-accent font-bold">{selectedHexagram.name}</span>
                    <span className="text-foreground-secondary">
                        {selectedHexagram.upperTrigram}/{selectedHexagram.lowerTrigram} · {selectedHexagram.element}
                    </span>
                </div>
            )}

            {/* 卦列表网格 */}
            <div className="grid grid-cols-4 md:grid-cols-8 gap-1.5 max-h-[300px] overflow-y-auto pr-1">
                {filtered.map(h => (
                    <button
                        key={h.code}
                        onClick={() => onChange(h.code)}
                        className={`px-1 py-2 rounded text-xs text-center transition-all
                            ${value === h.code
                                ? 'bg-accent text-white font-bold ring-2 ring-accent/50'
                                : 'bg-background/5 border border-white/10 text-foreground hover:bg-background/10 hover:border-white/20'
                            }`}
                    >
                        {h.name}
                    </button>
                ))}
            </div>

            {filtered.length === 0 && (
                <p className="text-center text-sm text-foreground-secondary py-4">
                    未找到匹配的卦象
                </p>
            )}
        </div>
    );
}
