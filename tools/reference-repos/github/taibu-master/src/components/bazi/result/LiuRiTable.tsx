import type { LiuRiInfo } from '@/lib/divination/bazi';
import { getBranchElement, getElementColor, getStemElement } from '@/lib/divination/display-helpers';

export function LiuRiTable({
    liuRi,
    selectedDate,
    onSelect,
}: {
    liuRi: LiuRiInfo[];
    selectedDate: string;
    onSelect: (date: string) => void;
}) {
    return (
        <div className="overflow-x-auto -mx-2 px-2 scrollbar-thin">
            <div className="flex gap-2 min-w-max">
                {liuRi.map((ri) => {
                    const isSelected = ri.date === selectedDate;
                    const ganElement = getStemElement(ri.gan);
                    const zhiElement = getBranchElement(ri.zhi);

                    return (
                        <button
                            key={ri.date}
                            type="button"
                            onClick={() => onSelect(ri.date)}
                            className={`
                                flex-shrink-0 w-12 text-center p-2 rounded-md border transition-colors
                                ${isSelected
                                    ? 'border-[#2eaadc] bg-blue-50/30'
                                    : 'border-border bg-background hover:bg-background-secondary'
                                }
                            `}
                        >
                            <div className="text-[10px] font-mono text-foreground/40 mb-1.5 leading-none">
                                {ri.date.split('-')[1]}/{ri.date.split('-')[2]}
                            </div>
                            <div className="flex flex-col items-center gap-0.5">
                                <span
                                    className="text-xs font-bold"
                                    style={{ color: ganElement ? getElementColor(ganElement) : undefined }}
                                >
                                    {ri.gan}
                                </span>
                                <span
                                    className="text-xs font-bold"
                                    style={{ color: zhiElement ? getElementColor(zhiElement) : undefined }}
                                >
                                    {ri.zhi}
                                </span>
                            </div>
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
