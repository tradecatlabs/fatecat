import { calculateQimenData } from '../../../domains/qimen/calculate.js';
import { defineToolContract } from '../../contract.js';
import { renderQimenCanonicalJSON } from '../../../domains/qimen/json.js';
import { qimenCalculateOutputSchema } from './output-schema.js';
import { qimenCalculateDefinition } from './definition.js';
import { renderQimenCanonicalText } from '../../../domains/qimen/text.js';
import type { QimenInput, QimenOutput } from '../../../domains/qimen/types.js';

export const qimenManifest = defineToolContract<QimenInput, QimenOutput>({
  definition: qimenCalculateDefinition,
  execute: calculateQimenData,
  renderText: renderQimenCanonicalText,
  renderJSON: renderQimenCanonicalJSON,
  outputSchema: qimenCalculateOutputSchema,
});
