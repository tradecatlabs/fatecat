import type {
  BirthTimeInput,
  DecadalInfo,
  GanZhiPair,
  Gender,
  PalaceInfo,
  ScholarStarEntry,
  SmallLimitEntry,
  TrueSolarTimeInfo
} from '../shared/types.js';

// ===== 紫微相关类型 =====

export interface ZiweiInput extends BirthTimeInput {
  gender: Gender;
  longitude?: number;
}

export interface ZiweiOutput {
  solarDate: string;
  lunarDate: string;
  fourPillars: {
    year: GanZhiPair;
    month: GanZhiPair;
    day: GanZhiPair;
    hour: GanZhiPair;
  };
  soul: string;
  body: string;
  fiveElement: string;
  zodiac: string;
  sign: string;
  palaces: PalaceInfo[];
  decadalList: DecadalInfo[];
  earthlyBranchOfSoulPalace?: string;
  earthlyBranchOfBodyPalace?: string;
  time?: string;
  timeRange?: string;
  mutagenSummary?: MutagenSummaryItem[];
  gender?: string;    // 回显性别
  douJun?: string;    // 子年斗君地支
  trueSolarTimeInfo?: TrueSolarTimeInfo;
  lifeMasterStar?: string;   // 命主星
  bodyMasterStar?: string;   // 身主星
  smallLimit?: SmallLimitEntry[];    // 小限
  scholarStars?: ScholarStarEntry[]; // 博士十二星
}

export interface MutagenSummaryItem {
  mutagen: '禄' | '权' | '科' | '忌';
  starName: string;
  palaceName: string;
}
