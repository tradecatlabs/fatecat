import type {
  AlmanacInfo
} from '../shared/types.js';

// ===== 黄历相关类型 =====

export interface AlmanacInput {
  dayMaster?: string;
  birthYear?: number;
  birthMonth?: number;
  birthDay?: number;
  birthHour?: number;
  date?: string;
}

export interface AlmanacOutput {
  date: string;
  dayInfo: {
    stem: string;
    branch: string;
    ganZhi: string;
  };
  tenGod?: string;
  almanac: AlmanacInfo;
}
