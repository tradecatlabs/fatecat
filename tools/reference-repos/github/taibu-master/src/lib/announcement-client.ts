import { requestBrowserJson } from '@/lib/browser-api';
import type { Announcement } from '@/lib/announcement';

export async function loadLatestAnnouncement() {
  const result = await requestBrowserJson<{ announcement?: Announcement | null }>('/api/announcements?latest=1', {
    method: 'GET',
  });

  if (result.error) {
    throw new Error(result.error.message ?? '获取公告失败');
  }

  return result.data?.announcement ?? null;
}
