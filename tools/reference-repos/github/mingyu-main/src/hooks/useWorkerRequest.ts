import { useEffect, useRef, useState } from 'react';

const DEFAULT_TIMEOUT_MS = 30000;

export interface WorkerSafetyOptions {
  onError: (message: string) => void;
  timeoutMs?: number;
}

/**
 * 给已创建的 Worker 附加错误处理:
 *   - onerror 触发时调用 onError
 *   - onmessageerror 触发时调用 onError
 *   - timeoutMs 超时未响应时调用 onError 并 terminate
 *
 * 返回 disarm 函数,在收到成功响应或组件 cleanup 时调用,
 * 解除安全网(防止延迟的错误回调污染后续状态)。
 */
export function attachWorkerSafety(worker: Worker, options: WorkerSafetyOptions): () => void {
  const { onError, timeoutMs = DEFAULT_TIMEOUT_MS } = options;
  let disarmed = false;

  const fireError = (message: string) => {
    if (disarmed) return;
    disarmed = true;
    window.clearTimeout(timer);
    try {
      worker.terminate();
    } catch {
      /* 已 terminate 时静默 */
    }
    onError(message);
  };

  const timer = window.setTimeout(() => {
    fireError('请求超时,请稍后重试。');
  }, timeoutMs);

  worker.addEventListener('error', (event) => {
    fireError(event.message || 'Worker 执行出错。');
  });

  worker.addEventListener('messageerror', () => {
    fireError('Worker 消息解析失败。');
  });

  return () => {
    disarmed = true;
    window.clearTimeout(timer);
  };
}

export interface UseWorkerRequestOptions<TReq extends object> {
  factory: () => Worker;
  request: TReq | null;
  timeoutMs?: number;
}

export interface UseWorkerRequestResult<TRes> {
  data: TRes | null;
  loading: boolean;
  error: string | null;
}

type WorkerEnvelope<TRes> =
  ({ id: string; ok: true } & TRes) | { id: string; ok: false; error?: string };

/**
 * 通用 Worker 请求 hook:
 *   - request 为 null 时不发送请求
 *   - request 引用变化时重新发送(调用方需用 useMemo 稳定 request)
 *   - factory 引用通过 ref 保存,避免引用变化触发重发
 *   - 内置 onerror、onmessageerror、timeoutMs(默认 30s)兜底
 *   - 收到 id 不匹配的响应自动丢弃
 *
 * Worker 协议约定:
 *   请求: { id: string, ...request }
 *   响应: { id: string, ok: true, ...payload } | { id: string, ok: false, error?: string }
 */
export function useWorkerRequest<TReq extends object, TRes>(
  options: UseWorkerRequestOptions<TReq>,
): UseWorkerRequestResult<TRes> {
  const { factory, request, timeoutMs = DEFAULT_TIMEOUT_MS } = options;
  const factoryRef = useRef(factory);
  const idRef = useRef(0);

  const [data, setData] = useState<TRes | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    factoryRef.current = factory;

    if (!request) {
      setData(null);
      setLoading(false);
      setError(null);
      return;
    }

    idRef.current += 1;
    const requestId = `wreq-${idRef.current}`;
    const worker = factoryRef.current();
    let settled = false;

    const cleanup = () => {
      settled = true;
      window.clearTimeout(timer);
      try {
        worker.terminate();
      } catch {
        /* 已 terminate 时静默 */
      }
    };

    const finishWithError = (message: string) => {
      if (settled) return;
      cleanup();
      setData(null);
      setLoading(false);
      setError(message);
    };

    const finishWithSuccess = (payload: TRes) => {
      if (settled) return;
      cleanup();
      setData(payload);
      setLoading(false);
      setError(null);
    };

    const timer = window.setTimeout(() => {
      finishWithError('请求超时,请稍后重试。');
    }, timeoutMs);

    setData(null);
    setLoading(true);
    setError(null);

    worker.onmessage = (event: MessageEvent<WorkerEnvelope<TRes>>) => {
      if (settled || event.data.id !== requestId) {
        return;
      }
      if (event.data.ok) {
        finishWithSuccess(event.data as unknown as TRes);
      } else {
        finishWithError(event.data.error || '请求失败,请稍后重试。');
      }
    };

    worker.onerror = (event) => {
      finishWithError(event.message || 'Worker 执行出错。');
    };

    worker.onmessageerror = () => {
      finishWithError('Worker 消息解析失败。');
    };

    worker.postMessage({ id: requestId, ...request });

    return cleanup;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [request, timeoutMs]);

  return { data, loading, error };
}
