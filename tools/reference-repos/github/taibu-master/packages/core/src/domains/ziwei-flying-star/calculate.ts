/**
 * 紫微斗数飞星分析核心引擎
 */

import type {
  FlyingStarResult,
  ZiweiFlyingStarInput,
  ZiweiFlyingStarOutput,
} from './types.js';
import type {
  FlyingStarActualFlight,
  FlyingStarQuery,
  MutagedPlaceInfo,
  SurroundedPalaceInfo,
} from '../shared/types.js';
import { createAstrolabeWithTrueSolar, MUTAGEN_NAMES, STEM_MUTAGEN_TABLE, type MutagenName } from '../ziwei/shared.js';

export type { ZiweiFlyingStarInput, ZiweiFlyingStarOutput } from './types.js';

type FunctionalPalace = NonNullable<ReturnType<ReturnType<typeof createAstrolabeWithTrueSolar>['astrolabe']['palace']>>;

function buildActualFlights(
  palace: FunctionalPalace,
  mutagens: readonly string[],
): FlyingStarActualFlight[] {
  const requested = mutagens.length > 0 ? mutagens : [...MUTAGEN_NAMES];
  const places = palace.mutagedPlaces();
  const stemMutagens = STEM_MUTAGEN_TABLE[palace.heavenlyStem] || ['', '', '', ''];

  const result: FlyingStarActualFlight[] = [];
  for (const mutagen of requested) {
    const index = MUTAGEN_NAMES.indexOf(mutagen as MutagenName);
    if (index < 0) continue;
    result.push({
      mutagen,
      targetPalace: places[index]?.name ?? null,
      starName: stemMutagens[index] || null,
    });
  }

  return result;
}

function processQuery(
  astrolabe: ReturnType<typeof createAstrolabeWithTrueSolar>['astrolabe'],
  query: FlyingStarQuery,
  idx: number,
): FlyingStarResult {
  switch (query.type) {
    case 'fliesTo': {
      const palace = astrolabe.palace(query.from);
      if (!palace) throw new Error(`宫位 "${query.from}" 不存在`);
      const mutagens = (query.mutagens || []) as MutagenName[];
      const result = palace.fliesTo(query.to, mutagens);
      return {
        queryIndex: idx,
        type: 'fliesTo',
        result,
        queryTarget: {
          fromPalace: query.from,
          toPalace: query.to,
          mutagens: [...mutagens],
        },
        sourcePalaceGanZhi: `${palace.heavenlyStem}${palace.earthlyBranch}`,
        actualFlights: buildActualFlights(palace, mutagens),
      };
    }
    case 'selfMutaged': {
      const palace = astrolabe.palace(query.palace);
      if (!palace) throw new Error(`宫位 "${query.palace}" 不存在`);
      const mutagens = (query.mutagens || MUTAGEN_NAMES) as MutagenName[];
      const result = palace.selfMutaged(mutagens);
      return {
        queryIndex: idx,
        type: 'selfMutaged',
        result,
        queryTarget: {
          palace: query.palace,
          mutagens: [...mutagens],
        },
        sourcePalaceGanZhi: `${palace.heavenlyStem}${palace.earthlyBranch}`,
      };
    }
    case 'mutagedPlaces': {
      const palace = astrolabe.palace(query.palace);
      if (!palace) throw new Error(`宫位 "${query.palace}" 不存在`);
      const places = palace.mutagedPlaces();
      const result: MutagedPlaceInfo[] = MUTAGEN_NAMES.map((m, i) => ({
        mutagen: m,
        targetPalace: places[i]?.name ?? null,
      }));
      return {
        queryIndex: idx,
        type: 'mutagedPlaces',
        result,
        queryTarget: {
          palace: query.palace,
        },
        sourcePalaceGanZhi: `${palace.heavenlyStem}${palace.earthlyBranch}`,
        actualFlights: buildActualFlights(palace, MUTAGEN_NAMES),
      };
    }
    case 'surroundedPalaces': {
      const surrounded = astrolabe.surroundedPalaces(query.palace);
      if (!surrounded) throw new Error(`宫位 "${query.palace}" 不存在`);
      const result: SurroundedPalaceInfo = {
        target: { name: surrounded.target.name, index: surrounded.target.index },
        opposite: { name: surrounded.opposite.name, index: surrounded.opposite.index },
        wealth: { name: surrounded.wealth.name, index: surrounded.wealth.index },
        career: { name: surrounded.career.name, index: surrounded.career.index },
      };
      return {
        queryIndex: idx,
        type: 'surroundedPalaces',
        result,
        queryTarget: {
          palace: query.palace,
        },
      };
    }
    default:
      throw new Error(`未知查询类型: ${(query as { type: string; }).type}`);
  }
}

export async function calculateZiweiFlyingStar(input: ZiweiFlyingStarInput): Promise<ZiweiFlyingStarOutput> {
  if (!input.queries || !Array.isArray(input.queries) || input.queries.length === 0) {
    throw new Error('queries 不能为空');
  }

  const { astrolabe } = createAstrolabeWithTrueSolar(input);
  const results = input.queries.map((q, i) => processQuery(astrolabe, q, i));

  return { results };
}
