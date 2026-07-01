import { getSystemAdminClient } from '@/lib/api-utils';

const NOTIFICATION_RETENTION_DAYS = 3;
const NOTIFICATION_RETENTION_MS = NOTIFICATION_RETENTION_DAYS * 24 * 60 * 60 * 1000;

export function getNotificationRetentionCutoffIso(now: Date = new Date()) {
    return new Date(now.getTime() - NOTIFICATION_RETENTION_MS).toISOString();
}

export async function pruneExpiredNotifications(options: { userId?: string } = {}) {
    const serviceClient = getSystemAdminClient();
    const cutoffIso = getNotificationRetentionCutoffIso();

    let deleteQuery = serviceClient
        .from('notifications')
        .delete()
        .lt('created_at', cutoffIso);

    if (options.userId) {
        deleteQuery = deleteQuery.eq('user_id', options.userId);
    }

    const { data, error } = await deleteQuery.select('id');
    if (error) {
        console.error('清理过期通知失败:', error);
        return 0;
    }

    return Array.isArray(data) ? data.length : 0;
}
