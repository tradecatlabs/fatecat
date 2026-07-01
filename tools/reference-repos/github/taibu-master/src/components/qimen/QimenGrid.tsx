/**
 * 奇门遁甲九宫格组件
 *
 * 'use client' 标记说明：
 * - 需要在客户端渲染交互式九宫格
 */
'use client';

import type { QimenPalaceJSON } from 'taibu-core/qimen';

/** 五行旺衰颜色映射 */
const PHASE_COLORS: Record<string, string> = {
    '旺': 'text-green-500',
    '相': 'text-red-500',
    '休': 'text-blue-500',
    '囚': 'text-amber-500',
    '死': 'text-stone-500',
};

/** 天干五行映射 */
const STEM_ELEMENT: Record<string, string> = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
};

/** 根据天干获取五行颜色 class */
function getStemColorClass(stem: string, monthPhase: Record<string, string>): string {
    const stemKey = stem.charAt(0);
    const phase = monthPhase[stemKey];
    if (phase && PHASE_COLORS[phase]) return PHASE_COLORS[phase];
    // fallback: 按五行固定色
    const el = STEM_ELEMENT[stemKey];
    if (el === '木') return 'text-green-500';
    if (el === '火') return 'text-red-500';
    if (el === '土') return 'text-stone-500';
    if (el === '金') return 'text-amber-500';
    if (el === '水') return 'text-blue-500';
    return 'text-foreground-secondary';
}

/** 洛书九宫排列顺序（左上→右下，3x3） */
const LUOSHU_ORDER = [4, 9, 2, 3, 5, 7, 8, 1, 6];

interface QimenGridProps {
    palaces: QimenPalaceJSON[];
    monthPhaseMap?: Record<string, string>;
    ju: string;
}

function PalaceCell({
    palace,
    monthPhaseMap,
    isCenterPalace,
    ju,
}: {
    palace: QimenPalaceJSON;
    monthPhaseMap?: Record<string, string>;
    isCenterPalace: boolean;
    ju: string;
}) {
    if (isCenterPalace) {
        const juMatch = ju.match(/^(.*?)(\d+)局$/u);
        const juPrefix = juMatch?.[1] || ju;
        const juValue = juMatch?.[2] ? `${juMatch[2]}局` : '';
        return (
            <div className="flex flex-col items-center justify-center h-full gap-1 text-foreground-secondary">
                <span className="text-xs opacity-60">{juPrefix}</span>
                <span className="text-lg font-bold text-foreground">{juValue || ju}</span>
                <span className="text-xs opacity-60">中五宫</span>
            </div>
        );
    }

    const earthColor = getStemColorClass(palace.地盘天干, monthPhaseMap || {});
    const heavenColor = getStemColorClass(palace.天盘天干, monthPhaseMap || {});

    return (
        <div className="flex flex-col h-full gap-1.5 pt-4 pb-2 px-1.5 md:px-2.5 md:pt-4 md:pb-2.5">
            {/* 格局标注 */}
            <div className="min-h-[1.75rem] md:min-h-[2.25rem]">
                {palace.格局 && palace.格局.length > 0 && (
                    <span className="text-[9px] md:text-[11px] text-purple-400/90 break-words leading-snug">
                        {palace.格局.join('、')}
                    </span>
                )}
            </div>
            {/* 地盘天干 + 八神 */}
            <div className="flex items-center justify-between">
                <span className={`text-sm md:text-base font-medium ${earthColor}`}>
                    {palace.地盘天干}
                </span>
                <span className="text-[10px] md:text-xs text-foreground-secondary">
                    {palace.八神}
                </span>
            </div>
            {/* 九星 + 天盘天干 */}
            <div className="flex items-center justify-between">
                <span className="text-xs md:text-sm text-foreground-secondary">
                    {palace.九星}
                </span>
                <span className={`text-sm md:text-base font-medium ${heavenColor}`}>
                    {palace.天盘天干}
                </span>
            </div>
            {/* 八门 */}
            <div className="flex items-center justify-between">
                <span className="text-xs md:text-sm text-foreground-secondary">
                    {palace.八门}
                </span>
            </div>
            {/* 星五行 / 门五行 / 宫五行 */}
            <div className="flex items-center justify-between text-[10px] md:text-[11px] text-foreground-tertiary">
                <span>星{palace.九星五行 || '-'}</span>
                <span>门{palace.八门五行 || '-'}</span>
            </div>
            <div className="text-[10px] md:text-[11px] text-foreground-tertiary">
                宫{palace.宫位五行 || '-'}{palace.宫旺衰 ? `·${palace.宫旺衰}` : ''}
            </div>
            {/* 空亡/驿马标记 */}
            {(palace.宫位状态.includes('日空') || palace.宫位状态.includes('时空') || palace.宫位状态.includes('驿马')) && (
                <div className="flex items-center gap-1 mt-auto">
                    {(palace.宫位状态.includes('日空') || palace.宫位状态.includes('时空')) && (
                        <span className="text-[10px] text-amber-400" title="空亡">◎</span>
                    )}
                    {palace.宫位状态.includes('驿马') && (
                        <span className="text-[10px] text-cyan-400" title="驿马">马</span>
                    )}
                </div>
            )}
        </div>
    );
}

export function QimenGrid({ palaces, monthPhaseMap, ju }: QimenGridProps) {
    const palaceMap = new Map(palaces.map(p => [p.宫位序号, p]));

    return (
        <div className="grid grid-cols-3 gap-[1px] bg-border/40 rounded-xl overflow-hidden border-border/60">
            {LUOSHU_ORDER.map((num) => {
                const palace = palaceMap.get(num);
                if (!palace) return <div key={num} />;
                const isCenterPalace = num === 5;
                return (
                    <div
                        key={num}
                        className="bg-background min-h-[100px] md:min-h-[140px] relative"
                    >
                        {/* 宫名角标 */}
                        <span className="absolute top-0.5 left-1 text-[9px] md:text-[10px] text-foreground-tertiary/60">
                            {palace.宫名}
                        </span>
                        <PalaceCell
                            palace={palace}
                            monthPhaseMap={monthPhaseMap}
                            isCenterPalace={isCenterPalace}
                            ju={ju}
                        />
                    </div>
                );
            })}
        </div>
    );
}
