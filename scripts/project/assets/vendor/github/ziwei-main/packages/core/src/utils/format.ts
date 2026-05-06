import { SolarTime } from "tyme4ts";

import { BRANCH_KEYS } from "../constants";
import { i18n } from "../infra/i18n";

/**
 * 将日期对象格式化为标准日期时间文本字符串。
 *
 * @param date - 要格式化的日期对象，可以是 SolarTime 或 JavaScript 原生 Date 类型
 * @returns 格式化后的日期时间字符串，格式为："YYYY-MM-DD HH:MM"
 */
export function getSolarDateText(date: SolarTime | Date) {
  if (date instanceof SolarTime) {
    const _array = [date.getMonth(), date.getDay(), date.getHour(), date.getMinute()].map((n) =>
      String(n).padStart(2, "0"),
    );
    return `${date.getYear()}-${_array[0]}-${_array[1]} ${_array[2]}:${_array[3]}`;
  }
  const _array = [date.getMonth() + 1, date.getDate(), date.getHours(), date.getMinutes()].map(
    (n) => String(n).padStart(2, "0"),
  );
  return `${date.getFullYear()}-${_array[0]}-${_array[1]} ${_array[2]}:${_array[3]}`;
}

/**
 * 将阴阳合历（农历）时辰对象格式化为人类可读的文本字符串。
 *
 * 例如："甲子年正月初一 午时"。
 */
export function getLunisolarDateText(
  date: import("tyme4ts").LunarHour,
  hourIndex: number,
  translator: typeof i18n = i18n,
) {
  const lunarDay = date.getLunarDay();
  const lunarMonth = lunarDay.getLunarMonth();
  const lunarYear = lunarMonth.getLunarYear();
  return `${lunarYear.getName().slice(2)}${lunarMonth.getName()}${lunarDay.getName()} ${translator.$t(`branch.${BRANCH_KEYS[hourIndex]}`)}${translator.$t(`hour`)}`;
}
