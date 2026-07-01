import { calculateMeihua } from '../../../domains/meihua/calculate.js';
import { defineToolContract } from '../../contract.js';
import { renderMeihuaCanonicalJSON } from '../../../domains/meihua/json.js';
import { meihuaOutputSchema } from './output-schema.js';
import { meihuaDefinition } from './definition.js';
import { renderMeihuaCanonicalText } from '../../../domains/meihua/text.js';
import type { MeihuaInput, MeihuaOutput } from '../../../domains/meihua/types.js';

export const meihuaManifest = defineToolContract<MeihuaInput, MeihuaOutput>({
  definition: meihuaDefinition,
  execute: calculateMeihua,
  renderText: renderMeihuaCanonicalText,
  renderJSON: renderMeihuaCanonicalJSON,
  outputSchema: meihuaOutputSchema,
});
