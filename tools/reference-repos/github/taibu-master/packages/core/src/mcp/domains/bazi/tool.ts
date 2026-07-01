import { calculateBaziData } from '../../../domains/bazi/calculate.js';
import {
  defineToolContract,
  mergePlaceResolutionInfo,
} from '../../contract.js';
import { renderBaziCanonicalJSON } from '../../../domains/bazi/json.js';
import { baziCalculateOutputSchema } from './output-schema.js';
import { baziCalculateDefinition } from './definition.js';
import { renderBaziCanonicalText } from '../../../domains/bazi/text.js';
import type { BaziInput, BaziOutput } from '../../../domains/bazi/types.js';

export const baziManifest = defineToolContract<BaziInput, BaziOutput>({
  definition: baziCalculateDefinition,
  execute: calculateBaziData,
  renderText: renderBaziCanonicalText,
  renderJSON: renderBaziCanonicalJSON,
  outputSchema: baziCalculateOutputSchema,
  mergeRuntimeExtras: mergePlaceResolutionInfo,
});
