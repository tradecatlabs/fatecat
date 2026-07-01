import { type NextRequest } from 'next/server';
import { jsonError, jsonOk, requireUserContext } from '@/lib/api-utils';

export async function PUT(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) return jsonError(auth.error.message, auth.error.status);
        const { user } = auth;

        const { id } = await params;
        const body = await request.json() as {
            note_date?: string;
            content?: string;
            mood?: string | null;
        };

        const { data, error } = await auth.db
            .from('ming_notes')
            .update({
                ...(body.note_date !== undefined ? { note_date: body.note_date } : {}),
                ...(body.content !== undefined ? { content: body.content } : {}),
                ...(body.mood !== undefined ? { mood: body.mood } : {}),
                updated_at: new Date().toISOString(),
            })
            .eq('id', id)
            .eq('user_id', user.id)
            .select()
            .maybeSingle();

        if (error) {
            console.error('更新小记失败:', error);
            return jsonError('更新小记失败', 500);
        }
        if (!data) {
            return jsonError('小记不存在', 404);
        }

        return jsonOk(data as Record<string, unknown>);
    } catch (error) {
        console.error('更新小记失败:', error);
        return jsonError('更新小记失败', 500);
    }
}

export async function DELETE(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) return jsonError(auth.error.message, auth.error.status);
        const { user } = auth;

        const { id } = await params;
        const { error } = await auth.db
            .from('ming_notes')
            .delete()
            .eq('id', id)
            .eq('user_id', user.id);

        if (error) {
            console.error('删除小记失败:', error);
            return jsonError('删除小记失败', 500);
        }

        return jsonOk({ success: true });
    } catch (error) {
        console.error('删除小记失败:', error);
        return jsonError('删除小记失败', 500);
    }
}
