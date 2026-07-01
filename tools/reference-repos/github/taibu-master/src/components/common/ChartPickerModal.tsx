/**
 * 通用命盘选择器弹窗
 * 
 * 用于在合盘、AI对话等场景选择已保存的命盘
 * 支持单选和多选模式
 */
'use client';

import { useState, useEffect, useMemo, useCallback, createElement, type ComponentType } from 'react';
import { X, Search, Star } from 'lucide-react';
import { YinYangIcon } from '@phosphor-icons/react';
import { useToast } from '@/components/ui/Toast';
import { listSelectableCharts } from '@/lib/user/charts-client';

export interface ChartItem {
    id: string;
    name: string;
    gender: 'male' | 'female' | null;
    birth_date: string;
    birth_time: string | null;
    birth_year?: number;
    birth_month?: number;
    birth_day?: number;
    birth_hour?: number;
    type: 'bazi' | 'ziwei';
}

export interface ChartPickerModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSelect: (chart: ChartItem) => void;
    userId: string;
    title?: string;
    filterType?: 'bazi' | 'ziwei';  // 只显示某一类型
}

type PickerIcon = ComponentType<{ className?: string; size?: number | string }>;

function phosphor(Icon: ComponentType<Record<string, unknown>>): PickerIcon {
    const Wrapped: PickerIcon = (props) =>
        createElement(Icon, {
            ...props,
            style: { transform: 'scale(1.1)' },
        });
    Wrapped.displayName = `Phosphor(${Icon.displayName ?? Icon.name})`;
    return Wrapped;
}

const PYinYang = phosphor(YinYangIcon);

export function ChartPickerModal({
    isOpen,
    onClose,
    onSelect,
    userId,
    title = '选择命盘',
    filterType,
}: ChartPickerModalProps) {
    const [charts, setCharts] = useState<ChartItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [loadError, setLoadError] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState('');
    const { showToast } = useToast();

    // 加载用户命盘
    useEffect(() => {
        if (!isOpen || !userId) return;

        const loadCharts = async () => {
            setLoading(true);
            setLoadError(null);
            try {
                const rows = await listSelectableCharts();
                const allCharts = rows
                    .filter((chart) => !filterType || chart.type === filterType)
                    .map((chart) => {
                        let year = 0;
                        let month = 0;
                        let day = 0;
                        if (chart.birth_date) {
                            const date = new Date(`${chart.birth_date}T00:00:00`);
                            year = date.getFullYear();
                            month = date.getMonth() + 1;
                            day = date.getDate();
                        }

                        let hour: number | undefined;
                        if (chart.birth_time?.includes(':')) {
                            const [rawHour] = chart.birth_time.split(':');
                            const parsedHour = parseInt(rawHour, 10);
                            hour = Number.isNaN(parsedHour) ? undefined : parsedHour;
                        }

                        return {
                            ...chart,
                            birth_year: year,
                            birth_month: month,
                            birth_day: day,
                            birth_hour: hour,
                        };
                    });

                setCharts(allCharts);
            } catch (error) {
                const message = error instanceof Error ? error.message : '加载命盘失败';
                setCharts([]);
                setLoadError(message);
                showToast('error', message);
            } finally {
                setLoading(false);
            }
        };

        void loadCharts();
    }, [filterType, isOpen, showToast, userId]);

    // 过滤命盘
    const filteredCharts = useMemo(() => {
        if (!searchQuery.trim()) return charts;
        const query = searchQuery.toLowerCase();
        return charts.filter(chart =>
            chart.name.toLowerCase().includes(query)
        );
    }, [charts, searchQuery]);

    // 格式化显示信息
    const formatInfo = useCallback((chart: ChartItem) => {
        const genderText = chart.gender === 'male' ? '男' : chart.gender === 'female' ? '女' : '';
        const dateText = chart.birth_date
            ? new Date(`${chart.birth_date}T00:00:00`).toLocaleDateString('zh-CN')
            : '';
        return [genderText, dateText].filter(Boolean).join(' · ');
    }, []);

    const handleSelect = useCallback((chart: ChartItem) => {
        onSelect(chart);
        onClose();
    }, [onSelect, onClose]);

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div className="absolute inset-0 bg-black/50" onClick={onClose} />

            <div className="relative bg-background rounded-xl border border-border shadow-xl w-full max-w-md flex flex-col" style={{ maxHeight: '480px' }}>
                {/* 头部 */}
                <div className="flex items-center justify-between p-4 border-b border-border flex-shrink-0">
                    <h3 className="text-lg font-semibold">{title}</h3>
                    <button
                        onClick={onClose}
                        className="p-2 rounded-lg hover:bg-background-secondary transition-colors"
                    >
                        <X className="w-4 h-4" />
                    </button>
                </div>

                {/* 搜索框 */}
                <div className="p-3 border-b border-border flex-shrink-0">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground-secondary" />
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={e => setSearchQuery(e.target.value)}
                            placeholder="搜索命盘..."
                            className="w-full pl-9 pr-4 py-2 text-sm rounded-lg bg-background-secondary border border-border focus:outline-none focus:ring-2 focus:ring-accent/30"
                            autoFocus
                        />
                    </div>
                </div>

                {/* 命盘列表 */}
                <div className="flex-1 overflow-y-auto p-2" style={{ maxHeight: '300px' }}>
                    {loading ? (
                        <div className="space-y-1">
                            {/* 骨架屏 - 模拟命盘列表项 */}
                            {[1, 2, 3, 4].map((i) => (
                                <div key={i} className="flex items-center gap-3 p-3 rounded-lg">
                                    <div className="w-8 h-8 rounded-full bg-foreground/10 animate-pulse flex-shrink-0" />
                                    <div className="flex-1 min-w-0 space-y-2">
                                        <div className="h-4 w-24 rounded bg-foreground/10 animate-pulse" />
                                        <div className="h-3 w-32 rounded bg-foreground/5 animate-pulse" />
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : loadError ? (
                        <div className="text-center py-8 text-sm text-[#b42318]">
                            {loadError}
                        </div>
                    ) : filteredCharts.length === 0 ? (
                        <div className="text-center py-8 text-foreground-secondary text-sm">
                            {searchQuery ? '未找到匹配的命盘' : '暂无保存的命盘'}
                        </div>
                    ) : (
                        <div className="space-y-1">
                            {filteredCharts.map(chart => (
                                <button
                                    key={`${chart.type}-${chart.id}`}
                                    onClick={() => handleSelect(chart)}
                                    className="w-full flex items-center gap-3 p-3 rounded-lg transition-colors text-left hover:bg-background-secondary"
                                >
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${chart.type === 'bazi' ? 'bg-orange-500/10' : 'bg-purple-500/10'
                                        }`}>
                                        {chart.type === 'bazi' ? (
                                            <PYinYang className="w-4 h-4 text-orange-500" />
                                        ) : (
                                            <Star className="w-4 h-4 text-purple-500" />
                                        )}
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <div className="font-medium text-sm truncate">{chart.name}</div>
                                        <div className="text-xs text-foreground-secondary truncate">
                                            {formatInfo(chart)}
                                        </div>
                                    </div>
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                {/* 底部提示 */}
                <div className="p-3 border-t border-border text-center text-xs text-foreground-secondary flex-shrink-0">
                    选择命盘后将自动填充出生信息
                </div>
            </div>
        </div>
    );
}
