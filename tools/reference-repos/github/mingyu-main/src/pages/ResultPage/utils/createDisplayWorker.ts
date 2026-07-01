import { attachWorkerSafety } from '@/hooks/useWorkerRequest';
import type { AnalysisPayloadV1, ScopeType } from '@/types/analysis';
import type { ChartInput } from '@/types/chart';

export function createDisplayWorker(
  message: { id: string; input: ChartInput; dateStr: string; hourIndex: number; scope: ScopeType },
  onSuccess: (payload: AnalysisPayloadV1) => void,
  onError: () => void,
): () => void {
  const worker = new Worker(new URL('../../../workers/ziwei-display.worker.ts', import.meta.url), {
    type: 'module',
  });
  const disarm = attachWorkerSafety(worker, { onError });
  worker.onmessage = (
    event: MessageEvent<{
      id: string;
      ok: boolean;
      payload?: AnalysisPayloadV1;
    }>,
  ) => {
    if (event.data.id !== message.id) {
      return;
    }
    disarm();

    if (event.data.ok && event.data.payload) {
      onSuccess(event.data.payload);
    } else {
      onError();
    }

    worker.terminate();
  };

  worker.postMessage(message);

  return () => {
    disarm();
    worker.terminate();
  };
}
