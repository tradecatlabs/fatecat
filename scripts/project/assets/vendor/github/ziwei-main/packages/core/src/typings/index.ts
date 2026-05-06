import type {
  BRANCH,
  FIVE_ELEMENT_KEYS,
  FIVE_ELEMENT_SCHEME,
  FIVE_ELEMENT_SCHEME_VALUES,
  GENDER,
  HOUR_RANGES,
  PALACE_HANS,
  PALACE_HANT,
  PALACE_KEYS,
  STAR_GALAXY,
  STAR_HANS,
  STAR_HANT,
  STAR_TYPE,
  STEM,
  TRANSFORMATION_HANS,
  TRANSFORMATION_HANT,
  TRANSFORMATION_KEYS,
  YIN_YANG_HANS,
  YIN_YANG_HANT,
  YIN_YANG_KEYS,
  ZODIAC_HANS,
  ZODIAC_HANT,
} from "../constants";

// ================== Basic ==================

export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type Locale = "zh-Hans" | "zh-Hant";

// ================== Values Object ==================
export interface GenderVO {
  /** 业务唯一标识 */
  key: GenderKey;
  /** 名称 */
  name: GenderName;
}

export interface StemVO {
  /** 业务唯一标识 */
  key: StemKey; // e.g. "jia" | "yi" | "bing" ...
  /** 名称 */
  name: StemName;
}

export interface BranchVO {
  key: BranchKey;
  /** 名称 */
  name: BranchName;
}

export interface StarMetaVO {
  /** 星辰唯一标识符 */
  key?: StarKey;
  /** 星辰起始索引 */
  startIndex: number;
  /** 星辰坐落的顺逆 */
  direction: 1 | -1;
  /** 星辰的星系 */
  galaxy?: StarGalaxy;
}

export interface TransformationVO {
  key: TransformationKey;
  /** 名称 */
  name: TransformationName;
}

export interface SelfTransformationVO {
  /** 向心自化 */
  entry?: Readonly<TransformationVO>;
  /** 向心自化 */
  exit?: Readonly<TransformationVO>;
}

export interface DecadeVO {
  /** 大限 Key */
  key: DecadeKey;
  /** 名称 */
  name: DecadeName;
  /** 流年 */
  yearly: YearlyVO;
}

export interface YearlyVO {
  /** 流年 */
  name: number;
  /** 命主在此流年时的年龄 */
  age: number;
}

// ================== Enums ==================
export type OneKey = (typeof YIN_YANG_KEYS)[number];
export type OneNameHans = (typeof YIN_YANG_HANS)[OneKey];
export type OneNameHant = (typeof YIN_YANG_HANT)[OneKey];
export type OneName = OneNameHans | OneNameHant;

export type GenderKey = OneKey;
export type GenderName = (typeof GENDER)[OneKey];

export type StemKey = keyof typeof STEM;
export type StemName = (typeof STEM)[StemKey];

export type BranchKey = keyof typeof BRANCH;
export type BranchName = (typeof BRANCH)[BranchKey];

export type ZodiacKey = BranchKey;
export type ZodiacNameHans = (typeof ZODIAC_HANS)[ZodiacKey];
export type ZodiacNameHant = (typeof ZODIAC_HANT)[ZodiacKey];
export type ZodiacName = ZodiacNameHans | ZodiacNameHant;

export type HourRange = (typeof HOUR_RANGES)[number];

export type StarKey = keyof typeof STAR_HANS;
export type StarNameHans = (typeof STAR_HANS)[StarKey]["name"];
export type StarNameHant = (typeof STAR_HANT)[StarKey]["name"];
export type StarName = StarNameHans | StarNameHant;

export type StarAbbrKey = StarKey;
export type StarAbbrNameHans = (typeof STAR_HANS)[StarKey]["abbr"];
export type StarAbbrNameHant = (typeof STAR_HANT)[StarKey]["abbr"];
export type StarAbbrName = StarAbbrNameHans | StarAbbrNameHant;

export type MinorStarKey = Extract<StarKey, "ZuoFu" | "YouBi" | "WenChang" | "WenQu">;

/** 星辰所属星系（南 | 北 | 中） */
export type StarGalaxy = keyof typeof STAR_GALAXY;
export type StarGalaxyName = (typeof STAR_GALAXY)[StarGalaxy];
/** 星辰类型（主星 | 辅星 | 杂星） */
export type StarType = keyof typeof STAR_TYPE;

export type FiveElementSchemeKey = (typeof FIVE_ELEMENT_KEYS)[number];
export type FiveElementSchemeName = (typeof FIVE_ELEMENT_SCHEME)[FiveElementSchemeKey];
export type FiveElementSchemeValue = (typeof FIVE_ELEMENT_SCHEME_VALUES)[number];

export type PalaceKey = (typeof PALACE_KEYS)[number];
export type PalaceNameHans = (typeof PALACE_HANS)[PalaceKey]["name"];
export type PalaceNameHant = (typeof PALACE_HANT)[PalaceKey]["name"];
export type PalaceName = PalaceNameHans | PalaceNameHant;

export type DecadeKey = PalaceKey;
export type DecadeNameHans = (typeof PALACE_HANS)[PalaceKey]["decade"];
export type DecadeNameHant = (typeof PALACE_HANT)[PalaceKey]["decade"];
export type DecadeName = DecadeNameHans | DecadeNameHant;

export type TransformationKey = (typeof TRANSFORMATION_KEYS)[number];
export type TransformationNameHans = (typeof TRANSFORMATION_HANS)[TransformationKey];
export type TransformationNameHant = (typeof TRANSFORMATION_HANT)[TransformationKey];
export type TransformationName = TransformationNameHans | TransformationNameHant;
/** 向心自化 | 离心自化 */
export type SelfTransformationKey = "entry" | "exit";

// ================== Model ==================

export interface NatalProps {
  /** 姓名 */
  name: string;
  /** 性别 */
  gender: string;
  /** 出生年份天干 */
  birthYearStem: StemName;
  /** 出生年份天干 Key */
  birthYearStemKey: StemKey;
  /** 出生年份地支 */
  birthYearBranch: BranchName;
  /** 出生年份地支 Key */
  birthYearBranchKey: BranchKey;
  /** 阳历日期 */
  solarDate: string;
  /** 阳历日期之真太阳时 */
  solarDateByTrue?: string;
  /** 阴历年份 */
  lunisolarYear: number;
  /** 阴阳合历日期 */
  lunisolarDate: string;
  /** 干支日期 */
  sexagenaryCycleDate: string;
  /** 时辰 */
  hour: string;
  /** 时辰 Key */
  hourKey: BranchKey;
  /** 时辰对应的时间段 */
  hourRange: HourRange;
  /** 生肖 */
  zodiac: ZodiacName;
  /** 五行局 */
  fiveElementSchemeName: FiveElementSchemeName;
  /** 五行局数 */
  fiveElementSchemeValue: FiveElementSchemeValue;
  /** 紫微星所在地支 */
  ziweiBranch: BranchName;
  /** 紫微星所在地支Key */
  ziweiBranchKey: BranchKey;
  /** 命宫之地支 */
  mainPalaceBranch: BranchName;
  /** 命宫之地支 Key */
  mainPalaceBranchKey: BranchKey;
  /** 十二宫数据 */
  palaces: Palace[];
  /** 运限数据 */
  decade: DecadeVO[][];
  /** 当前运限索引 */
  decadeIndex: number;
  /** 大限流向，1为顺行，-1为逆行 */
  decadeDirection: 1 | -1;
}

export interface Natal extends NatalProps {
  /**
   * 获取运限数据
   *
   * @param index 以地支寅为起始的宫位索引（0-11）
   * @returns 运限数据
   */
  getDecade(index: number): DecadeVO[];

  getDecadeIndex(decade?: DecadeVO[]): number;
}

export interface PalaceProps {
  /** 宫位索引，从0到11的数字 */
  index: number;
  /** 宫位名称 */
  name: PalaceName;
  /** 宫位Key，用于唯一标识宫位 */
  key: PalaceKey;
  /** 是否来因宫，标识此宫是否为来因宫 */
  isLaiYin: boolean;
  /** 宫干 */
  stem: StemVO;
  /** 宫支 */
  branch: BranchVO;
  /** 主星，宫位中的主要星耀数组 */
  stars: Star[];
  /** 大限间隔，表示大限的起止年龄范围 */
  decadeRanges: number[];
}

export interface Palace extends PalaceProps {
  /**
   * 获取当前宫位飞宫四化的四个星辰Key数组
   * @param stemKey 天干 Key
   * @returns {StarKey[]} 返回一个四个星辰Key数组，下标分别对 [禄，权，科，忌]
   */
  flying(): StarKey[];
}

/**
 * 星辰
 * @property
 * - key 星辰唯一标识
 * - name 星辰名字
 * - abbrName 星辰缩写名
 * - type 星辰类型
 * - galaxy 星辰所属星系
 * - YT 生年四化
 * - ST 自化
 */
export interface StarProps {
  /** 星辰唯一标识符 */
  key: StarKey;
  /** 星辰名称 */
  name: StarName;
  /** 星辰简称 */
  abbr: StarAbbrName;
  /** 星辰类型（主星 | 辅星 | 杂星） */
  type: StarType;
  /** 星辰所属星系Key，可选属性 */
  galaxy?: StarGalaxy;
  /** 生年四化，若未产生生年四化则此字段为 `undefined` */
  YT?: TransformationVO;
  /** 自化，若未产生自化则此字段为 `undefined`，记录不同自化类型对应的变化 */
  ST?: SelfTransformationVO;
}

export interface Star extends StarProps {
  //
}

// ================== SDK ==================
export interface CreateZiWeiSolarParams {
  /** 姓名 */
  name: string;
  /** 性别 Key */
  gender: GenderKey;
  /** 出生日期 */
  date: Date;
  /** 语言 */
  language?: Locale;
  /** 出生地经度 默认为116.38333 北京天安门 */
  longitude?: number;
  /** 出生时区 默认为 8，北京时区 */
  timezone?: number;
  /** 是否采用真太阳时计算 默认为 true */
  useTrueSolarTime?: boolean;
  /** 覆盖用于推断大限等的参考时间；默认取 runtime.now() */
  referenceDate?: Date;
}

export interface CreateZiWeiLunisolarParams {
  /** 姓名 */
  name: string;
  /** 性别 Key */
  gender: GenderKey;
  /** 出生日期 YYYY-m-d-hourIndex  */
  date: string;
  /** 语言 */
  language?: Locale;
  /** 覆盖用于推断大限等的参考时间；默认取 runtime.now() */
  referenceDate?: Date;
}

export interface NatalCalculateParams {
  name: string;
  gender: GenderKey;
  monthIndex: number;
  day: number;
  hourIndex: number;
  birthYear: number;
  birthYearStemKey: StemKey;
  birthYearBranchKey: BranchKey;
  solarDate: string;
  solarDateByTrue?: string;
  lunisolarDate: string;
  sexagenaryCycleDate: string;
}

export interface NatalByStemBranchCalculateParams {
  /** 出生年干 Key */
  birthYearStemKey: StemKey;
  /** 命宫所在的地支 */
  mainPalaceBranchKey: BranchKey;
  /** 紫微星所在的地支 */
  branchKey: BranchKey;

  language?: Locale;
}

export interface CreateZiWeiByStemBranchParams extends NatalByStemBranchCalculateParams {
  //
}
