import type { BaziChartResult } from '../baziTypes';

export interface CheckContext {
  condition: string;
  dayStem: string;
  pillars: BaziChartResult['pillars'];
  hiddenStems: BaziChartResult['hiddenStems'];
  allBranches: string[];
  allStems: string[];
}

export type Matcher = (ctx: CheckContext) => boolean | null;
