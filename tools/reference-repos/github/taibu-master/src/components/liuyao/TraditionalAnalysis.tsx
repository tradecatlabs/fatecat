/**
 * 传统六爻分析组件（多用神分组版）
 */
'use client';

import { useMemo, useState, type CSSProperties } from 'react';
import { ChevronDown, AlertCircle } from 'lucide-react';
import type { LiuyaoCanonicalJSON } from 'taibu-core/liuyao';
import { LIU_QIN_TIPS, SHEN_XI_TIPS } from '@/lib/divination/liuyao-term-tips';
import { KONG_WANG_LABELS } from '@/lib/divination/liuyao';

interface TraditionalAnalysisProps {
    analysis: LiuyaoCanonicalJSON;
}

function CollapsibleSection({
    title,
    children,
    defaultOpen = false,
}: {
    title: string;
    children: React.ReactNode;
    defaultOpen?: boolean;
}) {
    const [isOpen, setIsOpen] = useState(defaultOpen);

    return (
        <div className="border border-border rounded-lg overflow-hidden bg-background">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex items-center justify-between px-4 py-3 bg-[#f8f7f4] hover:bg-background-secondary transition-colors duration-150 text-sm"
            >
                <span className="font-medium text-foreground">{title}</span>
                <ChevronDown className={`w-4 h-4 text-foreground/45 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
            </button>
            <div className={`grid transition-[grid-template-rows] duration-200 ${isOpen ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'}`}>
                <div className="overflow-hidden">
                    <div className="p-4 text-sm bg-background">{children}</div>
                </div>
            </div>
        </div>
    );
}

// 天干对应五行
const tianGanWuXing: Record<string, string> = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
};

// 地支对应五行
const diZhiWuXing: Record<string, string> = {
    '寅': '木', '卯': '木',
    '巳': '火', '午': '火',
    '辰': '土', '戌': '土', '丑': '土', '未': '土',
    '申': '金', '酉': '金',
    '亥': '水', '子': '水',
};

const wuXingColorValues: Record<string, string> = {
    '金': '#FFD700',
    '木': '#228B22',
    '水': '#1E90FF',
    '火': '#FF4500',
    '土': '#8B4513',
};

const YAO_NAMES = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻'];

function getWuXingStyle(wuXing: string | undefined): CSSProperties | undefined {
    const color = wuXing ? wuXingColorValues[wuXing] : undefined;
    return color ? { color } : undefined;
}

function getGanStyle(gan: string): CSSProperties | undefined {
    const wuXing = tianGanWuXing[gan] || '';
    return getWuXingStyle(wuXing);
}

function getZhiStyle(zhi: string): CSSProperties | undefined {
    const wuXing = diZhiWuXing[zhi] || '';
    return getWuXingStyle(wuXing);
}

function getMovementTone(state?: string): string {
    if (state === 'changing') return 'text-red-500';
    if (state === 'hidden_moving') return 'text-amber-500';
    if (state === 'day_break') return 'text-orange-500';
    return '';
}

function getPositionLabel(position?: string | number): string {
    if (typeof position === 'string' && position.trim()) return position;
    if (typeof position !== 'number') return '未定位';
    return YAO_NAMES[position - 1] ?? `第${position}爻`;
}

function getCandidateSourceLabel(source?: string): string | null {
    if (source === 'changed') return '变出';
    if (source === 'fushen') return '伏神';
    if (source === 'temporal') return '时空';
    if (source === 'visible') return '显爻';
    return null;
}

export function TraditionalAnalysis({
    analysis,
}: TraditionalAnalysisProps) {
    const movementStats = useMemo(() => {
        let changing = 0;
        let hiddenMoving = 0;
        let dayBreak = 0;
        let staticCount = 0;
        let withShenSha = 0;

        for (const yao of analysis.六爻) {
            switch (yao.动静状态) {
                case 'changing':
                    changing += 1;
                    break;
                case 'hidden_moving':
                    hiddenMoving += 1;
                    break;
                case 'day_break':
                    dayBreak += 1;
                    break;
                default:
                    staticCount += 1;
                    break;
            }

            if (Array.isArray(yao.神煞) && yao.神煞.length > 0) {
                withShenSha += 1;
            }
        }

        return { changing, hiddenMoving, dayBreak, staticCount, withShenSha };
    }, [analysis.六爻]);

    const totalRecommendations = useMemo(
        () => analysis.用神分析.reduce((sum, group) => sum + (group.应期提示?.length || 0), 0),
        [analysis.用神分析]
    );

    const fuShenHints = useMemo(() => {
        return analysis.六爻
            .filter((yao) => yao.伏神)
            .map((yao) => `${yao.伏神?.六亲}伏于${yao.爻位}下`);
    }, [analysis.六爻]);

    return (
        <div className="mx-auto w-full max-w-3xl space-y-4">
            {analysis.干支时间.length > 0 && (
                <div className="space-y-1.5">
                    <div className="overflow-x-auto">
                        <div className="min-w-max overflow-hidden rounded-lg border border-border bg-background shadow-sm">
                            <table className="w-full text-xs text-center">
                                <tbody className="divide-y divide-gray-200">
                                    <tr className="divide-x divide-gray-200">
                                        <td className="px-4 py-2 bg-[#f8f7f4] text-[#2eaadc] font-semibold whitespace-nowrap">干支</td>
                                        {analysis.干支时间.map((pillar) => {
                                            return (
                                                <td key={pillar.柱} className="px-4 py-2 whitespace-nowrap">
                                                    <span className="font-medium">
                                                        <span style={getGanStyle(pillar.干支.charAt(0))}>{pillar.干支.charAt(0)}</span>
                                                        <span style={getZhiStyle(pillar.干支.charAt(1))}>{pillar.干支.charAt(1)}</span>
                                                        <span className="text-foreground/55">{pillar.柱}</span>
                                                    </span>
                                                </td>
                                            );
                                        })}
                                    </tr>
                                    <tr className="divide-x divide-gray-200">
                                        <td className="px-4 py-2 bg-[#f8f7f4] text-[#2eaadc] font-semibold whitespace-nowrap">空亡</td>
                                        {analysis.干支时间.map((pillar) => {
                                            return (
                                                <td
                                                    key={pillar.柱}
                                                    className="px-4 py-2 whitespace-nowrap"
                                                >
                                                    {pillar.空亡.length > 0 ? (
                                                        <span className="tracking-wide">
                                                            <span style={getZhiStyle(pillar.空亡[0])}>{pillar.空亡[0]}</span>
                                                            <span style={getZhiStyle(pillar.空亡[1])}>{pillar.空亡[1]}</span>
                                                        </span>
                                                    ) : (
                                                        <span className="text-foreground-tertiary">-</span>
                                                    )}
                                                </td>
                                            );
                                        })}
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div className="text-[10px] text-foreground/35">
                        {'注：六爻断卦判空亡以"日旬空"为主，年/月/时旬空供参考。'}
                    </div>
                </div>
            )}

            <div className="rounded-lg border border-border bg-background px-4 py-4 shadow-sm">
                <div className="grid gap-4 lg:grid-cols-[1.2fr_1fr]">
                    <div className="space-y-3">
                        {(analysis.卦盘.互卦 || analysis.卦盘.错卦 || analysis.卦盘.综卦 || analysis.卦盘.卦身) && (
                            <div className="space-y-2 text-xs text-foreground/60">
                                <div className="text-[10px] font-semibold uppercase tracking-[0.24em] text-foreground/30">衍生卦象</div>
                                <div className="space-y-1">
                                    <div>互卦：{analysis.卦盘.互卦?.卦名 || '无'}</div>
                                    <div>错卦：{analysis.卦盘.错卦?.卦名 || '无'}</div>
                                    <div>综卦：{analysis.卦盘.综卦?.卦名 || '无'}</div>
                                    <div>
                                        卦身：
                                        {analysis.卦盘.卦身
                                            ? `${analysis.卦盘.卦身.地支}${analysis.卦盘.卦身.位置 ? `（${analysis.卦盘.卦身.位置}）` : ''}${analysis.卦盘.卦身.状态 ? `（${analysis.卦盘.卦身.状态}）` : ''}`
                                            : '无'}
                                    </div>
                                </div>
                            </div>
                        )}

                        {analysis.卦级分析.length > 0 && (
                            <div className="space-y-2 text-xs text-foreground/60">
                                <div className="text-[10px] font-semibold uppercase tracking-[0.24em] text-foreground/30">卦级分析</div>
                                <div className="space-y-1.5">
                                    {analysis.卦级分析.map((line, index) => (
                                        <div key={`${line}-${index}`}>{line}</div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="space-y-3 border-t border-border/60 pt-3 lg:border-t-0 lg:border-l lg:border-border/60 lg:pl-4 lg:pt-0">
                        <div className="text-[10px] font-semibold uppercase tracking-[0.24em] text-foreground/30">关键信号</div>
                        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
                            {movementStats.changing > 0 && (
                                <span className="text-red-500 font-medium">明动 {movementStats.changing}</span>
                            )}
                            {movementStats.hiddenMoving > 0 && (
                                <span className="text-amber-500 font-medium">暗动 {movementStats.hiddenMoving}</span>
                            )}
                            {movementStats.dayBreak > 0 && (
                                <span className="text-orange-500 font-medium">日破 {movementStats.dayBreak}</span>
                            )}
                            <span className="text-foreground/35">静爻 {movementStats.staticCount}</span>
                            <span className="text-foreground/25">|</span>
                            <span className="text-foreground/55">用神 {analysis.用神分析.length}</span>
                            <span className="text-foreground/55">应期 {totalRecommendations}</span>
                        </div>
                        {(analysis.全局神煞?.length || 0) > 0 && (
                            <div className="text-xs text-foreground/55">
                                全局神煞：{analysis.全局神煞?.join(' ')}
                            </div>
                        )}
                        {fuShenHints.length > 0 && (
                            <div className="text-xs text-orange-600">
                                伏神：{fuShenHints.join('；')}
                            </div>
                        )}
                        {analysis.提示.length > 0 && (
                            <div className="flex items-start gap-1.5 text-xs">
                                <AlertCircle className="w-3.5 h-3.5 text-red-400 shrink-0 mt-0.5" />
                                <span className="text-foreground/55">{analysis.提示.join('；')}</span>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {analysis.用神分析.length > 0 && (
                <div className="rounded-lg border border-border bg-background shadow-sm divide-y divide-border/60 overflow-hidden">
                    {analysis.用神分析.map((group, groupIndex) => {
                        const selectedSourceLabel = getCandidateSourceLabel(group.已选用神.来源);
                        const selectedKongState = group.已选用神.空亡状态;
                        const selectedKongLabel = selectedKongState && selectedKongState !== 'not_kong'
                            ? KONG_WANG_LABELS[selectedKongState as keyof typeof KONG_WANG_LABELS] || selectedKongState
                            : '';
                        return (
                            <div key={group.目标六亲} className="px-4 py-4 text-xs">
                                <div className="flex flex-wrap items-center gap-2 mb-2">
                                    <span className="font-bold text-[#2eaadc] text-sm" title={LIU_QIN_TIPS[group.目标六亲]}>{group.目标六亲}</span>
                                    {groupIndex === 0 && (
                                        <span className="px-1.5 py-0.5 rounded border border-[#2eaadc]/20 bg-[#2eaadc]/10 text-[#2eaadc] text-[10px] leading-none">主</span>
                                    )}
                                    <span className="text-foreground/35">{group.取用状态}</span>
                                </div>

                                <div className="grid gap-2 md:grid-cols-2">
                                    <div className="text-foreground/55">
                                        <span className="text-foreground/35">用神：</span>
                                        <span className="text-foreground font-medium" title={LIU_QIN_TIPS[group.已选用神.六亲]}>{group.已选用神.六亲}</span>
                                        {group.已选用神.爻位 && <span>{' @'}{getPositionLabel(group.已选用神.爻位)}</span>}
                                        {group.已选用神.是否世爻 && <span className="text-[#2eaadc]">{' · 世位'}</span>}
                                        {group.已选用神.是否应爻 && <span className="text-blue-500">{' · 应位'}</span>}
                                        {selectedSourceLabel && <span className="text-foreground/35">{` · ${selectedSourceLabel}`}</span>}
                                    </div>

                                    <div className="text-foreground/55">
                                        <span className="text-foreground/35">状态：</span>
                                        <span className={getMovementTone(group.已选用神.动静状态)}>{group.已选用神.动静}</span>
                                        <span>{' · '}{group.已选用神.强弱}</span>
                                        {group.已选用神.纳甲 && group.已选用神.五行 && <span>{` · ${group.已选用神.纳甲}${group.已选用神.五行}`}</span>}
                                        {selectedKongLabel && <span className="text-orange-500">{` · ${selectedKongLabel}`}</span>}
                                    </div>

                                    {(group.神煞系统?.原神 || group.神煞系统?.忌神 || group.神煞系统?.仇神) && (
                                        <div className="text-foreground/55 md:col-span-2">
                                            <span className="text-foreground/35">神系：</span>
                                            {[
                                                group.神煞系统?.原神 && <span key="yuan" className="text-green-500" title={SHEN_XI_TIPS['原神']}>{'原神'}{group.神煞系统.原神}</span>,
                                                group.神煞系统?.忌神 && <span key="ji" className="text-red-500" title={SHEN_XI_TIPS['忌神']}>{'忌神'}{group.神煞系统.忌神}</span>,
                                                group.神煞系统?.仇神 && <span key="chou" className="text-orange-500" title={SHEN_XI_TIPS['仇神']}>{'仇神'}{group.神煞系统.仇神}</span>,
                                            ].filter(Boolean).map((node, i) => <span key={i}>{i > 0 && ' · '}{node}</span>)}
                                        </div>
                                    )}

                                    {group.已选用神.依据 && group.已选用神.依据.length > 0 && (
                                        <div className="text-foreground/55 md:col-span-2">
                                            <span className="text-foreground/35">判据：</span>
                                            {group.已选用神.依据.join('、')}
                                        </div>
                                    )}

                                    {group.取用说明 && (
                                        <div className="text-foreground/55 md:col-span-2">
                                            <span className="text-foreground/35">取用：</span>
                                            {group.取用说明}
                                        </div>
                                    )}

                                    {group.候选用神 && group.候选用神.length > 0 && (
                                        <div className="text-foreground/45 md:col-span-2">
                                            <span className="text-foreground/35">{`候选（${group.候选用神.length}）：`}</span>
                                            {group.候选用神.map((c) => {
                                                const sourceLabel = getCandidateSourceLabel(c.来源);
                                                return `${c.六亲}@${getPositionLabel(c.爻位)}${sourceLabel ? `(${sourceLabel})` : ''}`;
                                            }).join('、')}
                                        </div>
                                    )}

                                    {group.应期提示 && group.应期提示.length > 0 && (
                                        <div className="text-foreground/55 md:col-span-2">
                                            <span className="text-foreground/35">近期应期：</span>
                                            {group.应期提示.slice(0, 2).map((rec) => `${rec.触发}${rec.依据.length > 0 ? `（${rec.依据.join('、')}）` : ''} ${rec.说明}`).join('；')}
                                        </div>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}

            {(analysis.卦盘.本卦.卦辞 || analysis.卦盘.本卦.象辞 || analysis.卦盘.变卦?.动爻爻辞?.length) && (
                <CollapsibleSection title="卦辞象辞" defaultOpen={false}>
                    <div className="space-y-2">
                        {analysis.卦盘.本卦.卦辞 && (
                            <div>
                                <span className="text-foreground/45">卦辞：</span>
                                <span className="text-foreground">{analysis.卦盘.本卦.卦辞}</span>
                            </div>
                        )}
                        {analysis.卦盘.本卦.象辞 && (
                            <div>
                                <span className="text-foreground/45">象曰：</span>
                                <span className="text-foreground italic">{analysis.卦盘.本卦.象辞}</span>
                            </div>
                        )}

                        {analysis.卦盘.变卦?.动爻爻辞 && analysis.卦盘.变卦.动爻爻辞.length > 0 && (
                            <div className="mt-2 pt-2 border-t border-border/60">
                                <div className="text-foreground/45 mb-1">变爻爻辞：</div>
                                {analysis.卦盘.变卦.动爻爻辞.map((yaoText) => {
                                    return (
                                        <div
                                            key={`${yaoText.爻名}-${yaoText.爻辞}`}
                                            className="p-2 rounded border-l-2 mb-1 border-l-[#2eaadc] bg-sky-50/40"
                                        >
                                            <span className="font-medium text-foreground">{yaoText.爻名}：</span>
                                            <span className="text-foreground/55">{yaoText.爻辞}</span>
                                        </div>
                                    );
                                })}
                            </div>
                        )}

                        {analysis.卦盘.变卦 && (
                            <div className="mt-2 pt-2 border-t border-border/60">
                                {analysis.卦盘.变卦.卦辞 && (
                                    <div>
                                        <span className="text-foreground/45">变卦 {analysis.卦盘.变卦.卦名} 卦辞：</span>
                                        <span className="text-foreground">{analysis.卦盘.变卦.卦辞}</span>
                                    </div>
                                )}
                                {analysis.卦盘.变卦.象辞 && (
                                    <div className="mt-1">
                                        <span className="text-foreground/45">变卦象曰：</span>
                                        <span className="text-foreground italic">{analysis.卦盘.变卦.象辞}</span>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </CollapsibleSection>
            )}

        </div>
    );
}
