'use client';

import { useQuery } from '@tanstack/react-query';
import { loadLatestAnnouncement } from '@/lib/announcement-client';
import { queryKeys } from '@/lib/query/keys';

export function useLatestAnnouncement(options?: { enabled?: boolean }) {
  const enabled = options?.enabled ?? true;

  return useQuery({
    queryKey: queryKeys.latestAnnouncement(),
    queryFn: () => loadLatestAnnouncement(),
    enabled,
    staleTime: 60_000,
  });
}
