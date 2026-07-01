'use client';

import { useQuery } from '@tanstack/react-query';
import { getUnreadCount } from '@/lib/notification';
import { useAppBootstrap } from '@/lib/hooks/useAppBootstrap';
import { queryKeys } from '@/lib/query/keys';

type UseNotificationUnreadCountOptions = {
  enabled?: boolean;
};

export function useNotificationUnreadCount(
  userId: string | null,
  options: UseNotificationUnreadCountOptions = {},
) {
  const enabled = options.enabled ?? true;
  const bootstrap = useAppBootstrap({ enabled });
  const bootstrapUnreadCount = userId && bootstrap.data.unreadCountLoaded
    ? bootstrap.data.unreadCount
    : null;

  const query = useQuery({
    queryKey: queryKeys.notificationsUnread(userId),
    queryFn: () => getUnreadCount(),
    enabled: enabled && !!userId,
    staleTime: 5_000,
    refetchOnWindowFocus: true,
    refetchInterval: userId ? 30_000 : false,
    refetchIntervalInBackground: false,
  });

  if (!enabled || !userId) {
    return null;
  }

  if (typeof query.data === 'number') {
    return query.data;
  }

  if (bootstrapUnreadCount != null) {
    return bootstrapUnreadCount;
  }

  return null;
}
