import type { ZiweiPalaceJSON } from 'taibu-core/ziwei';
import { StarBadge } from '@/components/ziwei/StarBadge';

interface FlowInfo {
    decadal?: { stem: string; ages: string };
    yearly?: string;
    monthly?: string;
    daily?: string;
}

interface PalaceCardProps {
    palace: ZiweiPalaceJSON;
    isSelected?: boolean;
    isLifePalace?: boolean;
    isHighlighted?: boolean;
    highlightTypes?: string[];
    isSanFangSiZheng?: boolean;
    showAdjStars?: boolean;
    flowInfo?: FlowInfo;
    onClick?: () => void;
}

// 高亮类型对应的颜色
const highlightColors: Record<string, { border: string; bg: string }> = {
    decadal: { border: 'border-purple-500', bg: 'bg-purple-500/10' },
    yearly: { border: 'border-blue-500', bg: 'bg-blue-500/10' },
    monthly: { border: 'border-green-500', bg: 'bg-green-500/10' },
    daily: { border: 'border-orange-500', bg: 'bg-orange-500/10' },
};

// 多重高亮指示条颜色
const indicatorBarColors: Record<string, string> = {
    decadal: 'bg-purple-500',
    yearly: 'bg-blue-500',
    monthly: 'bg-green-500',
    daily: 'bg-orange-500',
};

export function PalaceCard({
    palace,
    isSelected = false,
    isLifePalace = false,
    isHighlighted = false,
    highlightTypes = [],
    isSanFangSiZheng = false,
    showAdjStars = false,
    flowInfo,
    onClick
}: PalaceCardProps) {
    const shenSha = palace.神煞?.join('、') || '';
    const toStarInfo = (
        star: ZiweiPalaceJSON['主星及四化'][number],
        type: 'major' | 'minor' | 'auxiliary',
    ) => ({
        ...star,
        type,
    });
    // 获取边框样式（支持多色）
    const getBorderClasses = () => {
        if (isSelected) return 'border-accent bg-accent/5 shadow-md';
        if (isSanFangSiZheng) return 'border-green-500/50 bg-green-500/5 shadow-sm';
        if (isHighlighted && highlightTypes.length > 0) {
            // 单一高亮时直接使用对应颜色边框
            if (highlightTypes.length === 1) {
                const highlight = highlightColors[highlightTypes[0]];
                if (highlight) {
                    return `${highlight.border} ${highlight.bg} shadow-sm`;
                }
            }
            // 多重高亮时使用渐变背景 + 中性边框，指示条显示各色
            return 'border-foreground/30 bg-gradient-to-br from-purple-500/5 to-blue-500/5 shadow-sm';
        }
        return 'border-border bg-background-secondary hover:bg-background-tertiary';
    };

    // 是否有流限信息
    const hasFlowInfo = flowInfo && (flowInfo.decadal || flowInfo.yearly || flowInfo.monthly || flowInfo.daily);

    return (
        <div
            role="button"
            tabIndex={0}
            onClick={onClick}
            onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    onClick?.();
                }
            }}
            className={`
                relative h-full min-h-[100px] p-2 rounded-lg border-2 transition-all cursor-pointer flex flex-col
                ${getBorderClasses()}
            `}
        >
            {/* 多重高亮指示条 */}
            {highlightTypes.length > 1 && (
                <div className="absolute top-0 left-0 right-0 flex h-1 rounded-t-md overflow-hidden">
                    {highlightTypes.map((type) => (
                        <div
                            key={type}
                            className={`flex-1 ${indicatorBarColors[type] || 'bg-gray-400'}`}
                        />
                    ))}
                </div>
            )}
            {/* 宫名和干支 */}
            <div className="flex items-center justify-between mb-1">
                <span className={`text-xs font-semibold ${isLifePalace ? 'text-accent' : 'text-foreground'}`}>
                    {palace.宫位}
                    {palace.是否身宫 === '是' && (
                        <span className="md:ml-1 ml-0 px-1 py-0.5 text-[9px] bg-amber-500/20 text-amber-500 rounded font-medium">
                            身宫
                        </span>
                    )}
                    {palace.是否来因宫 === '是' && (
                        <span className="ml-1 px-1 py-0.5 text-[9px] bg-sky-500/15 text-sky-600 rounded font-medium">
                            来因宫
                        </span>
                    )}
                </span>
                <span className="text-[10px] text-foreground-secondary">
                    {palace.干支}
                </span>
            </div>
            {/* 星曜列表 - 主内容区 */}
            <div className="flex-1 flex flex-wrap gap-0.5 content-start">
                {/* 主星全部显示 */}
                {palace.主星及四化.map((star, idx) => (
                    <StarBadge key={`major-${idx}`} star={toStarInfo(star, 'major')} size="sm" />
                ))}
                {/* 辅星全部显示 */}
                {palace.辅星.map((star, idx) => (
                    <StarBadge key={`minor-${idx}`} star={toStarInfo(star, 'minor')} size="sm" />
                ))}
                {/* 杂曜全部显示（受showAdjStars控制） */}
                {showAdjStars && palace.杂曜?.map((star, idx) => (
                    <StarBadge key={`adj-${idx}`} star={toStarInfo(star, 'auxiliary')} size="sm" />
                ))}
            </div>

            {shenSha && (
                <div className="mt-1 space-y-1 text-[9px] text-foreground-secondary">
                    {shenSha && <div>神煞：{shenSha}</div>}
                </div>
            )}

            {/* 流限信息 - 底部横向排列 */}
            {hasFlowInfo && (
                <div className="flex flex-wrap gap-1 mt-1 pt-1 border-t border-border/50 text-[8px]">
                    {flowInfo.decadal && (
                        <span className="flex flex-col items-center px-1 py-0.5 bg-purple-500/20 text-purple-500 rounded leading-tight">
                            <span>限</span>
                            <span>{flowInfo.decadal.stem}</span>
                        </span>
                    )}
                    {flowInfo.yearly && (
                        <span className="flex flex-col items-center px-1 py-0.5 bg-blue-500/20 text-blue-500 rounded leading-tight">
                            <span>年</span>
                            <span>{flowInfo.yearly}</span>
                        </span>
                    )}
                    {flowInfo.monthly && (
                        <span className="flex flex-col items-center px-1 py-0.5 bg-green-500/20 text-green-500 rounded leading-tight">
                            <span>月</span>
                            <span>{flowInfo.monthly}</span>
                        </span>
                    )}
                    {flowInfo.daily && (
                        <span className="flex flex-col items-center px-1 py-0.5 bg-orange-500/20 text-orange-500 rounded leading-tight">
                            <span>日</span>
                            <span>{flowInfo.daily}</span>
                        </span>
                    )}
                    {flowInfo.decadal?.ages && (
                        <span className="text-foreground-secondary ml-auto">
                            {flowInfo.decadal.ages}
                        </span>
                    )}
                </div>
            )}
        </div>
    );
}
