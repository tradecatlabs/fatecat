/**
 * Deprecated: utils/date.ts 已拆分为更细的模块：
 * - utils/calendar.ts：日期换算与策略
 * - utils/trueSolarTime.ts：真太阳时
 * - utils/format.ts：文本格式化
 *
 * 为保持兼容性，此文件仅做聚合导出。
 */
export {
  calculateZiWeiDate,
  normalizeHour,
  fixLeapMonth,
  calculateNatalDateBySolar,
  calculateLunisolarDateBySolar,
  getStemAndBranchByYear,
  calculateHourByIndex,
} from "./calendar";
export { calculateTrueSolarTime } from "./trueSolarTime";
export { getSolarDateText, getLunisolarDateText } from "./format";
