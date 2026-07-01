import { type NextRequest } from 'next/server';
import { jsonError, jsonOk, requireUserContext } from '@/lib/api-utils';
import {
    buildHistoryRestorePayload,
    buildHistorySummary,
    HISTORY_CONFIG,
    isHistoryType,
} from '@/lib/history/registry';

type HistoryRow = Record<string, unknown>;

function toHistoryRow(value: unknown): HistoryRow | null {
    if (!value || typeof value !== 'object' || Array.isArray(value) || 'error' in value) {
        return null;
    }
    return value as HistoryRow;
}

async function loadHistoryItems(
    auth: Exclude<Awaited<ReturnType<typeof requireUserContext>>, { error: unknown }>,
    type: keyof typeof HISTORY_CONFIG,
    limit: number,
    offset: number,
) {
    const config = HISTORY_CONFIG[type];
    const { data, error } = await auth.db
        .from(config.tableName)
        .select(config.summarySelect)
        .eq('user_id', auth.user.id)
        .order('created_at', { ascending: false })
        .range(offset, offset + limit);

    if (error) {
        return { items: null, pagination: null, error };
    }

    const rows = (data || []).flatMap((item) => {
        const row = toHistoryRow(item);
        return row ? [row] : [];
    });
    const hasMore = rows.length > limit;
    const pageRows = hasMore ? rows.slice(0, limit) : rows;
    const items = await Promise.all(pageRows.map((row) => buildHistorySummary(type, row)));

    return {
        items,
        pagination: {
            hasMore,
            nextOffset: hasMore ? offset + limit : null,
        },
        error: null,
    };
}

async function loadHistoryRestoreItem(
    auth: Exclude<Awaited<ReturnType<typeof requireUserContext>>, { error: unknown }>,
    type: keyof typeof HISTORY_CONFIG,
    id: string,
    timezone: string,
) {
    const config = HISTORY_CONFIG[type];
    const { data, error } = await auth.db
        .from(config.tableName)
        .select('*')
        .eq('id', id)
        .eq('user_id', auth.user.id)
        .maybeSingle();

    if (error) {
        return { item: null, error };
    }

    const row = toHistoryRow(data);
    if (!row) {
        return { item: null, error: null };
    }

    const item = await buildHistoryRestorePayload(type, row, timezone);
    return { item, error: null };
}

async function loadHistoryDeleteContext(
    auth: Exclude<Awaited<ReturnType<typeof requireUserContext>>, { error: unknown }>,
    type: keyof typeof HISTORY_CONFIG,
    id: string,
) {
    const config = HISTORY_CONFIG[type];
    const { data, error } = await auth.db
        .from(config.tableName)
        .select('*')
        .eq('id', id)
        .eq('user_id', auth.user.id)
        .maybeSingle();

    if (error) {
        return { conversationId: null, error };
    }

    const row = toHistoryRow(data);
    const conversationId = typeof row?.conversation_id === 'string'
        ? row.conversation_id
        : null;

    return { conversationId, error: null };
}

export async function GET(request: NextRequest) {
    const auth = await requireUserContext(request);
    if ('error' in auth) return jsonError(auth.error.message, auth.error.status);

    const { searchParams } = new URL(request.url);
    const type = searchParams.get('type');
    const id = searchParams.get('id');
    const timezone = searchParams.get('timezone') || 'Asia/Shanghai';
    const limit = Math.min(
        Math.max(Number.parseInt(searchParams.get('limit') || '100', 10) || 100, 1),
        100,
    );
    const offset = Math.max(Number.parseInt(searchParams.get('offset') || '0', 10) || 0, 0);

    if (!isHistoryType(type)) {
        return jsonError('无效的历史类型', 400);
    }

    if (id) {
        const { item, error } = await loadHistoryRestoreItem(auth, type, id, timezone);
        if (error) {
            console.error('[history-summaries] failed to restore history:', error);
            return jsonError('加载历史记录失败', 500);
        }
        if (!item) {
            return jsonError('未找到历史记录', 404);
        }
        return jsonOk({ item });
    }

    const { items, pagination, error } = await loadHistoryItems(auth, type, limit, offset);
    if (error) {
        console.error('[history-summaries] failed to load history:', error);
        return jsonError('加载历史记录失败', 500);
    }

    return jsonOk({ items: items || [], pagination });
}

export async function DELETE(request: NextRequest) {
    const auth = await requireUserContext(request);
    if ('error' in auth) return jsonError(auth.error.message, auth.error.status);

    const { searchParams } = new URL(request.url);
    const type = searchParams.get('type');
    const id = searchParams.get('id');

    if (!isHistoryType(type) || !id) {
        return jsonError('缺少有效的历史记录类型或 ID', 400);
    }

    const { conversationId, error: contextError } = await loadHistoryDeleteContext(auth, type, id);
    if (contextError) {
        console.error('[history-summaries] failed to load delete context:', contextError);
        return jsonError('删除历史记录失败', 500);
    }

    const { data, error } = await auth.db.rpc('delete_history_item_and_conversation', {
        p_history_type: type,
        p_history_id: id,
    });

    if (error) {
        console.error('[history-summaries] failed to delete history transaction:', error);
        return jsonError('删除历史记录失败', 500);
    }

    if (data !== true) {
        return jsonError('未找到历史记录', 404);
    }

    return jsonOk({
        success: true,
        type,
        id,
        conversationId,
    });
}
