/**
 * 变爻选择器
 *
 * 选择哪些爻位是变爻
 */
'use client';

interface ChangingLinesSelectorProps {
    hexagramCode: string;
    value: number[];
    onChange: (positions: number[]) => void;
}

const YAO_LABELS = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻'];

export function ChangingLinesSelector({ hexagramCode, value, onChange }: ChangingLinesSelectorProps) {
    if (!hexagramCode || hexagramCode.length !== 6) {
        return (
            <p className="text-sm text-foreground-secondary text-center py-4">
                请先选择本卦
            </p>
        );
    }

    const toggle = (pos: number) => {
        if (value.includes(pos)) {
            onChange(value.filter(p => p !== pos));
        } else {
            onChange([...value, pos].sort((a, b) => a - b));
        }
    };

    // 从上爻到初爻显示（视觉上从上到下）
    const yaosReversed = hexagramCode.split('').map((char, i) => ({
        position: i + 1,
        isYang: char === '1',
    })).reverse();

    return (
        <div className="space-y-2">
            <div className="flex items-center justify-between">
                <h4 className="text-sm font-medium text-foreground">选择变爻</h4>
                <span className="text-xs text-foreground-secondary">
                    {value.length > 0 ? `已选 ${value.length} 个变爻` : '可选 0-6 个'}
                </span>
            </div>
            <div className="flex flex-col gap-1 bg-background/[0.02] border border-white/10 rounded-lg p-3">
                {yaosReversed.map(({ position, isYang }) => {
                    const isChanging = value.includes(position);
                    return (
                        <button
                            key={position}
                            onClick={() => toggle(position)}
                            className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-all
                                ${isChanging
                                    ? 'bg-red-500/10 border border-red-500/30'
                                    : 'hover:bg-background/5'
                                }`}
                        >
                            {/* 勾选框 */}
                            <div className={`w-4 h-4 rounded border-2 flex items-center justify-center transition-all
                                ${isChanging
                                    ? 'bg-red-500 border-red-500'
                                    : 'border-foreground-secondary'
                                }`}
                            >
                                {isChanging && (
                                    <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                                    </svg>
                                )}
                            </div>

                            {/* 爻位名称 */}
                            <span className={`text-xs w-10 ${isChanging ? 'text-red-500 font-medium' : 'text-foreground-secondary'}`}>
                                {YAO_LABELS[position - 1]}
                            </span>

                            {/* 爻线 */}
                            <div className="flex items-center flex-1">
                                {isYang ? (
                                    <div className={`w-[62px] h-2 rounded-sm ${isChanging ? 'bg-red-500' : 'bg-foreground'}`} />
                                ) : (
                                    <>
                                        <div className={`w-[27px] h-2 rounded-sm ${isChanging ? 'bg-red-500' : 'bg-foreground'}`} />
                                        <div className="w-2" />
                                        <div className={`w-[27px] h-2 rounded-sm ${isChanging ? 'bg-red-500' : 'bg-foreground'}`} />
                                    </>
                                )}
                            </div>

                            {/* 变爻标记 */}
                            {isChanging && (
                                <span className="text-xs text-red-500 font-medium">变</span>
                            )}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
