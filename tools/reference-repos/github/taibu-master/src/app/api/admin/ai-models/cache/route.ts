/**
 * AI 模型缓存管理 API
 *
 * POST: 清除配置缓存
 */
import { NextRequest } from 'next/server';
import { requireAdminUser, jsonError, jsonOk } from '@/lib/api-utils';
import { clearModelCache } from '@/lib/server/ai-config';

export async function POST(request: NextRequest) {
    // 验证管理员权限
    const authResult = await requireAdminUser(request);
    if ('error' in authResult) {
        return jsonError(authResult.error.message, authResult.error.status);
    }

    clearModelCache();

    return jsonOk({ success: true, message: '配置缓存已清除' });
}
