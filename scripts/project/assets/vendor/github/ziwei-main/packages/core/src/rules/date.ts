/**
 * 根据给定的小时数计算其对应的地支时辰索引。
 *
 * 地支时辰索引规则：
 * - 子时分为早子时（0点）和晚子时（23点），分别对应索引 0 和 12。
 * - 其他时间按照每两个小时一个时辰的规则计算索引。
 *
 * @param hour - 小时数（0~23之间的整数）
 * @returns 对应的地支时辰索引（0~12之间的整数）
 *
 * @example
 * getHourIndex(0);  // 返回 0（早子时）
 * getHourIndex(23); // 返回 12（晚子时）
 * getHourIndex(10); // 返回 6
 */
export function getHourIndex(hour: number) {
  return (hour + 1) >> 1;
}
