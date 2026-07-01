import { calculateZiweiData } from '../../../domains/ziwei/calculate.js';
import {
  defineToolContract,
  mergePlaceResolutionInfo,
} from '../../contract.js';
import { renderZiweiCanonicalJSON } from '../../../domains/ziwei/json.js';
import { ziweiCalculateOutputSchema } from './output-schema.js';
import { ziweiCalculateDefinition } from './definition.js';
import { renderZiweiCanonicalText } from '../../../domains/ziwei/text.js';
import type { ZiweiInput, ZiweiOutput } from '../../../domains/ziwei/types.js';

export const ziweiManifest = defineToolContract<ZiweiInput, ZiweiOutput>({
  definition: ziweiCalculateDefinition,
  execute: calculateZiweiData,
  renderText: renderZiweiCanonicalText,
  renderJSON: renderZiweiCanonicalJSON,
  outputSchema: ziweiCalculateOutputSchema,
  mergeRuntimeExtras: mergePlaceResolutionInfo,
});
