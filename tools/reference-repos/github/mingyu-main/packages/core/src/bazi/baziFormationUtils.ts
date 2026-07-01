import type { Pillars, Wuxing } from './baziTypes';

export interface CompleteBranchFormation {
  type: '三合' | '三会';
  branches: string[];
  wuxing: Wuxing;
  includesMonthBranch: boolean;
}

const FORMATION_DEFINITIONS: Array<{
  type: '三合' | '三会';
  branches: string[];
  wuxing: Wuxing;
}> = [
  { type: '三合', branches: ['亥', '卯', '未'], wuxing: '木' },
  { type: '三会', branches: ['寅', '卯', '辰'], wuxing: '木' },
  { type: '三合', branches: ['寅', '午', '戌'], wuxing: '火' },
  { type: '三会', branches: ['巳', '午', '未'], wuxing: '火' },
  { type: '三合', branches: ['巳', '酉', '丑'], wuxing: '金' },
  { type: '三会', branches: ['申', '酉', '戌'], wuxing: '金' },
  { type: '三合', branches: ['申', '子', '辰'], wuxing: '水' },
  { type: '三会', branches: ['亥', '子', '丑'], wuxing: '水' },
];

const REPRESENTATIVE_STEM_BY_WUXING: Record<Wuxing, string> = {
  木: '甲',
  火: '丙',
  土: '戊',
  金: '庚',
  水: '壬',
};

export function getRepresentativeStemByWuxing(wuxing: Wuxing): string {
  return REPRESENTATIVE_STEM_BY_WUXING[wuxing];
}

export function collectCompleteBranchFormations(pillars: Pillars): CompleteBranchFormation[] {
  const uniqueBranches = new Set(Object.values(pillars).map((pillar) => pillar.zhi));

  return FORMATION_DEFINITIONS.filter((formation) =>
    formation.branches.every((branch) => uniqueBranches.has(branch)),
  ).map((formation) => ({
    ...formation,
    includesMonthBranch: formation.branches.includes(pillars.month.zhi),
  }));
}
