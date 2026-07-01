import { normalizeDetailLevelBinary } from '../../shared/render-utils.js';
import { GAN_WUXING } from '../../shared/utils.js';

import type { TaiyiCanonicalTextOptions } from '../shared/text-options.js';
import type { TaiyiCanonicalJSON } from './json-types.js';
import type { TaiyiOutput, TaiyiStarSnapshot } from './types.js';

function formatMappingReference(star: TaiyiStarSnapshot): string {
  return `${star.qimenName} / ${star.xuankongName}`;
}

function formatScaleLabel(star: TaiyiStarSnapshot): string {
  return star.scale === 'minute' ? '分钟主星' : star.scaleLabel;
}

function buildEnergyInteraction(result: TaiyiOutput): string {
  const dayStem = result.datetimeContext.dayGanZhi.charAt(0);
  const dayElement = GAN_WUXING[dayStem] || '';
  const dayStemLabel = dayElement ? `${dayStem}(${dayElement})` : dayStem;
  return `当前主星【${result.coreBoard.primaryStar.taiyiName}(${result.coreBoard.primaryStar.wuXing})】${result.derivedIndicators.elementRelation.replace('主星五行', '')}【${dayStemLabel}】`;
}

export function renderTaiyiCanonicalJSON(
  result: TaiyiOutput,
  options: { detailLevel?: TaiyiCanonicalTextOptions['detailLevel']; } = {},
): TaiyiCanonicalJSON {
  normalizeDetailLevelBinary(options.detailLevel);
  const timeLabel = `${result.datetimeContext.solarDateTime}（${result.datetimeContext.yearGanZhi}年 ${result.datetimeContext.monthGanZhi}月 ${result.datetimeContext.dayGanZhi}日 ${result.datetimeContext.hourGanZhi}时）`;
  const json: TaiyiCanonicalJSON = {
    问卜与时空底盘: {
      ...(result.question ? { 占问: result.question } : {}),
      时间: timeLabel,
      农历: result.datetimeContext.lunarDate,
      ...(result.datetimeContext.jieQi ? { 节气: result.datetimeContext.jieQi } : {}),
      四柱: `${result.datetimeContext.yearGanZhi} ${result.datetimeContext.monthGanZhi} ${result.datetimeContext.dayGanZhi} ${result.datetimeContext.hourGanZhi}`,
      ...(result.coreBoard.minuteRefinement
        ? { 分钟段: `第 ${result.coreBoard.minuteRefinement.slot} 段（${String(result.coreBoard.minuteRefinement.startMinute).padStart(2, '0')}-${String(result.coreBoard.minuteRefinement.endMinute).padStart(2, '0')} 分）` }
        : {}),
    },
    外部时空环境: {
      星宿: `${result.datetimeContext.xiu}${result.datetimeContext.xiuLuck ? `（${result.datetimeContext.xiuLuck}）` : ''}`,
      值星: result.datetimeContext.dayOfficer,
      天神: `${result.datetimeContext.tianShen}${result.datetimeContext.tianShenLuck ? `（${result.datetimeContext.tianShenLuck}）` : ''}`,
    },
    核心物理关系: {
      能量交互: buildEnergyInteraction(result),
    },
    九星阵列: [
      result.coreBoard.yearStar,
      result.coreBoard.monthStar,
      result.coreBoard.dayStar,
      result.coreBoard.hourStar,
      ...(result.coreBoard.minuteRefinement ? [result.coreBoard.minuteRefinement.refinedStar] : []),
    ].map((star) => ({
      观测层级: formatScaleLabel(star),
      太乙名: star.taiyiName,
      神性: star.taiyiType,
      北斗名: star.beidouName,
      映射参考: formatMappingReference(star),
      五行: star.wuXing,
      方位: star.positionDesc,
      宫位: star.position,
    })),
    古典参考: {
      主诀原文: result.judgementAnchors.primarySong,
      使用提示: '原文仅供意象联想，需结合前述时空底盘与九星阵列辩证解读。',
    },
  };

  return json;
}
