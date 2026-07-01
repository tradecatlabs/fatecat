import type {
  ChongHeTransition,
  DerivedHexagramInfo,
  DetailLevel,
  FullYaoInfo,
  FuShenInfo,
  GanZhiTime,
  GuaFanFuYinInfo,
  GuaShenInfo,
  KongWangByPillarInfo,
  KongWangInfo,
  LiuChongGuaInfo,
  LiuHeGuaInfo,
  LiuQinType,
  SanHeAnalysisInfo,
  ShenSystemByYongShenInfo,
  TimeRecommendation,
  YongShenGroupInfo
} from '../shared/types.js';

// ===== 六爻相关类型 =====

export interface LiuyaoInput {
  question: string;
  yongShenTargets: LiuQinType[];
  method?: 'auto' | 'select' | 'time' | 'number';
  hexagramName?: string;
  changedHexagramName?: string;
  numbers?: number[];
  date: string;  // 占卜日期时间，必须包含时间；支持 YYYY-MM-DDTHH:MM[:SS]、YYYY-MM-DD HH:MM[:SS] 及带时区偏移的 ISO 时间
  seed?: string;
  seedScope?: string;
  detailLevel?: DetailLevel;
}

export interface LiuyaoOutput {
  question: string;
  seed?: string;
  // 本卦信息
  hexagramName: string;
  hexagramGong: string;
  hexagramElement: string;
  hexagramBrief?: string;
  guaCi?: string;
  xiangCi?: string;
  // 变卦信息
  changedHexagramName?: string;
  changedHexagramGong?: string;
  changedHexagramElement?: string;
  changedGuaCi?: string;
  changedXiangCi?: string;
  // 时间信息
  ganZhiTime: GanZhiTime;
  kongWang: KongWangInfo;
  kongWangByPillar: KongWangByPillarInfo;
  // 爻信息
  fullYaos: FullYaoInfo[];
  // 用神系统
  yongShen: YongShenGroupInfo[];
  fuShen?: FuShenInfo[];
  shenSystemByYongShen: ShenSystemByYongShenInfo[];
  globalShenSha: string[];
  // 分析结果
  liuChongGuaInfo?: LiuChongGuaInfo;
  liuHeGuaInfo?: LiuHeGuaInfo;
  chongHeTransition?: ChongHeTransition;
  guaFanFuYin?: GuaFanFuYinInfo;
  sanHeAnalysis?: SanHeAnalysisInfo;
  warnings?: string[];
  timeRecommendations?: TimeRecommendation[];
  // 互卦/错卦/综卦
  nuclearHexagram?: DerivedHexagramInfo;
  oppositeHexagram?: DerivedHexagramInfo;
  reversedHexagram?: DerivedHexagramInfo;
  // 卦身
  guaShen?: GuaShenInfo;
}
