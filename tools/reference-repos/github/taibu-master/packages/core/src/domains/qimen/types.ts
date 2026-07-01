
// ===== 奇门遁甲相关类型 =====

export interface QimenInput {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute?: number;
  timezone?: string;
  question?: string;
  panType?: 'zhuan';
  juMethod?: 'chaibu' | 'maoshan';
  zhiFuJiGong?: 'ji_liuyi' | 'ji_wugong';
}

export interface QimenPalaceInfo {
  palaceIndex: number;        // 宫位序号 1-9
  palaceName: string;         // 卦名（坎、坤、震...）
  direction: string;          // 方位
  element: string;            // 宫五行
  earthStem: string;          // 地盘天干
  heavenStem: string;         // 天盘天干
  star: string;               // 九星
  starElement: string;        // 星五行
  gate: string;               // 八门
  gateElement: string;        // 门五行
  deity: string;              // 八神
  formations: string[];       // 该宫格局列表
  stemWangShuai?: string;     // 天干旺衰状态
  elementState?: string;      // 宫五行旺衰
  earthStemElement?: string;  // 地盘干五行
  heavenStemElement?: string; // 天盘干五行
  isKongWang?: boolean;       // 是否空亡
  isYiMa?: boolean;           // 是否驿马
  isRuMu?: boolean;           // 是否入墓
}

export interface QimenOutput {
  dateInfo: {
    solarDate: string;
    lunarDate: string;
    solarTerm: string;
    solarTermRange?: string;
  };
  siZhu: {
    year: string;
    month: string;
    day: string;
    hour: string;
  };
  dunType: 'yang' | 'yin';
  juNumber: number;
  yuan: string;
  xunShou: string;
  zhiFu: { star: string; palace: number; };
  zhiShi: { gate: string; palace: number; };
  palaces: QimenPalaceInfo[];
  kongWang: {
    dayKong: { branches: string[]; palaces: number[]; };
    hourKong: { branches: string[]; palaces: number[]; };
  };
  yiMa: { branch: string; palace: number; };
  globalFormations: string[];
  panType: string;
  juMethod: string;
  question?: string;
  monthPhase?: Record<string, string>; // 十干月令旺衰：干 → 旺/相/休/囚/死
}
