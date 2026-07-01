import { calculateDailyAlmanac } from '../../../domains/almanac/calculate.js';
import { defineToolContract } from '../../contract.js';
import { renderAlmanacCanonicalJSON } from '../../../domains/almanac/json.js';
import { almanacOutputSchema } from './output-schema.js';
import { almanacDefinition } from './definition.js';
import { renderAlmanacCanonicalText } from '../../../domains/almanac/text.js';
import type { AlmanacInput, AlmanacOutput } from '../../../domains/almanac/types.js';

export const almanacManifest = defineToolContract<AlmanacInput, AlmanacOutput>({
  definition: almanacDefinition,
  execute: calculateDailyAlmanac,
  renderText: renderAlmanacCanonicalText,
  renderJSON: renderAlmanacCanonicalJSON,
  outputSchema: almanacOutputSchema,
});
