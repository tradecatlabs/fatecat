export type TaiyiMode = 'year' | 'month' | 'day' | 'hour' | 'minute';

export interface TaiyiInput {
  mode: TaiyiMode;
  date: string;
  hour?: number;
  minute?: number;
  timezone?: string;
  question?: string;
}

export interface TaiyiStarSnapshot {
  scale: TaiyiMode | 'support';
  scaleLabel: string;
  index: number;
  number: number;
  color: string;
  wuXing: string;
  position: string;
  positionDesc: string;
  beidouName: string;
  xuankongName: string;
  qimenName: string;
  qimenLuck: string;
  qimenYinYang: string;
  qimenGate?: string;
  taiyiName: string;
  taiyiType: string;
  song: string;
}

export interface TaiyiMinuteRefinement {
  slot: number;
  startMinute: number;
  endMinute: number;
  refinedStar: TaiyiStarSnapshot;
  note: string;
}

export interface TaiyiBoardMeta {
  system: 'taiyi_nine_star';
  systemLabel: string;
  mode: TaiyiMode;
  modeLabel: string;
  minuteSlot?: number;
  minuteStrategy?: string;
}

export interface TaiyiDatetimeContext {
  solarDateTime: string;
  lunarDate: string;
  jieQi?: string;
  yearGanZhi: string;
  monthGanZhi: string;
  dayGanZhi: string;
  hourGanZhi: string;
  xiu: string;
  xiuLuck: string;
  dayOfficer: string;
  tianShen: string;
  tianShenLuck: string;
}

export interface TaiyiDerivedIndicators {
  favorableSignals: string[];
  cautionSignals: string[];
  elementRelation: string;
  directionalHint: string;
}

export interface TaiyiJudgementAnchors {
  summary: string[];
  primarySong: string;
  modeNotes: string[];
}

export interface TaiyiOutput {
  question?: string;
  boardMeta: TaiyiBoardMeta;
  datetimeContext: TaiyiDatetimeContext;
  coreBoard: {
    primaryStar: TaiyiStarSnapshot;
    yearStar: TaiyiStarSnapshot;
    monthStar: TaiyiStarSnapshot;
    dayStar: TaiyiStarSnapshot;
    hourStar: TaiyiStarSnapshot;
    minuteRefinement?: TaiyiMinuteRefinement;
  };
  derivedIndicators: TaiyiDerivedIndicators;
  judgementAnchors: TaiyiJudgementAnchors;
}
