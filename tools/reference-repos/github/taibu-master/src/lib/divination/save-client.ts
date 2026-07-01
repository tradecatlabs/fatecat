import { requestBrowserJson, type BrowserApiError } from '@/lib/browser-api';

export type SaveActionResult =
  | { ok: true; id: string | null }
  | { ok: false; error: BrowserApiError };

export async function saveDivinationAction(options: {
  endpoint: string;
  body: Record<string, unknown>;
  idKey: string;
  fallbackMessage?: string;
}): Promise<SaveActionResult> {
  const result = await requestBrowserJson<Record<string, unknown>>(options.endpoint, {
    method: 'POST',
    body: JSON.stringify({
      action: 'save',
      ...options.body,
    }),
  });

  if (result.error) {
    return {
      ok: false,
      error: result.error,
    };
  }

  const rawId = result.data?.[options.idKey];
  if (rawId != null && typeof rawId !== 'string') {
    return {
      ok: false,
      error: { message: options.fallbackMessage || '保存失败' },
    };
  }

  return {
    ok: true,
    id: typeof rawId === 'string' ? rawId : null,
  };
}
