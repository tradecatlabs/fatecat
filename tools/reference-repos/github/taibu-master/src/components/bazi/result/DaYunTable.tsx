import type { DaYunInfo } from '@/lib/divination/bazi';
import { getBranchElement, getElementColor, getStemElement } from '@/lib/divination/display-helpers';

export function DaYunTable({
    daYun,
    selectedIndex,
    onSelect,
}: {
    daYun: DaYunInfo[];
    selectedIndex: number;
    onSelect: (index: number) => void;
}) {
    return (
        <div className="overflow-x-auto -mx-2 px-2 scrollbar-thin">
            <div className="flex gap-2 min-w-max">
                {daYun.map((dy, index) => {
                    const isSelected = selectedIndex === index;
                    const ganElement = getStemElement(dy.gan);
                    const zhiElement = getBranchElement(dy.zhi);

                    return (
                        <button
                            key={index}
                            onClick={() => onSelect(index)}
                            className={`
                                flex-shrink-0 w-16 text-center p-2.5 rounded-md border transition-colors
                                ${isSelected
                                    ? 'border-[#2eaadc] bg-blue-50/30'
                                    : 'border-border bg-background hover:bg-background-secondary'
                                }
                            `}
                        >
                            <div className="text-[10px] font-bold text-foreground/30 uppercase tracking-wider">{dy.startYear}</div>
                            <div className="text-[11px] font-semibold text-foreground/50 mb-1.5">{dy.startAge}岁</div>
                            <div className="flex flex-col items-center gap-0.5">
                                <span
                                    className="text-base font-bold"
                                    style={{ color: ganElement ? getElementColor(ganElement) : undefined }}
                                >
                                    {dy.gan}
                                </span>
                                <span
                                    className="text-base font-bold"
                                    style={{ color: zhiElement ? getElementColor(zhiElement) : undefined }}
                                >
                                    {dy.zhi}
                                </span>
                            </div>
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
