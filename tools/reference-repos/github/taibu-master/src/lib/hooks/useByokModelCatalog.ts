'use client';

import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { requestBrowserJson } from '@/lib/browser-api';
import { buildByokProviderOptions, type ByokCatalogModel } from '@/lib/ai/byok-catalog';
import { queryKeys } from '@/lib/query/keys';

async function loadByokCatalogModels() {
  const result = await requestBrowserJson<{ models?: ByokCatalogModel[] }>('/api/models?catalog=byok', {
    method: 'GET',
  });

  if (result.error) {
    throw new Error(result.error.message || 'BYOK 模型目录加载失败');
  }

  return result.data?.models ?? [];
}

export function useByokModelCatalog() {
  const query = useQuery({
    queryKey: queryKeys.byokCatalog(),
    queryFn: loadByokCatalogModels,
    staleTime: 10 * 60_000,
  });

  const providers = useMemo(
    () => buildByokProviderOptions(query.data ?? []),
    [query.data],
  );

  return {
    ...query,
    providers,
  };
}
