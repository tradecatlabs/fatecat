import type { LiuYueInfo } from '@/lib/divination/bazi';
import { getBranchElement, getElementColor, getStemElement } from '@/lib/divination/display-helpers';

export function LiuYueTable({
    liuYue,
    selectedMonth,
    onSelect,
}: {
    liuYue: LiuYueInfo[];
    selectedMonth: number;
    onSelect: (month: number) => void;
}) {
    return (
        <div className="overflow-x-auto -mx-2 px-2 scrollbar-thin">
            <div className="flex gap-2 min-w-max">
                {liuYue.map((ly, index) => {
                    const isSelected = ly.month === selectedMonth;
                    const gan = ly.gan;
                    const zhi = ly.zhi;
                    const ganElement = getStemElement(gan);
                    const zhiElement = getBranchElement(zhi);

                    return (
                        <button
                            key={index}
                            type="button"
                            onClick={() => onSelect(ly.month)}
                            className={`
                                flex-shrink-0 w-12 text-center p-2 rounded-md border transition-colors
                                ${isSelected
                                    ? 'border-[#2eaadc] bg-blue-50/30'
                                    : 'border-border bg-background hover:bg-background-secondary'
                                }
                            `}
                        >
                            <div className="text-[10px] font-bold text-foreground/30 uppercase truncate mb-0.5">{ly.jieQi}</div>
                            <div className="text-[10px] font-mono text-foreground/40 mb-1.5 leading-none">
                                {Number(ly.startDate.split('-')[1])}/{Number(ly.startDate.split('-')[2])}
                            </div>
                            <div className="flex flex-col items-center gap-0.5">
                                <span
                                    className="text-sm font-bold"
                                    style={{ color: ganElement ? getElementColor(ganElement) : undefined }}
                                >
                                    {gan}
                                </span>
                                <span
                                    className="text-sm font-bold"
                                    style={{ color: zhiElement ? getElementColor(zhiElement) : undefined }}
                                >
                                    {zhi}
                                </span>
                            </div>
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
