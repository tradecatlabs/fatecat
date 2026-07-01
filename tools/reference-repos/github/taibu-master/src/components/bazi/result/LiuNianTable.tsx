import type { LiuNianInfo } from '@/lib/divination/bazi';
import { getBranchElement, getElementColor, getStemElement } from '@/lib/divination/display-helpers';

export function LiuNianTable({
    liuNian,
    selectedYear,
    onSelect,
}: {
    liuNian: LiuNianInfo[];
    selectedYear: number;
    onSelect: (year: number) => void;
}) {
    return (
        <div className="overflow-x-auto -mx-2 px-2 scrollbar-thin">
            <div className="flex gap-2 min-w-max">
                {liuNian.map((ln, index) => {
                    const isSelected = selectedYear === ln.year;
                    const ganElement = getStemElement(ln.gan);
                    const zhiElement = getBranchElement(ln.zhi);

                    return (
                        <button
                            key={index}
                            onClick={() => onSelect(ln.year)}
                            className={`
                                flex-shrink-0 w-14 text-center p-2.5 rounded-md border transition-colors
                                ${isSelected
                                    ? 'border-[#2eaadc] bg-blue-50/30'
                                    : 'border-border bg-background hover:bg-background-secondary'
                                }
                            `}
                        >
                            <div className="text-[10px] font-bold text-foreground/30 uppercase tracking-wider">{ln.year}</div>
                            <div className="flex flex-col items-center gap-0.5 my-1.5">
                                <span
                                    className="text-sm font-bold"
                                    style={{ color: ganElement ? getElementColor(ganElement) : undefined }}
                                >
                                    {ln.gan}
                                </span>
                                <span
                                    className="text-sm font-bold"
                                    style={{ color: zhiElement ? getElementColor(zhiElement) : undefined }}
                                >
                                    {ln.zhi}
                                </span>
                            </div>
                            <div className="text-[10px] font-bold text-foreground/40">{ln.age}岁</div>
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
