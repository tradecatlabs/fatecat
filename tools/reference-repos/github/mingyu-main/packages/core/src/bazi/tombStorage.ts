
import type { TombStorageItem, TombStorageProfile } from '../types/analysis';

const HIDDEN_STEMS: Record<string, string[]> = {
  子: ['癸'], 丑: ['己','癸','辛'], 寅: ['甲','丙','戊'],
  卯: ['乙'], 辰: ['戊','乙','癸'], 巳: ['丙','庚','戊'],
  午: ['丁','己'], 未: ['己','丁','乙'], 申: ['庚','壬','戊'],
  酉: ['辛'], 戌: ['戊','辛','丁'], 亥: ['壬','甲'],
};
const TOMB_BRANCH: Record<string, string> = { 金: '丑', 木: '未', 火: '戌', 水: '辰', 土: '辰' };
const WUXING_S: Record<string, string> = { 金: '丑', 木: '未', 火: '戌', 水: '辰', 土: '辰' };

export function analyzeTombStorage(
  pillars: Array<{ gan: string; zhi: string }>,
  dayMaster: string,
  getWuxing: (s: string) => string,
  getTenGod: (g: string, d: string) => string,
): TombStorageProfile {
  const items: TombStorageItem[] = [];
  const fourTombs = ['辰','戌','丑','未'];
  const dmWuxing = getWuxing(dayMaster);
  const dmTomb = TOMB_BRANCH[dmWuxing] || '';

  pillars.forEach(p => {
    if (!fourTombs.includes(p.zhi)) return;
    const stems = HIDDEN_STEMS[p.zhi] || [];
    const storageStem = stems[stems.length - 1] || stems[0];
    const storageWuxing = getWuxing(storageStem);
    items.push({
      branch: p.zhi, storageElement: storageWuxing,
      storageStem: storageStem,
      storageTenGod: getTenGod(storageStem, dayMaster),
      isDayMasterTomb: p.zhi === dmTomb,
    });
  });

  return { items, summary: '四库分析' };
}
