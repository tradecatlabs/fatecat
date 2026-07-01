
import type { KongWangProfile } from '../types/analysis';

export function analyzeKongWangProfile(
  pillars: Array<{ gan: string; zhi: string }>,
  dayMasterStem: string,
): KongWangProfile {
  const stems = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'];
  const branches = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
  const pillarNames = ['year', 'month', 'day', 'hour'];

  // Find day pillar index to determine xun
  const dayIdx = pillars.findIndex((_, idx) => {
    const pillarNamesLookup = ['year', 'month', 'day', 'hour'];
    return pillarNamesLookup[idx] === 'day';
  });
  const dayGan = pillars[2].gan;
  const dayZhi = pillars[2].zhi;
  const gi = stems.indexOf(dayGan);
  const zi = branches.indexOf(dayZhi);
  const xunStart = gi - zi;
  const emptyIdx1 = (10 + zi - gi) % 12;
  const emptyIdx2 = (11 + zi - gi) % 12;
  const emptyBranches = [branches[emptyIdx1], branches[emptyIdx2]];

  const cnItems = pillarNames.map((pn, idx) => {
    const isEmpty = emptyBranches.includes(pillars[idx].zhi);
    return { pillar: pn, emptyBranches, isEmpty, fillableItems: [] };
  });

  return { items: cnItems, summary: '旬空：' + emptyBranches.join('、') };
}
