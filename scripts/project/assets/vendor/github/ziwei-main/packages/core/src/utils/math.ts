/**
 * 用于处理索引，欧几里得取模，将索引锁定在 0~max 范围内
 *
 * @param index 当前索引
 * @param max 最大循环数，默认为12
 * @returns 处理后的索引
 */
export function wrapIndex(index: number, max: number = 12) {
  if (max <= 0) throw new Error("最大值 max 必须大于 0");
  // 使用取模操作将索引限制在 0 到 max-1 范围内
  return ((index % max) + max) % max;
}

/**
 * 获取传入索引的相对宫位索引
 * @param index
 * @returns
 */
export function relativeIndex(index: number, max: number = 12) {
  return wrapIndex(max - index);
}

/**
 * 获取传入索引的本对宫位索引
 * @param index
 * @returns
 */
export function oppositeIndex(index: number, max: number = 12) {
  return wrapIndex(index + max / 2);
}
