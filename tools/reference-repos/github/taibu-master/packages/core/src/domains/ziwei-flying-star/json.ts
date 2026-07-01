import type {
  ZiweiFlyingStarResultJSON
} from '../shared/json-types.js';
import type {
  ZiweiFlyingStarCanonicalJSON,
} from './json-types.js';
import {
  mapZiweiFlyingStarQueryType
} from '../../shared/render-utils.js';
import type {
  MutagedPlaceInfo,
  SurroundedPalaceInfo,
} from '../shared/types.js';
import type {
  ZiweiFlyingStarOutput
} from './types.js';

export function renderZiweiFlyingStarCanonicalJSON(
  result: ZiweiFlyingStarOutput,
): ZiweiFlyingStarCanonicalJSON {
  const formatPalace = (name: string | null | undefined) => {
    if (!name) return null;
    return name.endsWith('宫') ? name : `${name}宫`;
  };

  return {
    查询结果: result.results.map((r) => {
      const entry: ZiweiFlyingStarResultJSON = {
        查询序号: r.queryIndex + 1,
        查询类型: mapZiweiFlyingStarQueryType(r.type),
      };

      if (r.type === 'fliesTo') {
        if (r.queryTarget?.fromPalace && r.queryTarget?.toPalace && r.queryTarget?.mutagens?.length) {
          entry.判断目标 = `${formatPalace(r.queryTarget.fromPalace)} -> ${formatPalace(r.queryTarget.toPalace)} [${r.queryTarget.mutagens.join('、')}]`;
        }
        entry.结果 = (r.result as boolean) ? '是' : '否';
        if (r.actualFlights?.length) {
          entry.实际飞化 = r.actualFlights.map((item) => ({
            四化: item.mutagen,
            宫位: formatPalace(item.targetPalace),
            ...(item.starName ? { 星曜: item.starName } : {}),
          }));
        }
      } else if (r.type === 'selfMutaged') {
        if (r.queryTarget?.palace && r.queryTarget?.mutagens?.length) {
          entry.判断目标 = `${formatPalace(r.queryTarget.palace)} [${r.queryTarget.mutagens.join('、')}]`;
        }
        entry.结果 = (r.result as boolean) ? '是' : '否';
      } else if (r.type === 'mutagedPlaces') {
        if (r.queryTarget?.palace) {
          const sourcePalace = formatPalace(r.queryTarget.palace);
          if (sourcePalace) entry.发射宫位 = sourcePalace;
        }
        if (r.sourcePalaceGanZhi) entry.发射宫干支 = r.sourcePalaceGanZhi;
        const flights = r.actualFlights || (r.result as MutagedPlaceInfo[]).map((item) => ({
          mutagen: item.mutagen,
          targetPalace: item.targetPalace,
          starName: null,
        }));
        entry.四化落宫 = flights.map((p) => ({
          四化: p.mutagen,
          宫位: formatPalace(p.targetPalace),
          ...(p.starName ? { 星曜: p.starName } : {}),
        }));
      } else if (r.type === 'surroundedPalaces') {
        const s = r.result as SurroundedPalaceInfo;
        const targetPalace = formatPalace(s.target.name);
        if (targetPalace) entry.本宫 = targetPalace;
        entry.矩阵宫位 = {
          对宫: formatPalace(s.opposite.name) || '-',
          三合1: formatPalace(s.wealth.name) || '-',
          三合2: formatPalace(s.career.name) || '-',
        };
      }

      return entry;
    }),
  };
}
