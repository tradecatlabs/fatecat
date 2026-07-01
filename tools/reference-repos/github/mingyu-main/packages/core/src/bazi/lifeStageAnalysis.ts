
import type { TenGodLifeStageItem, TenGodLifeStageProfile } from '../types/analysis';

const TWELVE_STAGES = ['长生','沐浴','冠带','临官','帝旺','衰','病','死','墓','绝','胎','养'];
const TWELVE_STAGES_START: Record<string, string> = {
  木: '亥', 火: '寅', 金: '巳', 水: '申', 土: '申',
};

function getLifeStage(stem: string, branch: string): string {
  const elemMap: Record<string, string> = {
    甲: '木', 乙: '木', 丙: '火', 丁: '火',
    戊: '土', 己: '土', 庚: '金', 辛: '金', 壬: '水', 癸: '水',
  };
  const elem = elemMap[stem];
  const start = TWELVE_STAGES_START[elem || ''];
  if (!start) return '未知';
  const branches = ['寅','卯','辰','巳','午','未','申','酉','戌','亥','子','丑'];
  const si = branches.indexOf(start);
  const bi = branches.indexOf(branch);
  if (si === -1 || bi === -1) return '未知';
  return TWELVE_STAGES[((bi - si + 12) % 12)];
}

export function analyzeLifeStageProfile(
  pillars: Array<{ gan: string; zhi: string }>,
): Array<{ pillar: string; stage: string }> {
  const pillarNames = ['year', 'month', 'day', 'hour'];
  return pillars.map((p, idx) => ({
    pillar: pillarNames[idx], stage: getLifeStage(p.gan, p.zhi),
  }));
}

export function analyzeTenGodLifeStageProfile(
  pillars: Array<{ gan: string; zhi: string; hiddenStems: string[] }>,
  dayMaster: string,
  getTenGod: (g: string, d: string) => string,
): TenGodLifeStageProfile {
  const stageScores: Record<string, number> = { 临官: 1, 帝旺: 1, 长生: 0.5, 冠带: 0.5 };
  const lowScores: Record<string, number> = { 死: 1, 绝: 1, 病: 0.5, 墓: 0.5 };

  const tenGodMap: Record<string, { strong: number; low: number }> = {};

  const processStem = (stem: string) => {
    if (stem === dayMaster) return;
    const tg = getTenGod(stem, dayMaster);
    if (!tenGodMap[tg]) tenGodMap[tg] = { strong: 0, low: 0 };
    // Calculate life stage for each branch
    pillars.forEach(p => {
      const stage = getLifeStage(stem, p.zhi);
      if (stageScores[stage]) tenGodMap[tg].strong += stageScores[stage];
      if (lowScores[stage]) tenGodMap[tg].low += lowScores[stage];
    });
  };

  // Process visible stems
  pillars.forEach(p => { processStem(p.gan); });
  // Process hidden stems
  pillars.forEach(p => {
    (p.hiddenStems || []).forEach(s => processStem(s));
  });

  const items = Object.entries(tenGodMap).map(([tenGod, v]) => ({
    stem: '', tenGod, strongCount: v.strong, lowCount: v.low,
    summary: v.strong > v.low ? '旺位多于弱位' : v.low > v.strong ? '弱位多于旺位' : '旺弱相当',
  }));

  return { items, summary: '十神十二长生分析' };
}
