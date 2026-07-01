import type {
  DayunItemJSON
} from '../shared/json-types.js';

// ===== 大运 =====

export interface DayunCanonicalJSON {
  起运信息: {
    起运年龄: number;
    起运详情: string;
  };
  小运?: Array<{
    年龄: number;
    干支: string;
    十神: string;
  }>;
  大运列表: DayunItemJSON[];
}
