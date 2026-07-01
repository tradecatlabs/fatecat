import { NextRequest } from 'next/server';
import { getSystemAdminClient, jsonError, jsonOk, requireAdminContext } from '@/lib/api-utils';
import { parseAnnouncementInput, serializeAnnouncement, type AnnouncementRow } from '@/lib/announcement';

export async function GET(request: NextRequest) {
    const auth = await requireAdminContext(request);
    if ('error' in auth) {
        return jsonError(auth.error.message, auth.error.status);
    }

    const supabase = getSystemAdminClient();
    const { data, error } = await supabase
        .from('announcements')
        .select('*')
        .order('published_at', { ascending: false });

    if (error) {
        console.error('[announcements][admin][GET] query failed:', error);
        return jsonError('获取公告列表失败', 500);
    }

    return jsonOk({
        announcements: (data || []).map((row: AnnouncementRow) => serializeAnnouncement(row)),
    });
}

export async function POST(request: NextRequest) {
    const auth = await requireAdminContext(request);
    if ('error' in auth) {
        return jsonError(auth.error.message, auth.error.status);
    }

    let body: unknown;
    try {
        body = await request.json();
    } catch {
        return jsonError('请求体不是合法 JSON', 400);
    }

    const parsed = parseAnnouncementInput(body);
    if (parsed.error || !parsed.value) {
        return jsonError(parsed.error || '公告参数无效', 400);
    }

    const payload = {
        content: parsed.value.content!,
        published_at: new Date().toISOString(),
    };

    const supabase = getSystemAdminClient();
    const { data, error } = await supabase
        .from('announcements')
        .insert(payload)
        .select('*')
        .single();

    if (error) {
        console.error('[announcements][admin][POST] insert failed:', error);
        return jsonError('发布公告失败', 500);
    }

    return jsonOk({ announcement: serializeAnnouncement(data as AnnouncementRow) });
}
