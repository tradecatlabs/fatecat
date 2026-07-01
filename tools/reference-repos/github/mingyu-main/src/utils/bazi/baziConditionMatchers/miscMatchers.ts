import { BASIC_MAPPINGS, LU_BRANCH_MAP } from '../baziDefinitions';
import type { Matcher } from './types';

const ZHI_CHONG_MAP = BASIC_MAPPINGS.DI_ZHI_CHONG;

export const luShenChongMatcher: Matcher = ({ condition, dayStem, allBranches }) => {
  if (!condition.includes('禄神逢冲')) return null;

  const luZhi = LU_BRANCH_MAP[dayStem];
  if (!luZhi || !allBranches.includes(luZhi)) {
    return false;
  }
  const chongZhi = ZHI_CHONG_MAP[luZhi];
  return chongZhi ? allBranches.includes(chongZhi) : false;
};
