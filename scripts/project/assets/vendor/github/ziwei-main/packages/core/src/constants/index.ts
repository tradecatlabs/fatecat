import { keys } from "remeda";

// ================== 阴阳 ==================
export const YIN_YANG = {
  Yin: 0,
  Yang: 1,
} as const;

export const YIN_YANG_HANS = {
  Yin: "阴",
  Yang: "阳",
} as const;

export const YIN_YANG_HANT = {
  Yin: "陰",
  Yang: "陽",
} as const;

export const YIN_YANG_KEYS = ["Yin", "Yang"] as const;

// ================== Gender ==================
export const GENDER = {
  Yin: "女",
  Yang: "男",
} as const;

export const GENDER_KEYS = YIN_YANG_KEYS;

// ================== Stem ==================
export const STEM = {
  Jia: "甲",
  Yi: "乙",
  Bing: "丙",
  Ding: "丁",
  Wu: "戊",
  Ji: "己",
  Geng: "庚",
  Xin: "辛",
  Ren: "壬",
  Gui: "癸",
} as const;

/** 十天干 Key 数组 */
export const STEM_KEYS = keys(STEM);

/** 十天干四化曜表 */
export const STEM_TRANSFORMATIONS: Record<(typeof STEM_KEYS)[number], (keyof typeof STAR_HANS)[]> =
  {
    Jia: ["LianZhen", "PoJun", "WuQu", "TaiYang"],
    Yi: ["TianJi", "TianLiang", "ZiWei", "TaiYin"],
    Bing: ["TianTong", "TianJi", "WenChang", "LianZhen"],
    Ding: ["TaiYin", "TianTong", "TianJi", "JuMen"],
    Wu: ["TanLang", "TaiYin", "YouBi", "TianJi"],
    Ji: ["WuQu", "TanLang", "TianLiang", "WenQu"],
    Geng: ["TaiYang", "WuQu", "TaiYin", "TianTong"],
    Xin: ["JuMen", "TaiYang", "WenQu", "WenChang"],
    Ren: ["TianLiang", "ZiWei", "ZuoFu", "WuQu"],
    Gui: ["PoJun", "JuMen", "TaiYin", "TanLang"],
  };

// ================== Branch ==================

/**
 * 十二地支对象（拼音 Key，首字母大写）。
 */
export const BRANCH = {
  Zi: "子",
  Chou: "丑",
  Yin: "寅",
  Mao: "卯",
  Chen: "辰",
  Si: "巳",
  Wu: "午",
  Wei: "未",
  Shen: "申",
  You: "酉",
  Xu: "戌",
  Hai: "亥",
} as const;

/** 十二地支 Key 数组 */
export const BRANCH_KEYS = keys(BRANCH);

export const ZODIAC_HANS = {
  Zi: "鼠",
  Chou: "牛",
  Yin: "虎",
  Mao: "兔",
  Chen: "龙",
  Si: "蛇",
  Wu: "马",
  Wei: "羊",
  Shen: "猴",
  You: "鸡",
  Xu: "狗",
  Hai: "猪",
} as const;

export const ZODIAC_HANT = {
  Zi: "鼠",
  Chou: "牛",
  Yin: "虎",
  Mao: "兔",
  Chen: "龍",
  Si: "蛇",
  Wu: "馬",
  Wei: "羊",
  Shen: "猴",
  You: "雞",
  Xu: "狗",
  Hai: "豬",
} as const;

// ================== Hour ==================

/** 时辰间隔文案数组 */
export const HOUR_RANGES = [
  "23:00~00:59",
  "01:00~02:59",
  "03:00~04:59",
  "05:00~06:59",
  "07:00~08:59",
  "09:00~10:59",
  "11:00~12:59",
  "13:00~14:59",
  "15:00~16:59",
  "17:00~18:59",
  "19:00~20:59",
  "21:00~22:59",
] as const;

// ================== Star ==================
export const STAR_HANS = {
  ZiWei: {
    name: "紫微",
    abbr: "紫",
  },
  TaiYang: {
    name: "太阳",
    abbr: "阳",
  },
  WuQu: {
    name: "武曲",
    abbr: "武",
  },
  TianTong: {
    name: "天同",
    abbr: "同",
  },
  LianZhen: {
    name: "廉贞",
    abbr: "廉",
  },
  TianJi: {
    name: "天机",
    abbr: "机",
  },
  TaiYin: {
    name: "太阴",
    abbr: "阴",
  },
  TanLang: {
    name: "贪狼",
    abbr: "贪",
  },
  JuMen: {
    name: "巨门",
    abbr: "巨",
  },
  TianLiang: {
    name: "天梁",
    abbr: "梁",
  },
  PoJun: {
    name: "破军",
    abbr: "破",
  },
  QiSha: {
    name: "七杀",
    abbr: "杀",
  },
  TianXiang: {
    name: "天相",
    abbr: "相",
  },
  TianFu: {
    name: "天府",
    abbr: "府",
  },
  ZuoFu: {
    name: "左辅",
    abbr: "左",
  },
  YouBi: {
    name: "右弼",
    abbr: "右",
  },
  WenChang: {
    name: "文昌",
    abbr: "昌",
  },
  WenQu: {
    name: "文曲",
    abbr: "曲",
  },
} as const;

export const STAR_HANT = {
  ZiWei: {
    name: "紫微",
    abbr: "紫",
  },
  TaiYang: {
    name: "太陽",
    abbr: "陽",
  },
  WuQu: {
    name: "武曲",
    abbr: "武",
  },
  TianTong: {
    name: "天同",
    abbr: "同",
  },
  LianZhen: {
    name: "廉貞",
    abbr: "廉",
  },
  TianJi: {
    name: "天機",
    abbr: "機",
  },
  TaiYin: {
    name: "太陰",
    abbr: "陰",
  },
  TanLang: {
    name: "貪狼",
    abbr: "貪",
  },
  JuMen: {
    name: "巨門",
    abbr: "巨",
  },
  TianLiang: {
    name: "天梁",
    abbr: "梁",
  },
  PoJun: {
    name: "破軍",
    abbr: "破",
  },
  QiSha: {
    name: "七殺",
    abbr: "殺",
  },
  TianXiang: {
    name: "天相",
    abbr: "相",
  },
  TianFu: {
    name: "天府",
    abbr: "府",
  },
  ZuoFu: {
    name: "左輔",
    abbr: "左",
  },
  YouBi: {
    name: "右弼",
    abbr: "右",
  },
  WenChang: {
    name: "文昌",
    abbr: "昌",
  },
  WenQu: {
    name: "文曲",
    abbr: "曲",
  },
} as const;

/** 星辰所属星系（南 | 北 | 中） */
export const STAR_GALAXY = {
  S: "南斗",
  N: "北斗",
  C: "中斗",
} as const;

export const STAR_TYPE = {
  major: "主星",
  minor: "辅星",
  auxiliary: "杂星",
} as const;

export const MINOR_STARS = ["ZuoFu", "YouBi", "WenChang", "WenQu"];

// ================== FiveElement ==================

export const FIVE_ELEMENT_ELEMENT = {
  Shui: "水",
  Huo: "火",
  Mu: "木",
  Tu: "土",
  Jin: "金",
} as const;

export const FIVE_ELEMENT_SCHEME = {
  Shui: "水二局",
  Huo: "火六局",
  Mu: "木三局",
  Tu: "土五局",
  Jin: "金四局",
} as const;

export const FIVE_ELEMENT_SCHEME_VALUE = {
  Shui: 2,
  Huo: 6,
  Mu: 3,
  Tu: 5,
  Jin: 4,
} as const;

/** 五行局数 Key 数组 */
export const FIVE_ELEMENT_KEYS = ["Shui", "Huo", "Mu", "Tu", "Jin"] as const;
/** 五行局数 */
export const FIVE_ELEMENT_SCHEME_VALUES = [2, 6, 3, 5, 4] as const;

export const FIVE_ELEMENT_TABLE = [
  // 甲己
  ["Shui", "Huo", "Mu", "Tu", "Jin", "Huo"],

  // 乙庚
  ["Huo", "Tu", "Jin", "Mu", "Shui", "Tu"],

  // 丙辛
  ["Tu", "Mu", "Shui", "Jin", "Huo", "Mu"],

  // 丁壬
  ["Mu", "Jin", "Huo", "Shui", "Tu", "Jin"],

  // 戊癸
  ["Jin", "Shui", "Tu", "Huo", "Mu", "Shui"],
] as const;

// ================== Palace ==================
export const PALACE_HANS = {
  Ming: { name: "命宫", decade: "大命" },
  XiongDi: { name: "兄弟", decade: "大兄" },
  FuQi: { name: "夫妻", decade: "大夫" },
  ZiNv: { name: "子女", decade: "大子" },
  CaiBo: { name: "财帛", decade: "大财" },
  JiE: { name: "疾厄", decade: "大疾" },
  QianYi: { name: "迁移", decade: "大迁" },
  JiaoYou: { name: "交友", decade: "大友" },
  GuanLu: { name: "官禄", decade: "大官" },
  TianZhai: { name: "田宅", decade: "大田" },
  FuDe: { name: "福德", decade: "大福" },
  FuMu: { name: "父母", decade: "大父" },
} as const;

export const PALACE_HANT = {
  Ming: { name: "命宮", decade: "大命" },
  XiongDi: { name: "兄弟", decade: "大兄" },
  FuQi: { name: "夫妻", decade: "大夫" },
  ZiNv: { name: "子女", decade: "大子" },
  CaiBo: { name: "財帛", decade: "大財" },
  JiE: { name: "疾厄", decade: "大疾" },
  QianYi: { name: "遷移", decade: "大遷" },
  JiaoYou: { name: "交友", decade: "大友" },
  GuanLu: { name: "官祿", decade: "大官" },
  TianZhai: { name: "田宅", decade: "大田" },
  FuDe: { name: "福德", decade: "大福" },
  FuMu: { name: "父母", decade: "大父" },
} as const;

/** 十二宫职 Key 数组 */
export const PALACE_KEYS = [
  "Ming",
  "XiongDi",
  "FuQi",
  "ZiNv",
  "CaiBo",
  "JiE",
  "QianYi",
  "JiaoYou",
  "GuanLu",
  "TianZhai",
  "FuDe",
  "FuMu",
] as const;

// ================== Transformation ==================
/** 四化 key 数组 */
export const TRANSFORMATION_HANS = {
  A: "禄",
  B: "权",
  C: "科",
  D: "忌",
} as const;

export const TRANSFORMATION_HANT = {
  A: "祿",
  B: "權",
  C: "科",
  D: "忌",
} as const;

export const TRANSFORMATION_KEYS = ["A", "B", "C", "D"] as const;
