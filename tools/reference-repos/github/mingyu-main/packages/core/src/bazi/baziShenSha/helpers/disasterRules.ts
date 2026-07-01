import type { RuleContext, ShenShaRuleMap } from './types';

/**
 * 灾厄神煞规则
 */
export function buildDisasterRules(ctx: RuleContext): ShenShaRuleMap {
  const { zhi, nianGan, nianZhi, yueZhi, riGan, riZhi, isMan, ctg, cdz, zhiIdx, baziArray } = ctx;

  return {
    空亡: () => {
      // 以日柱和年柱的旬查空亡地支，看当前柱地支是否落入
      // 注：同时以日柱和年柱判定空亡，较传统仅以日柱定空亡更为宽松。
      // 此为兼容多流派应用，调用方可按需仅取日柱空亡。
      const getEmptyBranches = (g: string, z: string): string[] => {
        const gIdx = ctg.indexOf(g);
        const zIdx = cdz.indexOf(z);
        if (gIdx === -1 || zIdx === -1) return [];
        const e1 = (10 + zIdx - gIdx) % 12;
        const e2 = (11 + zIdx - gIdx) % 12;
        return [cdz[e1], cdz[e2]];
      };
      const riEmpty = getEmptyBranches(riGan, riZhi);
      const nianEmpty = getEmptyBranches(nianGan, nianZhi);
      return riEmpty.includes(zhi) || nianEmpty.includes(zhi);
    },
    亡神: () => {
      const map: Record<string, string> = {
        申: '亥',
        子: '亥',
        辰: '亥',
        亥: '申',
        卯: '申',
        未: '申',
        寅: '巳',
        午: '巳',
        戌: '巳',
        巳: '寅',
        酉: '寅',
        丑: '寅',
      };
      return map[nianZhi] === zhi || map[riZhi] === zhi;
    },
    劫煞: () => {
      const map: Record<string, string> = {
        申: '巳',
        子: '巳',
        辰: '巳',
        亥: '寅',
        卯: '寅',
        未: '寅',
        寅: '亥',
        午: '亥',
        戌: '亥',
        巳: '申',
        酉: '申',
        丑: '申',
      };
      return map[nianZhi] === zhi || map[riZhi] === zhi;
    },
    灾煞: () => {
      const map: Record<string, string> = {
        申: '午',
        子: '午',
        辰: '午',
        亥: '酉',
        卯: '酉',
        未: '酉',
        寅: '子',
        午: '子',
        戌: '子',
        巳: '卯',
        酉: '卯',
        丑: '卯',
      };
      return map[nianZhi] === zhi || map[riZhi] === zhi;
    },
    元辰: () => {
      const nianGanIsYang = ctg.indexOf(nianGan) % 2 === 0;
      const offset = (nianGanIsYang && isMan) || (!nianGanIsYang && !isMan) ? 5 : 7;
      const targetIdx = (zhiIdx(nianZhi) + offset + 12) % 12;
      return cdz[targetIdx] === zhi;
    },
    血刃: () => {
      const map: Record<string, string> = {
        寅: '丑',
        卯: '寅',
        辰: '卯',
        巳: '辰',
        午: '巳',
        未: '午',
        申: '未',
        酉: '申',
        戌: '酉',
        亥: '戌',
        子: '亥',
        丑: '子',
      };
      return map[yueZhi] === zhi;
    },
    流霞: () => {
      const map: Record<string, string> = {
        甲: '酉',
        乙: '戌',
        丙: '未',
        丁: '申',
        戊: '巳',
        己: '午',
        庚: '辰',
        辛: '卯',
        壬: '亥',
        癸: '寅',
      };
      return map[riGan] === zhi;
    },
    天罗: () => {
      // 戌亥互见为天罗
      const hasXu = baziArray.some((p) => p[1] === '戌');
      const hasHai = baziArray.some((p) => p[1] === '亥');
      return hasXu && hasHai && (zhi === '戌' || zhi === '亥');
    },
    地网: () => {
      // 辰巳互见为地网
      const hasChen = baziArray.some((p) => p[1] === '辰');
      const hasSi = baziArray.some((p) => p[1] === '巳');
      return hasChen && hasSi && (zhi === '辰' || zhi === '巳');
    },
    天医: () => {
      // 正月(寅)见丑，二月(卯)见寅... 即月令前一位
      const monthIdx = cdz.indexOf(yueZhi);
      if (monthIdx === -1) return false;
      const targetIdx = (monthIdx - 1 + 12) % 12;
      return cdz[targetIdx] === zhi;
    },
    丧门: () => cdz[(zhiIdx(nianZhi) + 2) % 12] === zhi,
    吊客: () => cdz[(zhiIdx(nianZhi) - 2 + 12) % 12] === zhi,
    披麻: () => cdz[(zhiIdx(nianZhi) - 3 + 12) % 12] === zhi,
  };
}
