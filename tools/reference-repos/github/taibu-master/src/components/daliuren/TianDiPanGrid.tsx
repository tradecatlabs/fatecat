/**
 * 大六壬天地盘宫格组件
 * 4x4 布局，中心显示课名
 */
import type { DaliurenCanonicalJSON } from 'taibu-core/daliuren';

const WANGSUAI_COLORS: Record<string, string> = {
    旺: 'text-red-500 font-bold',
    相: 'text-orange-400 font-semibold',
    休: 'text-blue-400',
    囚: 'text-gray-400',
    死: 'text-gray-500',
};

const TIANJIANG_COLORS: Record<string, string> = {
    贵人: 'text-yellow-500', 腾蛇: 'text-red-400', 朱雀: 'text-red-500',
    六合: 'text-green-500', 勾陈: 'text-amber-500', 青龙: 'text-blue-500',
    天空: 'text-gray-400', 白虎: 'text-white', 太常: 'text-yellow-400',
    玄武: 'text-black dark:text-foreground/20', 太阴: 'text-purple-400', 天后: 'text-pink-400',
};

// 天地盘 12 宫的布局位置（4x4，中心2x2为课名区域）
// 顺序：从子位开始逆时针（传统六壬布局，外圈从右到左，上下）
// 位置索引对应 DI_ZHI 的 0-11（子丑寅卯辰巳午未申酉戌亥）
const GRID_POSITIONS: Record<number, { row: number; col: number }> = {
    // 下方（子丑寅）：row=3, col=1,2,3（从左到右：寅丑子）
    2: { row: 3, col: 0 }, // 寅
    1: { row: 3, col: 1 }, // 丑
    0: { row: 3, col: 2 }, // 子
    11: { row: 3, col: 3 }, // 亥
    // 右侧（亥戌酉）：col=3, row=2,1（从下到上：戌酉）
    10: { row: 2, col: 3 }, // 戌
    9: { row: 1, col: 3 }, // 酉
    // 上方（酉申未午巳）：row=0, col=3,2,1,0（从右到左：申未午巳）
    8: { row: 0, col: 3 }, // 申
    7: { row: 0, col: 2 }, // 未
    6: { row: 0, col: 1 }, // 午
    5: { row: 0, col: 0 }, // 巳
    // 左侧（辰卯寅）：col=0, row=1,2（从上到下：辰卯）
    4: { row: 1, col: 0 }, // 辰
    3: { row: 2, col: 0 }, // 卯
};

interface PalaceCellProps {
    gong: DaliurenCanonicalJSON['天地盘'][number];
    isKong: boolean;
    isSanChuan?: 'chu' | 'zhong' | 'mo';
}

function PalaceCell({ gong, isKong, isSanChuan }: PalaceCellProps) {
    const wangColor = gong.旺衰 ? WANGSUAI_COLORS[gong.旺衰] || 'text-foreground' : 'text-foreground';
    const jiangColor = gong.天将 ? TIANJIANG_COLORS[gong.天将] || 'text-foreground' : 'text-foreground';
    const kongStyle = isKong ? 'opacity-50' : '';

    const sanChuanBorder = isSanChuan
        ? isSanChuan === 'chu' ? 'ring-1 ring-red-400' :
          isSanChuan === 'zhong' ? 'ring-1 ring-orange-400' :
          'ring-1 ring-yellow-400'
        : '';

    return (
        <div className={`flex flex-col items-center justify-center p-1 min-h-[64px] bg-background-secondary/50 rounded-lg border border-border/30 ${sanChuanBorder} ${kongStyle}`}>
            {/* 天将 */}
            <span className={`text-xs leading-tight ${jiangColor}`}>{gong.天将}</span>
            {/* 天盘地支 */}
            <span className={`text-sm font-bold leading-tight ${wangColor}`}>
                {gong.天盘}{isKong ? '⊙' : ''}
            </span>
            {/* 地盘地支 */}
            <span className="text-xs text-foreground-secondary leading-tight">{gong.地盘}</span>
            {/* 十二长生 */}
            <span className="text-[10px] text-foreground-tertiary leading-tight">{gong.长生十二神}</span>
        </div>
    );
}

interface TianDiPanGridProps {
    result: DaliurenCanonicalJSON;
}

export function TianDiPanGrid({ result }: TianDiPanGridProps) {
    const kongSet = new Set(result.基本信息.关键状态.空亡);
    const chuZhi = result.三传[0]?.地支;
    const zhongZhi = result.三传[1]?.地支;
    const moZhi = result.三传[2]?.地支;
    const [centerTitle, centerSubtitle] = result.基本信息.课式.split(' / ');

    // 确定三传所在宫位（天盘地支匹配）
    const getSanChuanMark = (gong: DaliurenCanonicalJSON['天地盘'][number]): 'chu' | 'zhong' | 'mo' | undefined => {
        if (gong.天盘 === chuZhi) return 'chu';
        if (gong.天盘 === zhongZhi) return 'zhong';
        if (gong.天盘 === moZhi) return 'mo';
        return undefined;
    };

    return (
        <div className="w-full max-w-xs mx-auto">
            <div className="grid grid-cols-4 grid-rows-4 gap-1">
                {Array.from({ length: 16 }, (_, idx) => {
                    const row = Math.floor(idx / 4);
                    const col = idx % 4;

                    // 中心 2x2
                    if (row >= 1 && row <= 2 && col >= 1 && col <= 2) {
                        if (row === 1 && col === 1) {
                            // 中心格：课名
                            return (
                                <div key={idx} className="col-span-2 row-span-2 flex flex-col items-center justify-center bg-gradient-to-br from-cyan-500/10 to-teal-500/10 border border-cyan-500/30 rounded-lg p-2">
                                    <div className="text-xs text-foreground-secondary mb-1">课式</div>
                                    <div className="text-sm font-bold text-foreground text-center leading-tight">
                                        {centerTitle}
                                    </div>
                                    {centerSubtitle && (
                                        <div className="text-xs text-teal-500 text-center">
                                            {centerSubtitle}
                                        </div>
                                    )}
                                </div>
                            );
                        }
                        return null; // 中心其他格被 span 占用
                    }

                    // 找到对应的地支序号
                    const zhiIdx = Object.entries(GRID_POSITIONS).find(
                        ([, pos]) => pos.row === row && pos.col === col
                    )?.[0];

                    if (zhiIdx === undefined) return <div key={idx} />;

                    const gong = result.天地盘[parseInt(zhiIdx)];
                    if (!gong) return <div key={idx} />;

                    return (
                        <PalaceCell
                            key={idx}
                            gong={gong}
                            isKong={kongSet.has(gong.天盘)}
                            isSanChuan={getSanChuanMark(gong)}
                        />
                    );
                })}
            </div>
            {/* 图例 */}
            <div className="flex items-center justify-center gap-3 mt-2 text-xs text-foreground-tertiary">
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-red-400"></span>初传</span>
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-orange-400"></span>中传</span>
                <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-yellow-400"></span>末传</span>
                <span>⊙空亡</span>
            </div>
        </div>
    );
}
