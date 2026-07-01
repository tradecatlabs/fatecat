/**
 * 管理员帖子操作 API 路由
 * PUT: 管理员操作（置顶、精华、删除）
 */

import { NextRequest } from 'next/server';
import { jsonError, jsonOk, requireAdminContext, getSystemAdminClient } from '@/lib/api-utils';
import { missingFields } from '@/lib/validation';

export async function PUT(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const auth = await requireAdminContext(request);
        if ('error' in auth) {
            return jsonError(auth.error.message, auth.error.status);
        }

        const { id } = await params;
        const body = await request.json();
        const { action, value } = body;

        if (missingFields(body, ['action']).length > 0) {
            return jsonError('缺少参数', 400);
        }

        // 使用 Service Role Client 绕过 RLS
        const serviceClient = getSystemAdminClient();

        switch (action) {
            case 'pin': {
                const { error } = await serviceClient
                    .from('community_posts')
                    .update({ is_pinned: value, updated_at: new Date().toISOString() })
                    .eq('id', id);
                if (error) throw error;
                break;
            }
            case 'feature': {
                const { error } = await serviceClient
                    .from('community_posts')
                    .update({ is_featured: value, updated_at: new Date().toISOString() })
                    .eq('id', id);
                if (error) throw error;
                break;
            }
            case 'delete': {
                const { error } = await serviceClient
                    .from('community_posts')
                    .update({ is_deleted: true, updated_at: new Date().toISOString() })
                    .eq('id', id);
                if (error) throw error;
                break;
            }
            default:
                return jsonError('无效操作', 400);
        }

        return jsonOk({ success: true });
    } catch (error) {
        console.error('管理员操作失败:', error);
        return jsonError('操作失败', 500);
    }
}
