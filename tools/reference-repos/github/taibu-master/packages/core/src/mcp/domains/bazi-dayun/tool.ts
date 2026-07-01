import { calculateDayunData } from '../../../domains/bazi-dayun/calculate.js';
import {
  defineToolContract,
  mergePlaceResolutionInfo,
} from '../../contract.js';
import { renderDayunCanonicalJSON } from '../../../domains/bazi-dayun/json.js';
import { baziDayunOutputSchema } from './output-schema.js';
import { baziDayunDefinition } from './definition.js';
import { renderDayunCanonicalText } from '../../../domains/bazi-dayun/text.js';
import type { DayunInput, DayunOutput } from '../../../domains/bazi-dayun/types.js';

export const baziDayunManifest = defineToolContract<DayunInput, DayunOutput>({
  definition: baziDayunDefinition,
  execute: calculateDayunData,
  renderText: renderDayunCanonicalText,
  renderJSON: renderDayunCanonicalJSON,
  outputSchema: baziDayunOutputSchema,
  mergeRuntimeExtras: mergePlaceResolutionInfo,
});
