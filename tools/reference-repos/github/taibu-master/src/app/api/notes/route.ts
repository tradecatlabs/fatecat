/**
 * 小记 API 路由
 * GET: 获取小记列表
 * POST: 创建小记
 * DELETE: 删除小记
 */

import { NextRequest } from 'next/server';
import { requireUserContext, jsonError, jsonOk } from '@/lib/api-utils';

export async function GET(request: NextRequest) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) return jsonError(auth.error.message, auth.error.status);
        const { user } = auth;

        const { searchParams } = new URL(request.url);
        const date = searchParams.get('date');
        const startDate = searchParams.get('startDate');
        const endDate = searchParams.get('endDate');
        const page = Math.max(Number(searchParams.get('page') || 1), 1);
        const pageSize = Math.min(Math.max(Number(searchParams.get('pageSize') || 20), 1), 100);

        let query = auth.db
            .from('ming_notes')
            .select('*', { count: 'exact' })
            .eq('user_id', user.id)
            .order('created_at', { ascending: false });

        if (date) {
            query = query.eq('note_date', date);
        }
        if (startDate) {
            query = query.gte('note_date', startDate);
        }
        if (endDate) {
            query = query.lte('note_date', endDate);
        }

        const from = (page - 1) * pageSize;
        const to = from + pageSize - 1;
        query = query.range(from, to);

        const { data, error, count } = await query;

        if (error) {
            console.error('获取小记失败:', error);
            return jsonError('获取小记失败', 500);
        }

        return jsonOk({ notes: data, total: count || 0 });
    } catch (error) {
        console.error('获取小记失败:', error);
        return jsonError('获取小记失败', 500);
    }
}

export async function POST(request: NextRequest) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) return jsonError(auth.error.message, auth.error.status);
        const { user } = auth;

        const body = await request.json();

        if (!body.content) {
            return jsonError('内容不能为空', 400);
        }

        const { data, error } = await auth.db
            .from('ming_notes')
            .insert({
                user_id: user.id,
                note_date: body.note_date || new Date().toISOString().split('T')[0],
                content: body.content,
                mood: body.mood || null,
            })
            .select()
            .single();

        if (error) {
            console.error('创建小记失败:', error);
            return jsonError('创建小记失败', 500);
        }

        return jsonOk(data as Record<string, unknown>);
    } catch (error) {
        console.error('创建小记失败:', error);
        return jsonError('创建小记失败', 500);
    }
}

export async function DELETE(request: NextRequest) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) return jsonError(auth.error.message, auth.error.status);
        const { user } = auth;

        const { searchParams } = new URL(request.url);
        const id = searchParams.get('id');

        if (!id) {
            return jsonError('缺少 id 参数', 400);
        }

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
