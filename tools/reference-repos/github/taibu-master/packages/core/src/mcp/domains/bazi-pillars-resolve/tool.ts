import { calculateBaziPillarsResolve } from '../../../domains/bazi-pillars-resolve/calculate.js';
import { defineToolContract } from '../../contract.js';
import { renderBaziPillarsResolveCanonicalJSON } from '../../../domains/bazi-pillars-resolve/json.js';
import { baziPillarsResolveOutputSchema } from './output-schema.js';
import { baziPillarsResolveDefinition } from './definition.js';
import { renderBaziPillarsResolveCanonicalText } from '../../../domains/bazi-pillars-resolve/text.js';
import type { BaziPillarsResolveInput, BaziPillarsResolveOutput } from '../../../domains/bazi-pillars-resolve/types.js';

export const baziPillarsResolveManifest = defineToolContract<BaziPillarsResolveInput, BaziPillarsResolveOutput>({
  definition: baziPillarsResolveDefinition,
  execute: calculateBaziPillarsResolve,
  renderText: renderBaziPillarsResolveCanonicalText,
  renderJSON: renderBaziPillarsResolveCanonicalJSON,
  outputSchema: baziPillarsResolveOutputSchema,
});
