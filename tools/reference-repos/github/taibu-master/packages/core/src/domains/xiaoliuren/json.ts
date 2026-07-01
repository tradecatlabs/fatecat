import type { XiaoliurenCanonicalJSON } from './json-types.js';
import type { XiaoliurenOutput } from './types.js';
import type { XiaoliurenCanonicalTextOptions } from './text.js';
import { normalizeDetailLevelBinary } from '../../shared/render-utils.js';

export function toXiaoliurenJson(
  output: XiaoliurenOutput,
  options: XiaoliurenCanonicalTextOptions = {},
): XiaoliurenCanonicalJSON {
  const detailLevel = normalizeDetailLevelBinary(options.detailLevel);
  const showPoem = options.showPoem ?? detailLevel === 'full';

  return {
    起课信息: {
      ...(output.question ? { 占问: output.question } : {}),
      农历月: output.input.lunarMonth,
      农历日: output.input.lunarDay,
      时辰: output.input.shichen,
      时辰序号: output.input.hour,
    },
    推演链: {
      月上起: output.monthStatus,
      日上落: output.dayStatus,
      时上落: output.hourStatus,
    },
    结果: {
      落宫: output.result.name,
      五行: output.result.element,
      方位: output.result.direction,
      性质: output.result.nature,
      ...(detailLevel === 'full' ? { 释义: output.result.description } : {}),
      ...(showPoem ? { 诗诀: output.result.poem } : {}),
    },
  };
}
