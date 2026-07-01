
export interface QimenCanonicalJSON {
  基本信息: {
    占问?: string;
    四柱: string;
    节气: string;
    局式: string;
    三元: string;
    旬首: string;
    值符: string;
    值使: string;
    公历?: string;
    农历?: string;
    节气范围?: string;
    盘式?: string;
    定局法?: string;
  };
  九宫盘: QimenPalaceJSON[];
  空亡信息?: {
    日空: {
      地支: string[];
      宫位: string[];
    };
    时空: {
      地支: string[];
      宫位: string[];
    };
  };
  驿马?: {
    地支: string;
    宫位: string;
  };
  十干月令旺衰?: Record<string, string>;
  全局格局?: string[];
}

// ===== 奇门遁甲 =====

export interface QimenPalaceJSON {
  宫名: string;
  宫位序号: number;
  宫位: string;
  宫位五行: string;
  八神: string;
  九星: string;
  九星五行?: string;
  八门: string;
  八门五行?: string;
  天盘天干: string;
  地盘天干: string;
  宫位状态: string[];
  方位?: string;
  格局?: string[];
  宫旺衰?: string;
  天盘天干五行?: string;
  地盘天干五行?: string;
}
