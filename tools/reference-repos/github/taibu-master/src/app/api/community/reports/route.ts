/**
 * 举报 API 路由
 * GET: 管理员获取举报列表
 * POST: 提交举报
 * PUT: 管理员处理举报
 */

import { NextRequest } from 'next/server';
import { TargetType, ReportReason, ReportStatus } from '@/lib/community';
import { jsonError, jsonOk, requireAdminContext, requireUserContext, resolveRequestDbClient } from '@/lib/api-utils';
import { parsePagination } from '@/lib/pagination';
import { missingFields } from '@/lib/validation';

export async function GET(request: NextRequest) {
    try {
        const auth = await requireAdminContext(request);
        if ('error' in auth) {
            return jsonError(auth.error.message, auth.error.status);
        }
        const db = resolveRequestDbClient(auth);
        if (!db) {
            return jsonError('获取举报列表失败', 500);
        }

        const { searchParams } = new URL(request.url);
        const status = searchParams.get('status') as ReportStatus | null;
        const { from, to } = parsePagination(searchParams, { defaultPageSize: 20 });

        // 使用 Service Role Client 获取所有举报
        let query = db
            .from('community_reports')
            .select('*', { count: 'exact' })
            .order('created_at', { ascending: false });

        if (status) {
            query = query.eq('status', status);
        }

        query = query.range(from, to);

        const { data, error, count } = await query;

        if (error) {
            console.error('获取举报列表失败:', error);
            return jsonError('获取举报列表失败', 500);
        }

        return jsonOk({
            reports: data,
            total: count || 0,
        });
    } catch (error) {
        console.error('获取举报列表失败:', error);
        return jsonError('获取举报列表失败', 500);
    }
}

export async function POST(request: NextRequest) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) {
            return jsonError(auth.error.message, auth.error.status);
        }
        const db = resolveRequestDbClient(auth);
        if (!db) {
            return jsonError('提交举报失败', 500);
        }

        const body = await request.json();
        const { targetType, targetId, reason, description } = body as {
            targetType: TargetType;
            targetId: string;
            reason: ReportReason;
            description?: string;
        };

        if (missingFields(body, ['targetType', 'targetId', 'reason']).length > 0) {
            return jsonError('缺少参数', 400);
        }

        const { data, error } = await db.rpc('submit_community_report_and_notify', {
            p_target_type: targetType,
            p_target_id: targetId,
            p_reason: reason,
            p_description: description || null,
        });

        if (error) {
            console.error('提交举报失败:', error);
            return jsonError('提交举报失败', 500);
        }

        const result = (Array.isArray(data) ? data[0] : data) as { status?: string; report?: unknown } | null;
        if (result?.status !== 'ok' || !result.report) {
            console.error('提交举报失败: unexpected rpc response', result);
            return jsonError('提交举报失败', 500);
        }

        return jsonOk(result.report);
    } catch (error) {
        console.error('提交举报失败:', error);
        return jsonError('提交举报失败', 500);
    }
}

export async function PUT(request: NextRequest) {
    try {
        const auth = await requireAdminContext(request);
        if ('error' in auth) {
            return jsonError(auth.error.message, auth.error.status);
        }
        const { user } = auth;
        const db = resolveRequestDbClient(auth);
        if (!db) {
            return jsonError('处理举报失败', 500);
        }

        const body = await request.json();
        const { reportId, status, notes } = body as {
            reportId: string;
            status: 'resolved' | 'dismissed';
            notes?: string;
        };

        if (missingFields(body, ['reportId', 'status']).length > 0) {
            return jsonError('缺少参数', 400);
        }

        // 使用 Service Role Client 更新举报
        const { error } = await db
            .from('community_reports')
            .update({
                status,
                reviewed_by: user.id,
                reviewed_at: new Date().toISOString(),
                review_notes: notes || null,
            })
            .eq('id', reportId);

        if (error) {
            console.error('处理举报失败:', error);
            return jsonError('处理举报失败', 500);
        }

        return jsonOk({ success: true });
    } catch (error) {
        console.error('处理举报失败:', error);
        return jsonError('处理举报失败', 500);
    }
}
