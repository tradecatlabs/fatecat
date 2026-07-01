import { NextRequest } from 'next/server';
import { getSystemAdminClient, jsonError, jsonOk } from '@/lib/api-utils';
import { serializeAnnouncement, type AnnouncementRow } from '@/lib/announcement';

export async function GET(request: NextRequest) {
    const supabase = getSystemAdminClient();
    const countOnly = request.nextUrl.searchParams.get('count') === '1';
    const latestOnly = request.nextUrl.searchParams.get('latest') === '1';
    const limit = Math.min(Math.max(Number(request.nextUrl.searchParams.get('limit') || 20), 1), 100);
    const offset = Math.max(Number(request.nextUrl.searchParams.get('offset') || 0), 0);

    if (countOnly) {
        const { count, error } = await supabase
            .from('announcements')
            .select('id', { count: 'exact', head: true });

        if (error) {
            console.error('[announcements][GET][count] query failed:', error);
            return jsonError('获取公告失败', 500);
        }

        return jsonOk({ count: count ?? 0 });
    }

    const query = supabase
        .from('announcements')
        .select('*')
        .order('published_at', { ascending: false });

    if (latestOnly) {
        const { data, error } = await query.limit(1).maybeSingle();
        if (error) {
            console.error('[announcements][GET][latest] query failed:', error);
            return jsonError('获取公告失败', 500);
        }

        return jsonOk({
            announcement: data ? serializeAnnouncement(data as AnnouncementRow) : null,
        });
    }

    const { data, error } = await query.range(offset, offset + limit);
    if (error) {
        console.error('[announcements][GET][list] query failed:', error);
        return jsonError('获取公告失败', 500);
    }

    const rows = (data || []) as AnnouncementRow[];
    const announcements = rows.slice(0, limit).map((row) => serializeAnnouncement(row));
    const hasMore = rows.length > limit;

    return jsonOk({
        announcements,
        pagination: {
            hasMore,
            nextOffset: hasMore ? offset + announcements.length : null,
        },
    });
}
