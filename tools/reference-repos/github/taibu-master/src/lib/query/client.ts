import { QueryClient } from '@tanstack/react-query';

let browserQueryClient: QueryClient | null = null;

export function createAppQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,
        gcTime: 5 * 60_000,
        retry: 1,
        refetchOnWindowFocus: true,
        refetchOnReconnect: true,
      },
      mutations: {
        retry: 0,
      },
    },
  });
}

export function registerBrowserQueryClient(queryClient: QueryClient) {
  browserQueryClient = queryClient;
}

export function getBrowserQueryClient() {
  return browserQueryClient;
}
