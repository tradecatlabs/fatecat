/**
 * Cron API - 处理到期提醒
 * 
 * 由 GitHub Actions 定期调用（每小时一次）
 * 处理 scheduled_reminders 表中到期的提醒
 */
import { NextRequest } from 'next/server';
import { processScheduledReminders, scheduleAllUsersReminders } from '@/lib/reminders';
import { jsonError, jsonOk } from '@/lib/api-utils';
import { pruneExpiredNotifications } from '@/lib/notification-server';

/**
 * 验证 Cron 请求
 * 支持 CRON_SECRET 环境变量验证
 */
function validateCronRequest(request: NextRequest): boolean {
    const cronSecret = process.env.CRON_SECRET;

    // 如果没有配置 CRON_SECRET，仅在开发环境允许
    if (!cronSecret) {
        return process.env.NODE_ENV === 'development';
    }

    // 验证 Authorization header
    const authHeader = request.headers.get('authorization');
    if (authHeader?.startsWith('Bearer ')) {
        const token = authHeader.slice(7);
        return token === cronSecret;
    }

    // 验证 X-Cron-Secret header（备选）
    const cronHeader = request.headers.get('x-cron-secret');
    return cronHeader === cronSecret;
}

// GET - 处理到期提醒
export async function GET(request: NextRequest) {
    // 验证请求来源
    if (!validateCronRequest(request)) {
        return jsonError('Unauthorized', 401);
    }

    try {
        // 1. 处理到期的提醒
        const processed = await processScheduledReminders();

        // 2. 为所有启用提醒的用户调度新提醒
        const scheduled = await scheduleAllUsersReminders();
        const prunedNotifications = await pruneExpiredNotifications();

        console.log(`[cron/process-reminders] 处理了 ${processed} 条提醒，调度了 ${scheduled} 条新提醒，清理了 ${prunedNotifications} 条过期通知`);

        return jsonOk({
            success: true,
            processed,
            scheduled,
            prunedNotifications,
        });
    } catch (error) {
        console.error('[cron/process-reminders] 处理失败:', error);
        return jsonError('处理提醒失败', 500);
    }
}

// 确保每次请求都执行
export const dynamic = 'force-dynamic';
