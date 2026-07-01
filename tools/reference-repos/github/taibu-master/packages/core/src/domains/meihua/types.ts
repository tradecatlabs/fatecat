import type {
  DerivedHexagramInfo,
  DetailLevel,
  DiZhi,
  GanZhiTime,
  WuXing
} from '../shared/types.js';

// ===== 梅花易数相关类型 =====

export type MeihuaMethodFamily = 'classical' | 'extended';

export type MeihuaMethod =
  | 'time'
  | 'count_with_time'
  | 'text_split'
  | 'measure'
  | 'classifier_pair'
  | 'select'
  | 'number_pair'
  | 'number_triplet';

export type MeihuaTextSplitMode = 'auto' | 'count' | 'sentence_pair' | 'stroke';

export type MeihuaMultiSentenceStrategy = 'first' | 'last';

export type MeihuaMeasureKind = '丈尺' | '尺寸';

export type MeihuaCountCategory = 'item' | 'sound';

export type MeihuaCueCategory = 'direction' | 'color' | 'weather' | 'person' | 'body' | 'animal' | 'object' | 'shape' | 'trigram';

export type MeihuaSeasonState = '旺' | '相' | '休' | '囚' | '死';

export type MeihuaOutcome = '吉' | '平' | '凶';

export interface MeihuaInput {
  question: string;
  date: string;
  method?: MeihuaMethod;
  count?: number;
  countCategory?: MeihuaCountCategory;
  text?: string;
  textSplitMode?: MeihuaTextSplitMode;
  multiSentenceStrategy?: MeihuaMultiSentenceStrategy;
  sentences?: string[];
  leftStrokeCount?: number;
  rightStrokeCount?: number;
  measureKind?: MeihuaMeasureKind;
  majorValue?: number;
  minorValue?: number;
  upperCue?: string;
  lowerCue?: string;
  upperCueCategory?: MeihuaCueCategory;
  lowerCueCategory?: MeihuaCueCategory;
  upperTrigram?: string;
  lowerTrigram?: string;
  movingLine?: number;
  hexagramName?: string;
  numbers?: number[];
  detailLevel?: DetailLevel;
}

export interface MeihuaTrigramInfo {
  name: string;
  code: string;
  number: number;
  element: WuXing;
}

export interface MeihuaHexagramInfo {
  name: string;
  code: string;
  upperTrigram: MeihuaTrigramInfo;
  lowerTrigram: MeihuaTrigramInfo;
  element: WuXing;
  guaCi?: string;
  xiangCi?: string;
}

export interface MeihuaCastNumbers {
  upper: number;
  lower: number;
  moving: number;
  total?: number;
  hour?: number;
}

export interface MeihuaCastInputSnapshot {
  date: string;
  count?: number;
  countCategory?: MeihuaCountCategory;
  text?: string;
  sentences?: string[];
  selectedText?: string;
  multiSentenceStrategy?: MeihuaMultiSentenceStrategy;
  leftStrokeCount?: number;
  rightStrokeCount?: number;
  measureKind?: MeihuaMeasureKind;
  majorValue?: number;
  minorValue?: number;
  upperCue?: string;
  lowerCue?: string;
  upperCueCategory?: MeihuaCueCategory;
  lowerCueCategory?: MeihuaCueCategory;
  hexagramName?: string;
  upperTrigram?: string;
  lowerTrigram?: string;
  movingLine?: number;
  numbers?: number[];
}

export interface MeihuaCastMeta {
  method: MeihuaMethod;
  methodFamily: MeihuaMethodFamily;
  methodLabel: string;
  resolvedMode?: 'time' | 'count_with_time' | 'count' | 'tone' | 'sentence_pair' | 'stroke' | 'measure' | 'classifier_pair' | 'select' | 'number_pair' | 'number_triplet';
  inputSummary: string[];
  resolvedNumbers?: MeihuaCastNumbers;
  inputSnapshot?: MeihuaCastInputSnapshot;
}

export interface MeihuaBodyUseRelation {
  relation: '比和' | '体生用' | '用生体' | '体克用' | '用克体';
  favorable: boolean;
  summary: string;
}

export interface MeihuaSeasonalState {
  monthBranch: DiZhi;
  body: MeihuaSeasonState;
  use: MeihuaSeasonState;
  bodyMutual?: MeihuaSeasonState;
  useMutual?: MeihuaSeasonState;
  changed?: MeihuaSeasonState;
}

export interface MeihuaInteractionReading {
  stage: 'use' | 'body_mutual' | 'use_mutual' | 'changed';
  stageLabel: string;
  relation: '比和' | '体生用' | '用生体' | '体克用' | '用克体';
  favorable: boolean;
  summary: string;
}

export interface MeihuaTimingHint {
  phase: 'early' | 'middle' | 'late';
  trigger: string;
  summary: string;
}

export interface MeihuaJudgement {
  outcome: MeihuaOutcome;
  summary: string;
  basis: string[];
}

export interface MeihuaOutput {
  question: string;
  castMeta: MeihuaCastMeta;
  ganZhiTime: GanZhiTime;
  mainHexagram: MeihuaHexagramInfo;
  changedHexagram?: MeihuaHexagramInfo;
  nuclearHexagram?: MeihuaHexagramInfo;
  oppositeHexagram?: DerivedHexagramInfo;
  reversedHexagram?: DerivedHexagramInfo;
  movingLine: number;
  bodyTrigram: MeihuaTrigramInfo;
  useTrigram: MeihuaTrigramInfo;
  bodyMutualTrigram?: MeihuaTrigramInfo;
  useMutualTrigram?: MeihuaTrigramInfo;
  bodyUseRelation: MeihuaBodyUseRelation;
  seasonalState: MeihuaSeasonalState;
  interactionReadings: MeihuaInteractionReading[];
  timingHints: MeihuaTimingHint[];
  judgement: MeihuaJudgement;
  warnings: string[];
}
