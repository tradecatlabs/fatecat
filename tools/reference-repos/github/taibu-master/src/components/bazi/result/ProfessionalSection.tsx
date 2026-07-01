import { Calendar, TrendingUp } from 'lucide-react';
import type { BaziCanonicalJSON } from 'taibu-core/bazi';
import { calculateProfessionalData, type DaYunInfo, type LiuNianInfo, type LiuYueInfo, type LiuRiInfo } from '@/lib/divination/bazi';
import { DaYunTable } from '@/components/bazi/result/DaYunTable';
import { LiuNianTable } from '@/components/bazi/result/LiuNianTable';
import { LiuYueTable } from '@/components/bazi/result/LiuYueTable';
import { LiuRiTable } from '@/components/bazi/result/LiuRiTable';
import { ProfessionalTable } from '@/components/bazi/result/ProfessionalTable';

export function ProfessionalSection({
    canonicalChart,
    proData,
    isUnknownTime = false,
    selectedDaYunIndex,
    onSelectDaYun,
    currentLiuNian,
    selectedLiuNianYear,
    onSelectLiuNian,
    liuYue,
    selectedLiuYueMonth,
    onSelectLiuYue,
    liuRi,
    selectedLiuRiDate,
    onSelectLiuRi,
    activeLiuYue,
}: {
    canonicalChart: BaziCanonicalJSON;
    proData: ReturnType<typeof calculateProfessionalData>;
    isUnknownTime?: boolean;
    selectedDaYunIndex: number;
    onSelectDaYun: (index: number) => void;
    currentLiuNian: LiuNianInfo[];
    selectedLiuNianYear: number;
    onSelectLiuNian: (year: number) => void;
    liuYue: LiuYueInfo[];
    selectedLiuYueMonth: number;
    onSelectLiuYue: (month: number) => void;
    liuRi: LiuRiInfo[];
    selectedLiuRiDate: string;
    onSelectLiuRi: (date: string) => void;
    activeLiuYue: LiuYueInfo | null;
}) {
    // 获取当前选中的运势信息
    const activeDaYun: DaYunInfo | undefined = proData.daYun[selectedDaYunIndex];
    const activeLiuNian: LiuNianInfo | undefined = currentLiuNian.find(ln => ln.year === selectedLiuNianYear);
    const activeLiuRi: LiuRiInfo | undefined = liuRi.find(lr => lr.date === selectedLiuRiDate);
    const relationHighlights = isUnknownTime ? [] : canonicalChart.干支关系;
    const hasGanZhiHighlights = relationHighlights.length > 0;

    return (
        <div className="space-y-8">
            <section className="bg-background border border-border rounded-md px-1 pb-4 pt-2">
                {/* <h2 className="text-sm font-semibold mb-6 flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-[#2eaadc]" />
                    命盘详情
                </h2> */}
                <ProfessionalTable
                    canonicalChart={canonicalChart}
                    isUnknownTime={isUnknownTime}
                    // 运势信息
                    activeDaYun={activeDaYun}
                    activeLiuNian={activeLiuNian}
                    activeLiuYue={activeLiuYue ?? undefined}
                    activeLiuRi={activeLiuRi}
                />
                <div className="px-4 mt-4 border-t border-border/60 space-y-2 text-xs text-foreground/45 font-medium">
                        <div>
                            起运：{proData.startAgeDetail}
                        {canonicalChart.基本信息.胎元 ? `　胎元：${canonicalChart.基本信息.胎元}` : ''}
                        {canonicalChart.基本信息.命宫 ? `　命宫：${canonicalChart.基本信息.命宫}` : ''}
                    </div>
                    {hasGanZhiHighlights ? (
                        <div>
                            干支关系：{relationHighlights.join('、')}
                        </div>
                    ) : null}
                    {canonicalChart.基本信息.真太阳时 ? (
                        <div>
                            真太阳时：{canonicalChart.基本信息.真太阳时.真太阳时}（钟表 {canonicalChart.基本信息.真太阳时.钟表时间}）
                        </div>
                    ) : null}
                </div>
            </section>

            <section className="bg-background border border-border rounded-md p-6 py-4">
                <h2 className="text-sm font-semibold mb-6 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-[#2eaadc]" />
                    大运排布
                </h2>
                <DaYunTable
                    daYun={proData.daYun}
                    selectedIndex={selectedDaYunIndex}
                    onSelect={onSelectDaYun}
                />
            </section>

            {currentLiuNian.length > 0 && (
                <section className="bg-background border border-border rounded-md p-6 py-4">
                    <h2 className="text-sm font-semibold mb-6 flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-[#2eaadc]" />
                        流年运势
                    </h2>
                    <LiuNianTable
                        liuNian={currentLiuNian}
                        selectedYear={selectedLiuNianYear}
                        onSelect={onSelectLiuNian}
                    />
                </section>
            )}

            {liuYue.length > 0 && (
                <section className="bg-background border border-border rounded-md p-6 py-4">
                    <h2 className="text-sm font-semibold mb-6 flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-[#2eaadc]" />
                        {selectedLiuNianYear}年 流月
                    </h2>
                    <LiuYueTable
                        liuYue={liuYue}
                        selectedMonth={selectedLiuYueMonth}
                        onSelect={onSelectLiuYue}
                    />
                    <p className="mt-4 text-[11px] text-foreground/30 font-medium italic">
                        * 点击特定流月以展开流日详情
                    </p>
                </section>
            )}

            {liuRi.length > 0 && activeLiuYue && (
                <section className="bg-background border border-border rounded-md p-6 py-4">
                    <h2 className="text-sm font-semibold mb-6 flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-[#2eaadc]" />
                        流日记录（{activeLiuYue.startDate} — {activeLiuYue.endDate}）
                    </h2>
                    <LiuRiTable
                        liuRi={liuRi}
                        selectedDate={selectedLiuRiDate}
                        onSelect={onSelectLiuRi}
                    />
                </section>
            )}
        </div>
    );
}
