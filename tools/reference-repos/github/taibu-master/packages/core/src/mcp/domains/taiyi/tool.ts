import { calculateTaiyi } from '../../../domains/taiyi/calculate.js';
import { renderTaiyiCanonicalJSON } from '../../../domains/taiyi/json.js';
import { renderTaiyiCanonicalText } from '../../../domains/taiyi/text.js';
import type { TaiyiInput, TaiyiOutput } from '../../../domains/taiyi/types.js';
import { defineToolContract } from '../../contract.js';

import { taiyiDefinition } from './definition.js';
import { taiyiOutputSchema } from './output-schema.js';

export const taiyiManifest = defineToolContract<TaiyiInput, TaiyiOutput>({
  definition: taiyiDefinition,
  execute: calculateTaiyi,
  renderText: renderTaiyiCanonicalText,
  renderJSON: renderTaiyiCanonicalJSON,
  outputSchema: taiyiOutputSchema,
});
