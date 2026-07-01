import { type NextRequest } from 'next/server';
import { getSystemAdminClient, jsonError, jsonOk, requireAdminContext } from '@/lib/api-utils';

export async function DELETE(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    const auth = await requireAdminContext(request);
    if ('error' in auth) return jsonError(auth.error.message, auth.error.status);

    const { id } = await params;
    const serviceClient = getSystemAdminClient();
    const { error } = await serviceClient
        .from('community_comments')
        .update({ is_deleted: true, updated_at: new Date().toISOString() })
        .eq('id', id);

    if (error) {
        console.error('管理员删除评论失败:', error);
        return jsonError('操作失败', 500);
    }

    return jsonOk({ success: true });
}
