import { NextRequest } from 'next/server';
import { getSystemAdminClient, jsonError, jsonOk, requireAdminContext } from '@/lib/api-utils';
import { parseAnnouncementInput, serializeAnnouncement, type AnnouncementRow } from '@/lib/announcement';

type RouteContext = {
    params: Promise<{ id: string }>;
};

async function getAnnouncementRow(id: string) {
    const supabase = getSystemAdminClient();
    const { data, error } = await supabase
        .from('announcements')
        .select('*')
        .eq('id', id)
        .maybeSingle();

    return {
        row: data as AnnouncementRow | null,
        error,
    };
}

export async function GET(request: NextRequest, context: RouteContext) {
    const auth = await requireAdminContext(request);
    if ('error' in auth) {
        return jsonError(auth.error.message, auth.error.status);
    }

    const { id } = await context.params;
    const { row, error } = await getAnnouncementRow(id);

    if (error) {
        console.error('[announcements][admin][GET] load failed:', error);
        return jsonError('获取公告失败', 500);
    }

    if (!row) {
        return jsonError('公告不存在', 404);
    }

    return jsonOk({ announcement: serializeAnnouncement(row) });
}

export async function PATCH(request: NextRequest, context: RouteContext) {
    const auth = await requireAdminContext(request);
    if ('error' in auth) {
        return jsonError(auth.error.message, auth.error.status);
    }

    const { id } = await context.params;
    const { row: existing, error: loadError } = await getAnnouncementRow(id);
    if (loadError) {
        console.error('[announcements][admin][PATCH] load failed:', loadError);
        return jsonError('获取公告失败', 500);
    }
    if (!existing) {
        return jsonError('公告不存在', 404);
    }

    let body: unknown;
    try {
        body = await request.json();
    } catch {
        return jsonError('请求体不是合法 JSON', 400);
    }

    const parsed = parseAnnouncementInput(body, { partial: true });
    if (parsed.error || !parsed.value) {
        return jsonError(parsed.error || '公告参数无效', 400);
    }

    if (!parsed.value.content) {
        return jsonError('公告内容不能为空', 400);
    }

    const supabase = getSystemAdminClient();
    const { data, error } = await supabase
        .from('announcements')
        .update({
            content: parsed.value.content,
        })
        .eq('id', id)
        .select('*')
        .single();

    if (error || !data) {
        console.error('[announcements][admin][PATCH] update failed:', error);
        return jsonError('更新公告失败', 500);
    }

    return jsonOk({ announcement: serializeAnnouncement(data as AnnouncementRow) });
}

export async function DELETE(request: NextRequest, context: RouteContext) {
    const auth = await requireAdminContext(request);
    if ('error' in auth) {
        return jsonError(auth.error.message, auth.error.status);
    }

    const { id } = await context.params;
    const { row: existing, error: loadError } = await getAnnouncementRow(id);
    if (loadError) {
        console.error('[announcements][admin][DELETE] load failed:', loadError);
        return jsonError('获取公告失败', 500);
    }
    if (!existing) {
        return jsonError('公告不存在', 404);
    }
    const supabase = getSystemAdminClient();
    const { error } = await supabase
        .from('announcements')
        .delete()
        .eq('id', id);

    if (error) {
        console.error('[announcements][admin][DELETE] delete failed:', error);
        return jsonError('删除公告失败', 500);
    }

    return jsonOk({ success: true });
}
