
export interface TarotCanonicalJSON {
  问卜设定: {
    牌阵: string;
    问题?: string;
    出生日期?: string;
    随机种子?: string;
  };
  牌阵展开: TarotCardJSON[];
  求问者生命数字?: {
    人格牌: TarotNumerologyCardJSON;
    灵魂牌: TarotNumerologyCardJSON;
    年度牌: TarotNumerologyCardJSON;
  };
}

// ===== 塔罗 =====

export interface TarotCardJSON {
  位置: string;
  塔罗牌: string;
  状态: string;
  核心基调: string[];
  元素?: string;
  星象?: string;
}

export interface TarotNumerologyCardJSON {
  对应塔罗: string;
  背景基调: string[];
  元素?: string;
  星象?: string;
  年份?: number;
}
