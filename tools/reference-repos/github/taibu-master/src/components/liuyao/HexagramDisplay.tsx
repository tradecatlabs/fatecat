/**
 * 卦象显示组件
 *
 * 显示完整的六爻卦象，从下到上排列
 * 支持传统六爻分析标签（六亲/六神/世应/用神）
 * 整合旺衰、空亡等详细信息
 */
'use client';

import { useMemo, useState } from 'react';
import type { LiuyaoYaoJSON } from 'taibu-core/liuyao';
import {
    type Yao,
    type Hexagram,
    type FullYaoInfo,
    type FullYaoInfoExtended,
    getHexagramBrief,
    WANG_SHUAI_LABELS,
    KONG_WANG_LABELS,
} from '@/lib/divination/liuyao';
import { YaoLine } from '@/components/liuyao/YaoLine';

// 静态常量提取到组件外部，避免每次渲染重新创建
const YAO_LABELS = ['初', '二', '三', '四', '五', '上'];
const ROW_HEIGHT = 'h-5';
const LIU_SHEN_COLORS: Record<string, string> = {
    '青龙': 'text-green-500',
    '朱雀': 'text-red-500',
    '勾陈': 'text-yellow-600',
    '螣蛇': 'text-purple-500',
    '白虎': 'text-gray-400',
    '玄武': 'text-blue-500',
};

interface HexagramDisplayProps {
    yaos: Yao[];
    hexagram: Hexagram;
    changedHexagram?: Hexagram;
    changedLines?: number[];
    showDetails?: boolean;
    size?: 'sm' | 'md' | 'lg';
    fullYaos?: FullYaoInfo[] | FullYaoInfoExtended[] | LiuyaoYaoJSON[];
    showTraditional?: boolean;
    yongShenPositions?: number[];
}

export function HexagramDisplay({
    yaos,
    hexagram,
    changedHexagram,
    changedLines = [],
    showDetails = true,
    size = 'md',
    fullYaos,
    showTraditional = false,
    yongShenPositions = [],
}: HexagramDisplayProps) {
    // 使用 useMemo 缓存计算结果，避免每次渲染重新计算
    const displayYaos = useMemo(() => [...yaos].reverse(), [yaos]);
    const displayFullYaos = useMemo(() => fullYaos ? [...fullYaos].reverse() : undefined, [fullYaos]);
    const getYaoShenSha = (yao: FullYaoInfo | FullYaoInfoExtended | LiuyaoYaoJSON | undefined): string[] => {
        if (!yao) return [];
        if ('神煞' in yao && Array.isArray(yao.神煞)) return yao.神煞;
        if ('shenSha' in yao && Array.isArray(yao.shenSha)) return yao.shenSha;
        return [];
    };
    const normalizePosition = (position: unknown): number | null => {
        if (typeof position === 'number') return position;
        if (typeof position !== 'string') return null;
        if (position.includes('初')) return 1;
        if (position.includes('二')) return 2;
        if (position.includes('三')) return 3;
        if (position.includes('四')) return 4;
        if (position.includes('五')) return 5;
        if (position.includes('上')) return 6;
        return null;
    };
    const getYaoPosition = (yao: FullYaoInfo | FullYaoInfoExtended | LiuyaoYaoJSON | undefined): string | number | undefined => {
        if (!yao) return undefined;
        if ('爻位' in yao) return yao.爻位;
        if ('position' in yao) return yao.position;
        return undefined;
    };
    const getYaoLiuQin = (yao: FullYaoInfo | FullYaoInfoExtended | LiuyaoYaoJSON | undefined): string => {
        if (!yao) return '';
        if ('六亲' in yao) return yao.六亲;
        if ('liuQin' in yao) return yao.liuQin;
        return '';
    };
    const getYaoNaJia = (yao: FullYaoInfo | FullYaoInfoExtended | LiuyaoYaoJSON | undefined): string => {
        if (!yao) return '';
        if ('纳甲' in yao) return yao.纳甲;
        if ('naJia' in yao) return yao.naJia;
        return '';
    };
    const getYaoWuXing = (yao: FullYaoInfo | FullYaoInfoExtended | LiuyaoYaoJSON | undefined): string => {
        if (!yao) return '';
        if ('五行' in yao) return yao.五行;
        if ('wuXing' in yao) return yao.wuXing;
        return '';
    };
    const getYaoLiuShen = (yao: FullYaoInfo | FullYaoInfoExtended | LiuyaoYaoJSON | undefined): string => {
        if (!yao) return '';
        if ('六神' in yao) return yao.六神;
        if ('liuShen' in yao) return yao.liuShen;
        return '';
    };
    const getYaoShiYing = (yao: LiuyaoYaoJSON | undefined): string | undefined => yao?.世应;
    const getYaoWangShuai = (yao: LiuyaoYaoJSON | undefined): string | undefined => yao?.旺衰;
    const getYaoKongWang = (yao: LiuyaoYaoJSON | undefined): string | undefined => yao?.空亡;

    // 检查是否有扩展信息
    const hasExtendedInfo = useMemo(() =>
        displayFullYaos && displayFullYaos.length > 0 && 'strength' in displayFullYaos[0],
        [displayFullYaos]
    );
    const hasYaoShenSha = useMemo(() =>
        Boolean(displayFullYaos?.some((yao) => getYaoShenSha(yao).length > 0)),
        [displayFullYaos]
    );
    const [expandedShenShaRows, setExpandedShenShaRows] = useState<Set<number>>(new Set());

    const toggleShenShaRow = (position: number) => {
        setExpandedShenShaRows((prev) => {
            const next = new Set(prev);
            if (next.has(position)) {
                next.delete(position);
            } else {
                next.add(position);
            }
            return next;
        });
    };

    return (
        <div className="flex flex-col items-center gap-4">
            {/* 卦象 */}
            <div className="flex flex-col md:flex-row gap-8 items-center md:items-start">
                {/* 本卦 */}
                <div className="flex flex-col items-center" data-hexagram="base">
                    {/* 卦名 */}
                    <div className="text-center mb-3 space-y-1">
                        <span className="text-[10px] font-semibold uppercase tracking-[0.2em] text-foreground/35">本卦</span>
                        <h3 className="text-lg font-semibold text-foreground">
                            {hexagram.name}
                        </h3>
                        <p className="text-xs text-foreground/45">
                            {hexagram.upperTrigram}/{hexagram.lowerTrigram} · {hexagram.element}
                        </p>
                    </div>

                    {/* 爻表格 - 整合所有信息 */}
                    <div className="overflow-hidden rounded-lg">
                        <table className="text-xs text-foreground/80">
                            <tbody>
                                {displayYaos.map((yao, index) => {
                                    const fullYao = displayFullYaos?.[index];
                                    const extYao = fullYao as FullYaoInfoExtended | undefined;
                                    const canonicalYao = fullYao as LiuyaoYaoJSON | undefined;
                                    const normalizedPosition = normalizePosition(getYaoPosition(fullYao));
                                    const isYongShen = typeof normalizedPosition === 'number' ? yongShenPositions.includes(normalizedPosition) : false;
                                    const isChanging = yao.change === 'changing';
                                    const yaoShenSha = getYaoShenSha(fullYao);
                                    const isShenShaExpanded = expandedShenShaRows.has(yao.position);
                                    const primaryShenSha = yaoShenSha[0];
                                    const remainingShenShaCount = Math.max(0, yaoShenSha.length - 1);

                                    return (
                                        <tr
                                            key={yao.position}
                                            className={`border-b border-border/60 last:border-b-0 ${isYongShen ? 'bg-sky-50/60' : ''} ${isChanging ? 'bg-red-50/70' : ''}`}
                                        >
                                            {/* 爻位 */}
                                            <td className={`px-2 py-2 text-center text-sm ${isChanging ? 'text-red-500 font-semibold' : 'text-foreground/45'}`}>
                                                {YAO_LABELS[yao.position - 1]}
                                                {isChanging && '○'}
                                            </td>

                                            {/* 六亲 + 用神标记 */}
                                            {showTraditional && fullYao && (
                                                <td className={`px-2 py-2 text-center ${isYongShen ? 'text-[#2eaadc] font-bold' : 'text-foreground'}`}>
                                                    {getYaoLiuQin(fullYao)}
                                                    {isYongShen && <span className="text-[#2eaadc] ml-0.5">★</span>}
                                                </td>
                                            )}

                                            {/* 纳甲 + 五行 */}
                                            {showTraditional && fullYao && (
                                                <td className="px-2 py-2 text-center text-foreground/55">
                                                    {getYaoNaJia(fullYao)}{getYaoWuXing(fullYao)}
                                                </td>
                                            )}

                                            {/* 卦象 */}
                                            <td className="px-3 py-2">
                                                <div className={`flex items-center justify-center ${ROW_HEIGHT}`}>
                                                    <YaoLine yao={yao} size={size} />
                                                </div>
                                            </td>

                                            {/* 世应 */}
                                            {showTraditional && fullYao && (
                                                <td className="px-1 py-2 text-center w-5">
                                                    {('isShiYao' in fullYao && fullYao.isShiYao) || getYaoShiYing(canonicalYao) === '世' ? <span className="text-[#2eaadc] font-bold">世</span> : null}
                                                    {('isYingYao' in fullYao && fullYao.isYingYao) || getYaoShiYing(canonicalYao) === '应' ? <span className="text-blue-500 font-bold">应</span> : null}
                                                </td>
                                            )}

                                            {/* 六神 */}
                                            {showTraditional && fullYao && (
                                                <td className={`px-2 py-2 text-center ${LIU_SHEN_COLORS[getYaoLiuShen(fullYao)] || 'text-foreground/45'}`}>
                                                    {getYaoLiuShen(fullYao)}
                                                </td>
                                            )}

                                            {/* 旺衰 + 空亡 (扩展信息) */}
                                            {showTraditional && hasExtendedInfo && extYao?.strength && (
                                                <td className="px-1.5 py-1 text-center">
                                                    <span className={extYao.strength.isStrong ? 'text-green-500' : 'text-red-500'}>
                                                        {WANG_SHUAI_LABELS[extYao.strength.wangShuai]}
                                                    </span>
                                                    {extYao.kongWangState !== 'not_kong' && (
                                                        <span className="text-red-400 ml-1">
                                                            {KONG_WANG_LABELS[extYao.kongWangState]}
                                                        </span>
                                                    )}
                                                </td>
                                            )}
                                            {showTraditional && !hasExtendedInfo && canonicalYao && (
                                                <td className="px-2 py-2 text-center">
                                                    <span>{getYaoWangShuai(canonicalYao)}</span>
                                                    {getYaoKongWang(canonicalYao) && (
                                                        <span className="text-red-400 ml-1">{getYaoKongWang(canonicalYao)}</span>
                                                    )}
                                                </td>
                                            )}

                                            {/* 神煞 */}
                                            {showTraditional && hasYaoShenSha && (
                                                <td className="px-1.5 py-2 text-left text-[10px] text-foreground/45">
                                                    {yaoShenSha.length > 0 ? (
                                                        <div className="flex items-center gap-1.5">
                                                            <span className="leading-4">
                                                                {isShenShaExpanded ? yaoShenSha.join('、') : primaryShenSha}
                                                            </span>
                                                            {remainingShenShaCount > 0 && (
                                                                <button
                                                                    type="button"
                                                                    onClick={() => toggleShenShaRow(yao.position)}
                                                                    className="shrink-0 px-1 py-0.5 rounded border border-border text-[10px] text-foreground/40 hover:text-foreground hover:bg-background-secondary transition-colors"
                                                                >
                                                                    {isShenShaExpanded ? '收起' : `+${remainingShenShaCount}`}
                                                                </button>
                                                            )}
                                                        </div>
                                                    ) : (
                                                        <span className="text-foreground/25">-</span>
                                                    )}
                                                </td>
                                            )}
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* 变卦 */}
                {changedHexagram && changedLines.length > 0 && (
                    <>
                        <div className="flex items-center self-center transform rotate-90 md:rotate-0">
                            <span className="text-xl text-foreground/30">→</span>
                        </div>
                        <div className="flex flex-col items-center" data-hexagram="changed">
                            {/* 卦名 */}
                            <div className="text-center mb-3 space-y-1">
                                <span className="text-[10px] font-semibold uppercase tracking-[0.2em] text-foreground/35">变卦</span>
                                <h4 className="text-lg font-semibold text-foreground">
                                    {changedHexagram.name}
                                </h4>
                                <p className="text-xs text-foreground/45">
                                    {changedHexagram.upperTrigram}/{changedHexagram.lowerTrigram} · {changedHexagram.element}
                                </p>
                            </div>

                            {/* 变卦爻表格 */}
                            <div className="overflow-hidden rounded-lg">
                                <table className="text-xs text-foreground/80">
                                    <tbody>
                                        {displayYaos.map((yao) => {
                                            const isChanged = changedLines.includes(yao.position);
                                            const changedYao: Yao = isChanged
                                                ? { ...yao, type: yao.type === 1 ? 0 : 1, change: 'stable' }
                                                : { ...yao, change: 'stable' };
                                            return (
                                                <tr key={yao.position} className="border-b border-border/60 last:border-b-0">
                                                    <td className="px-2 py-2 text-center text-sm text-foreground/45">
                                                        {YAO_LABELS[yao.position - 1]}
                                                    </td>
                                                    <td className="px-3 py-2">
                                                        <div className={`flex items-center justify-center ${ROW_HEIGHT}`}>
                                                            <YaoLine yao={changedYao} size={size} />
                                                        </div>
                                                    </td>
                                                </tr>
                                            );
                                        })}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </>
                )}
            </div>

            {/* 简要解读 */}
            {showDetails && (
                <div className="text-center max-w-md">
                    <p className="text-sm text-foreground/65">
                        {getHexagramBrief(hexagram.name)}
                    </p>
                    {changedLines.length > 0 && (
                        <p className="text-xs text-red-500 mt-2">
                            变爻：{changedLines.map(l => `第${l}爻`).join('、')}
                        </p>
                    )}
                </div>
            )}
        </div>
    );
}

// 小型卦象预览
export function HexagramPreview({ hexagram, yaos }: { hexagram: Hexagram; yaos: Yao[] }) {
    const displayYaos = [...yaos].reverse();

    return (
        <div className="flex items-center gap-3">
            <div className="flex flex-col gap-0.5">
                {displayYaos.map((yao) => (
                    <YaoLine key={yao.position} yao={yao} size="sm" />
                ))}
            </div>
            <span className="text-sm font-medium text-foreground">{hexagram.name}</span>
        </div>
    );
}
