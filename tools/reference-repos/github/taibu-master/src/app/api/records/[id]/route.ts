/**
 * 单条记录 API 路由
 * GET: 获取单条记录
 * PUT: 更新记录
 * DELETE: 删除记录
 */

import { NextRequest } from 'next/server';
import { requireUserContext, jsonError, jsonOk, resolveRequestDbClient } from '@/lib/api-utils';
import { normalizeRecordInput } from '@/lib/records';

export async function GET(
    _request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const auth = await requireUserContext(_request);
        if ('error' in auth) return jsonError(auth.error.message, auth.error.status);
        const { user } = auth;
        const db = resolveRequestDbClient(auth);
        if (!db) return jsonError('获取记录失败', 500);

        const { id } = await params;

        const { data, error } = await db
            .from('ming_records')
            .select('*')
            .eq('id', id)
            .eq('user_id', user.id)
            .single();

        if (error) {
            if (error.code === 'PGRST116') {
                return jsonError('记录不存在', 404);
            }
            console.error('获取记录失败:', error);
            return jsonError('获取记录失败', 500);
        }

        return jsonOk(data as Record<string, unknown>);
    } catch (error) {
        console.error('获取记录失败:', error);
        return jsonError('获取记录失败', 500);
    }
}

export async function PUT(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) return jsonError(auth.error.message, auth.error.status);
        const { user } = auth;
        const db = resolveRequestDbClient(auth);
        if (!db) return jsonError('更新记录失败', 500);

        const { id } = await params;
        let body: Record<string, unknown>;
        try {
            body = await request.json() as Record<string, unknown>;
        } catch {
            return jsonError('请求体不是合法 JSON', 400);
        }

        // 处理置顶切换
        if (body.togglePin === true) {
            const { data, error } = await db.rpc('toggle_ming_record_pin', {
                p_record_id: id,
            });

            if (error) {
                console.error('切换置顶失败:', error);
                return jsonError('更新记录失败', 500);
            }

            const result = (Array.isArray(data) ? data[0] : data) as {
                status?: string;
                record?: Record<string, unknown> | null;
            } | null;
            if (result?.status === 'not_found') {
                return jsonError('记录不存在', 404);
            }
            if (result?.status !== 'ok' || !result.record) {
                console.error('切换置顶失败: invalid rpc result', data);
                return jsonError('更新记录失败', 500);
            }

            return jsonOk(result.record);
        }

        const existing = await db
            .from('ming_records')
            .select('id, related_chart_type, related_chart_id')
            .eq('id', id)
            .eq('user_id', user.id)
            .maybeSingle();

        if (existing.error) {
            console.error('获取记录失败:', existing.error);
            return jsonError('获取记录失败', 500);
        }
        if (!existing.data) {
            return jsonError('记录不存在', 404);
        }

        const normalized = normalizeRecordInput(body, 'update', existing.data as {
            related_chart_type: string | null;
            related_chart_id: string | null;
        });
        if ('error' in normalized) {
            return jsonError(normalized.error, 400);
        }

        // 常规更新
        const updateData: Record<string, unknown> = {
            ...normalized.data,
            updated_at: new Date().toISOString(),
        };

        const { data, error } = await db
            .from('ming_records')
            .update(updateData)
            .eq('id', id)
            .eq('user_id', user.id)
            .select()
            .single();

        if (error) {
            console.error('更新记录失败:', error);
            return jsonError('更新记录失败', 500);
        }

        return jsonOk(data as Record<string, unknown>);
    } catch (error) {
        console.error('更新记录失败:', error);
        return jsonError('更新记录失败', 500);
    }
}

export async function DELETE(
    _request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const auth = await requireUserContext(_request);
        if ('error' in auth) return jsonError(auth.error.message, auth.error.status);
        const { user } = auth;
        const db = resolveRequestDbClient(auth);
        if (!db) return jsonError('删除记录失败', 500);

        const { id } = await params;

        const { data, error } = await db
            .from('ming_records')
            .delete()
            .eq('id', id)
            .eq('user_id', user.id)
            .select('id');

        if (error) {
            console.error('删除记录失败:', error);
            return jsonError('删除记录失败', 500);
        }

        if (!Array.isArray(data) || data.length === 0) {
            return jsonError('记录不存在', 404);
        }

        return jsonOk({ success: true });
    } catch (error) {
        console.error('删除记录失败:', error);
        return jsonError('删除记录失败', 500);
    }
}
