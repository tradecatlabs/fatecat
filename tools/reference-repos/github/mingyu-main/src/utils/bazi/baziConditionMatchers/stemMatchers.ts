import type { Matcher } from './types';

const TOU_GAN_REGEX = /([甲乙丙丁戊己庚辛壬癸])[金木水火土]?透干/;
const FA_YONG_REGEX = /([甲乙丙丁戊己庚辛壬癸])[金木水火土]?发用/;
const TIAN_GAN_DUO_REGEX = /天干三([甲乙丙丁戊己庚辛壬癸])/;
const WU_HE_REGEX = /([甲乙丙丁戊己庚辛壬癸])([甲乙丙丁戊己庚辛壬癸])同透/;
const NO_ZHENG_HE_REGEX = /无([甲乙丙丁戊己庚辛壬癸])([甲乙丙丁戊己庚辛壬癸])争合/;

export const touGanMatcher: Matcher = ({ condition, allStems }) => {
  const match = condition.match(TOU_GAN_REGEX);
  if (!match) return null;
  return allStems.includes(match[1]);
};

export const faYongMatcher: Matcher = ({ condition, allStems }) => {
  const match = condition.match(FA_YONG_REGEX);
  if (!match) return null;
  return allStems.includes(match[1]);
};

export const tianGanDuoMatcher: Matcher = ({ condition, allStems }) => {
  const match = condition.match(TIAN_GAN_DUO_REGEX);
  if (!match) return null;
  const target = match[1];
  const count = allStems.filter((s) => s === target).length;
  return count >= 3;
};

export const wuHeMatcher: Matcher = ({ condition, allStems }) => {
  const match = condition.match(WU_HE_REGEX);
  if (!match) return null;
  return allStems.includes(match[1]) && allStems.includes(match[2]);
};

export const noZhengHeMatcher: Matcher = ({ condition, allStems }) => {
  const match = condition.match(NO_ZHENG_HE_REGEX);
  if (!match) return null;
  // 争合（妒合）指一干合多干：合干之一在命局出现 ≥2 次方为争合、破化气之纯；
  // 乙庚各一为正合，化气成立。原实现“两干同时出现即判争合”，而化气格本就要求
  // 乙庚同透，会令所有化气格恒被破局。
  const count1 = allStems.filter((s) => s === match[1]).length;
  const count2 = allStems.filter((s) => s === match[2]).length;
  return !(count1 >= 2 || count2 >= 2);
};
