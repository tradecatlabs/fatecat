
// ===== 四柱反推 =====

export interface BaziPillarsResolveCanonicalJSON {
  原始四柱: {
    年柱: string;
    月柱: string;
    日柱: string;
    时柱: string;
  };
  候选数量: number;
  候选列表: Array<{
    候选序号: number;
    农历: string;
    公历: string;
    出生时间: string;
    是否闰月: '是' | '否';
    下一步排盘建议: {
      工具: 'bazi';
      参数: {
        出生年: number;
        出生月: number;
        出生日: number;
        出生时: number;
        出生分: number;
        历法: 'lunar';
        是否闰月: '是' | '否';
      };
      缺少信息: string[];
    };
  }>;
}
