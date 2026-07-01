/**
 * 紫微命盘网格组件
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useState)
 * - 有宫位显示/隐藏交互功能
 */
'use client';

import { useState } from 'react';
import type { ZiweiCanonicalJSON } from 'taibu-core/ziwei';
import { getBranchIndex, getTriangleSquare } from '@/lib/divination/ziwei';
import { getBranchElement, getStemElement, getElementColor } from '@/lib/divination/display-helpers';
import { PalaceCard } from '@/components/ziwei/PalaceCard';
import type { HoroscopeInfo, HoroscopeHighlight } from '@/components/ziwei/ZiweiHoroscopePanel';
import { Eye, EyeOff } from 'lucide-react';

import { useToast } from '@/components/ui/Toast';

interface ZiweiChartProps {
    canonicalChart: ZiweiCanonicalJSON;
    copied?: boolean;
    onCopy?: () => void;
    showJsonCopy?: boolean;
    jsonCopied?: boolean;
    onCopyJson?: () => void;
    horoscopeHighlight?: HoroscopeHighlight;
    horoscopeInfo?: HoroscopeInfo;
}

// 五行颜色映射：天干地支五行颜色统一走 display helpers
function getStemElementStyle(stem: string | undefined): { color: string } | undefined {
    if (!stem) return undefined;
    const element = getStemElement(stem);
    return element ? { color: getElementColor(element) } : undefined;
}

function getBranchElementStyle(branch: string | undefined): { color: string } | undefined {
    if (!branch) return undefined;
    const element = getBranchElement(branch);
    return element ? { color: getElementColor(element) } : undefined;
}


/**
 * 紫微斗数命盘 12 宫位图
 */
export function ZiweiChartGrid({
    canonicalChart,
    copied = false,
    onCopy,
    showJsonCopy = false,
    jsonCopied = false,
    onCopyJson,
    horoscopeHighlight = {},
    horoscopeInfo,
}: ZiweiChartProps) {
    const lifePalaceIndex = canonicalChart.十二宫位.find(p => p.宫位 === '命宫')?.宫位索引 ?? null;
    // 默认选中命宫，显示三方四正
    const [selectedPalace, setSelectedPalace] = useState<number | null | undefined>(undefined);
    const [showAdjStars, setShowAdjStars] = useState(true); // 默认显示杂曜
    const { showToast } = useToast();

    const defaultSelectedPalace = typeof lifePalaceIndex === 'number' && lifePalaceIndex >= 0 ? lifePalaceIndex : null;
    const activeSelectedPalace = selectedPalace === undefined ? defaultSelectedPalace : selectedPalace;

    const getCanonicalPalaceByBranch = (branchIndex: number) => {
        return canonicalChart.十二宫位.find((p) => getBranchIndex(p.干支.slice(-1)) === branchIndex);
    };

    // 计算三方四正高亮
    const sanFangSiZhengPalaces = activeSelectedPalace !== null ? getTriangleSquare(activeSelectedPalace).square : [];

    // 获取宫位高亮类型（多色支持）
    const getHighlightTypes = (palaceIndex: number) => {
        const types: string[] = [];
        if (horoscopeHighlight.decadalIndex === palaceIndex) types.push('decadal');
        if (horoscopeHighlight.yearlyIndex === palaceIndex) types.push('yearly');
        if (horoscopeHighlight.monthlyIndex === palaceIndex) types.push('monthly');
        if (horoscopeHighlight.dailyIndex === palaceIndex) types.push('daily');
        return types;
    };

    const handleCopy = () => {
        try {
            onCopy?.();
        } catch {
            showToast('error', '复制失败，请手动复制');
        }
    };

    // 生成宫位的流年流月信息
    const getFlowInfoForPalace = (palaceIndex: number) => {
        if (!horoscopeInfo) return undefined;

        const flowInfo: {
            decadal?: { stem: string; ages: string };
            yearly?: string;
            monthly?: string;
            daily?: string
        } = {};

        if (horoscopeInfo.decadal && horoscopeInfo.decadal.palace.index === palaceIndex) {
            flowInfo.decadal = {
                stem: horoscopeInfo.decadal.heavenlyStem,
                ages: `${horoscopeInfo.decadal.startAge}岁`,
            };
        }

        if (horoscopeInfo.yearly && horoscopeInfo.yearly.palaceIndex === palaceIndex) {
            flowInfo.yearly = horoscopeInfo.yearly.heavenlyStem;
        }

        if (horoscopeInfo.monthly && horoscopeInfo.monthly.palaceIndex === palaceIndex) {
            flowInfo.monthly = horoscopeInfo.monthly.heavenlyStem;
        }

        if (horoscopeInfo.daily && horoscopeInfo.daily.palaceIndex === palaceIndex) {
            flowInfo.daily = horoscopeInfo.daily.heavenlyStem;
        }

        return Object.keys(flowInfo).length > 0 ? flowInfo : undefined;
    };

    const gridLayout = [
        [5, 6, 7, 8],
        [4, -1, -1, 9],
        [3, -1, -1, 10],
        [2, 1, 0, 11],
    ];

    const lifePalaceBranch = canonicalChart.十二宫位.find((p) => p.宫位 === '命宫')?.干支.slice(-1) || '';
    const bodyPalaceBranch = canonicalChart.十二宫位.find((p) => p.是否身宫 === '是')?.干支.slice(-1) || '';
    return (
        <div className="w-full">
            {/* 工具栏 */}
            <div className="flex justify-end gap-2 mb-2 md:pr-0 pr-3">
                <button
                    onClick={handleCopy}
                    className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs transition-colors ${copied
                        ? 'bg-green-500/10 text-green-500'
                        : 'bg-background-secondary text-foreground-secondary hover:bg-background-tertiary'
                        }`}
                >
                    {copied ? '已复制' : '复制排盘'}
                </button>
                {showJsonCopy && onCopyJson && (
                    <button
                        onClick={onCopyJson}
                        className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs transition-colors ${jsonCopied
                            ? 'bg-green-500/10 text-green-500'
                            : 'bg-background-secondary text-foreground-secondary hover:bg-background-tertiary'
                            }`}
                    >
                        {jsonCopied ? 'JSON 已复制' : '复制 JSON'}
                    </button>
                )}
                <button
                    onClick={() => setShowAdjStars(!showAdjStars)}
                    className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs transition-colors ${showAdjStars
                        ? 'bg-accent/10 text-accent'
                        : 'bg-background-secondary text-foreground-secondary hover:bg-background-tertiary'
                        }`}
                >
                    {showAdjStars ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
                    {showAdjStars ? '隐藏杂曜' : '显示杂曜'}
                </button>
            </div>
            {/* 三方四正连线SVG层 */}
            <div className="relative">
                {activeSelectedPalace !== null && (
                    <svg
                        className="absolute inset-0 w-full h-full pointer-events-none z-10"
                        viewBox="0 0 100 100"
                        preserveAspectRatio="none"
                    >
                        {(() => {
                            const selectedPalaceInfo = canonicalChart.十二宫位.find((palace) => palace.宫位索引 === activeSelectedPalace);
                            if (!selectedPalaceInfo) return null;
                            // 宫位在网格中的位置映射 (branchIndex -> {row, col})
                            const positionMap: Record<number, { row: number; col: number }> = {
                                5: { row: 0, col: 0 }, 6: { row: 0, col: 1 }, 7: { row: 0, col: 2 }, 8: { row: 0, col: 3 },
                                4: { row: 1, col: 0 }, 9: { row: 1, col: 3 },
                                3: { row: 2, col: 0 }, 10: { row: 2, col: 3 },
                                2: { row: 3, col: 0 }, 1: { row: 3, col: 1 }, 0: { row: 3, col: 2 }, 11: { row: 3, col: 3 },
                            };

                            const selectedBranch = getBranchIndex(selectedPalaceInfo.干支.slice(-1));
                            const selectedPos = positionMap[selectedBranch];
                            if (!selectedPos) return null;

                            const sanFangIndexes = getTriangleSquare(activeSelectedPalace).square;
                            const cellSize = 25; // 每个宫位占25%
                            const padding = 1; // 边框内侧偏移

                            const getAnchorPoint = (pos: { row: number; col: number }) => {
                                const isTop = pos.row === 0;
                                const isBottom = pos.row === 3;
                                const isLeft = pos.col === 0;
                                const isRight = pos.col === 3;
                                const centerX = (pos.col + 0.5) * cellSize;
                                const centerY = (pos.row + 0.5) * cellSize;

                                // 角落宫：取靠近中心的角点
                                if ((isTop && isLeft) || (isTop && isRight) || (isBottom && isLeft) || (isBottom && isRight)) {
                                    const x = isLeft ? (pos.col + 1) * cellSize - padding : pos.col * cellSize + padding;
                                    const y = isTop ? (pos.row + 1) * cellSize - padding : pos.row * cellSize + padding;
                                    return { x, y };
                                }

                                // 非角落：取靠近中心的边中点
                                if (isTop) return { x: centerX, y: (pos.row + 1) * cellSize - padding };
                                if (isBottom) return { x: centerX, y: pos.row * cellSize + padding };
                                if (isLeft) return { x: (pos.col + 1) * cellSize - padding, y: centerY };
                                if (isRight) return { x: pos.col * cellSize + padding, y: centerY };

                                return { x: centerX, y: centerY };
                            };

                            const lines: React.ReactNode[] = [];
                            const startPoint = getAnchorPoint(selectedPos);
                            sanFangIndexes.forEach((palaceIdx, i) => {
                                if (palaceIdx === activeSelectedPalace) return;
                                const palaceInfo = canonicalChart.十二宫位.find((palace) => palace.宫位索引 === palaceIdx);
                                if (!palaceInfo) return;
                                const branch = getBranchIndex(palaceInfo.干支.slice(-1));
                                const targetPos = positionMap[branch];
                                if (!targetPos) return;

                                const from = startPoint;
                                const to = getAnchorPoint(targetPos);

                                lines.push(
                                    <line
                                        key={i}
                                        x1={`${from.x}%`}
                                        y1={`${from.y}%`}
                                        x2={`${to.x}%`}
                                        y2={`${to.y}%`}
                                        stroke="#b8bec8"
                                        strokeWidth="0.8"
                                        strokeOpacity="0.6"
                                    />
                                );
                            });
                            return lines;
                        })()}
                    </svg>
                )}

                <div className="grid grid-cols-4 gap-0.5 sm:gap-2 w-full sm:max-w-none mx-auto">
                    {gridLayout.map((row, rowIdx) =>
                        row.map((branchIdx, colIdx) => {
                            if (branchIdx === -1) {
                                if (rowIdx === 1 && colIdx === 1) {
                                    return (
                                        <div
                                            key={`center-${rowIdx}-${colIdx}`}
                                            className="col-span-2 row-span-2 p-1 rounded-lg bg-gradient-to-br from-background-secondary to-background border border-border"
                                        >
                                            <div className="h-full flex flex-col justify-center text-sm space-y-1.5">
                                                {/* 四柱信息 - 五行着色 */}
                                                <div className="grid grid-cols-4 gap-0.5 text-center text-xs">
                                                    <div>
                                                        <div className="text-foreground-secondary text-[10px]">年柱</div>
                                                        <div className="font-semibold">
                                                            <span style={getStemElementStyle(canonicalChart.基本信息.四柱.split(' ')[0]?.charAt(0))}>{canonicalChart.基本信息.四柱.split(' ')[0]?.charAt(0) || '*'}</span>
                                                            <span style={getBranchElementStyle(canonicalChart.基本信息.四柱.split(' ')[0]?.charAt(1))}>{canonicalChart.基本信息.四柱.split(' ')[0]?.charAt(1) || '*'}</span>
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <div className="text-foreground-secondary text-[10px]">月柱</div>
                                                        <div className="font-semibold">
                                                            <span style={getStemElementStyle(canonicalChart.基本信息.四柱.split(' ')[1]?.charAt(0))}>{canonicalChart.基本信息.四柱.split(' ')[1]?.charAt(0) || '*'}</span>
                                                            <span style={getBranchElementStyle(canonicalChart.基本信息.四柱.split(' ')[1]?.charAt(1))}>{canonicalChart.基本信息.四柱.split(' ')[1]?.charAt(1) || '*'}</span>
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <div className="text-foreground-secondary text-[10px]">日柱</div>
                                                        <div className="font-semibold">
                                                            <span style={getStemElementStyle(canonicalChart.基本信息.四柱.split(' ')[2]?.charAt(0))}>{canonicalChart.基本信息.四柱.split(' ')[2]?.charAt(0) || '*'}</span>
                                                            <span style={getBranchElementStyle(canonicalChart.基本信息.四柱.split(' ')[2]?.charAt(1))}>{canonicalChart.基本信息.四柱.split(' ')[2]?.charAt(1) || '*'}</span>
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <div className="text-foreground-secondary text-[10px]">时柱</div>
                                                        <div className="font-semibold">
                                                            <span style={getStemElementStyle(canonicalChart.基本信息.四柱.split(' ')[3]?.charAt(0))}>{canonicalChart.基本信息.四柱.split(' ')[3]?.charAt(0) || '*'}</span>
                                                            <span style={getBranchElementStyle(canonicalChart.基本信息.四柱.split(' ')[3]?.charAt(1))}>{canonicalChart.基本信息.四柱.split(' ')[3]?.charAt(1) || '*'}</span>
                                                        </div>
                                                    </div>
                                                </div>

                                                <div className="border-t border-border my-1" />

                                                <div className="flex justify-center gap-2 text-xs">
                                                    <span className="text-foreground-secondary">阳历</span>
                                                    <span>{canonicalChart.基本信息.阳历}</span>
                                                </div>
                                                <div className="flex justify-center gap-2 text-xs">
                                                    <span className="text-foreground-secondary">农历</span>
                                                    <span>{canonicalChart.基本信息.农历}</span>
                                                </div>

                                                <div className="border-t border-border my-1" />

                                                <div className="flex justify-center gap-4 text-xs">
                                                    <span>命主：<span className="font-semibold text-purple-500">{canonicalChart.基本信息.命主}</span></span>
                                                    <span>身主：<span className="font-semibold">{canonicalChart.基本信息.身主}</span></span>
                                                </div>

                                                <div className="flex justify-center gap-4 text-xs">
                                                    <span>命宫：<span className="text-accent">{lifePalaceBranch}</span></span>
                                                    <span>身宫：<span className="text-amber-500">{bodyPalaceBranch}</span></span>
                                                </div>

                                                {(canonicalChart.基本信息.斗君 || canonicalChart.基本信息.命主星 || canonicalChart.基本信息.身主星) && (
                                                    <div className="flex flex-wrap justify-center gap-4 text-xs">
                                                        {canonicalChart.基本信息.斗君 && <span>斗君：<span className="font-semibold">{canonicalChart.基本信息.斗君}</span></span>}
                                                        {canonicalChart.基本信息.命主星 && <span>命主星：<span className="font-semibold">{canonicalChart.基本信息.命主星}</span></span>}
                                                        {canonicalChart.基本信息.身主星 && <span>身主星：<span className="font-semibold">{canonicalChart.基本信息.身主星}</span></span>}
                                                    </div>
                                                )}

                                                {canonicalChart.基本信息.真太阳时 && (
                                                    <div className="flex justify-center gap-2 text-xs">
                                                        <span className="text-foreground-secondary">真太阳时</span>
                                                        <span>{canonicalChart.基本信息.真太阳时.真太阳时}</span>
                                                    </div>
                                                )}

                                                <div className="text-center">
                                                    <span className="px-2 py-0.5 rounded bg-accent/10 text-accent text-xs font-medium">
                                                        {canonicalChart.基本信息.五行局}
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    );
                                }
                                return null;
                            }

                            const palace = getCanonicalPalaceByBranch(branchIdx);
                            if (!palace || typeof palace.宫位索引 !== 'number') return null;

                            const palaceIndex = palace.宫位索引;
                            const isLifePalace = palaceIndex === lifePalaceIndex;
                            const highlightTypes = getHighlightTypes(palaceIndex);
                            const isHighlighted = highlightTypes.length > 0 || sanFangSiZhengPalaces.includes(palaceIndex);
                            const flowInfo = getFlowInfoForPalace(palaceIndex);

                            return (
                                <PalaceCard
                                    key={`palace-${branchIdx}`}
                                    palace={palace}
                                    isSelected={activeSelectedPalace === palaceIndex}
                                    isLifePalace={isLifePalace}
                                    isHighlighted={isHighlighted}
                                    highlightTypes={highlightTypes}
                                    isSanFangSiZheng={sanFangSiZhengPalaces.includes(palaceIndex) && activeSelectedPalace !== palaceIndex}
                                    showAdjStars={showAdjStars}
                                    flowInfo={flowInfo}
                                    onClick={() => setSelectedPalace(
                                        activeSelectedPalace === palaceIndex ? null : palaceIndex
                                    )}
                                />
                            );
                        })
                    )}
                </div>
            </div>

        </div >
    );
}
