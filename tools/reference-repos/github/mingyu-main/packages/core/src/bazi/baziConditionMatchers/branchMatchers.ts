import type { Matcher } from './types';

const CHONG_REGEX = /([子丑寅卯辰巳午未申酉戌亥])([子丑寅卯辰巳午未申酉戌亥])冲/;
const JIAN_ZHI_REGEX = /见([子丑寅卯辰巳午未申酉戌亥])/;
const DI_ZHI_DUO_REGEX = /地支多([子丑寅卯辰巳午未申酉戌亥])/;

export const chongMatcher: Matcher = ({ condition, allBranches }) => {
  const match = condition.match(CHONG_REGEX);
  if (!match) return null;
  return allBranches.includes(match[1]) && allBranches.includes(match[2]);
};

export const jianZhiMatcher: Matcher = ({ condition, allBranches }) => {
  const match = condition.match(JIAN_ZHI_REGEX);
  if (!match) return null;
  return allBranches.includes(match[1]);
};

export const diZhiDuoMatcher: Matcher = ({ condition, allBranches }) => {
  const match = condition.match(DI_ZHI_DUO_REGEX);
  if (!match) return null;
  const target = match[1];
  const count = allBranches.filter((b) => b === target).length;
  return count >= 2;
};
