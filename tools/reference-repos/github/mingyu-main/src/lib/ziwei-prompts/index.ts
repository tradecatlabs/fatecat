import type { AnalysisPayloadV1 } from '../../types/analysis';
import { buildZiweiReadableSnapshot, buildZiweiTaskBookSnapshot } from './snapshot';
import type { PromptContext } from './types';

export type { PromptContext } from './types';

export function buildPortablePromptPack(params: {
  payload: AnalysisPayloadV1;
  reportContext: PromptContext;
  mode?: 'full' | 'task-book';
}) {
  const { payload, reportContext } = params;

  const builder =
    params.mode === 'task-book' ? buildZiweiTaskBookSnapshot : buildZiweiReadableSnapshot;

  return [builder({ payload, reportContext })].join('\n');
}
