import type {
  ZiweiBirthYearMutagenJSON,
  ZiweiStarJSON
} from '../shared/json-types.js';

export interface ZiweiCanonicalJSON {
  基本信息: {
    性别?: string;
    阳历: string;
    农历: string;
    四柱: string;
    命主: string;
    身主: string;
    五行局: string;
    生年四化?: {
      天干: string;
      四化星曜: ZiweiBirthYearMutagenJSON[];
    };
    时辰?: string;
    斗君?: string;
    命主星?: string;
    身主星?: string;
    真太阳时?: {
      钟表时间: string;
      真太阳时: string;
      经度: number;
      校正分钟: number;
      真太阳时索引: number;
      跨日偏移: string;
    };
  };
  十二宫位: ZiweiPalaceJSON[];
  小限?: Array<{
    宫位: string;
    虚岁: number[];
  }>;
}

export interface ZiweiPalaceJSON {
  宫位: string;
  宫位索引?: number;
  干支: string;
  是否身宫: '是' | '否';
  是否来因宫: '是' | '否';
  大限?: string;
  主星及四化: ZiweiStarJSON[];
  辅星: ZiweiStarJSON[];
  杂曜?: ZiweiStarJSON[];
  神煞?: string[];
  流年虚岁?: number[];
  小限虚岁?: number[];
}
