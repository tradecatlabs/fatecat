import type {
  DayunItemJSON,
  HiddenStemJSON,
  TrueSolarTimeJSON
} from '../shared/json-types.js';

export interface BaziCanonicalJSON {
  基本信息: {
    性别: string;
    日主: string;
    命主五行?: string;
    空亡?: string[];
    出生地?: string;
    真太阳时?: TrueSolarTimeJSON;
    胎元?: string;
    命宫?: string;
  };
  四柱: BaziPillarJSON[];
  干支关系: string[];
  大运?: {
    起运信息: string;
    大运列表: DayunItemJSON[];
  };
}

// ===== 八字 =====

export interface BaziPillarJSON {
  柱: string;
  干支: string;
  天干十神: string;
  藏干: HiddenStemJSON[];
  地势: string;
  纳音?: string;
  神煞?: string[];
  空亡?: '是';
}
