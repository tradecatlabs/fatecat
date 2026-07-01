/**
 * 单个评论 API 路由
 * PUT: 更新评论
 * DELETE: 删除评论（软删除）
 */

import { NextRequest } from 'next/server';
import { jsonError, jsonOk, requireUserContext } from '@/lib/api-utils';
import { withRetry } from '@/lib/retry';
import { hasNonEmptyStrings } from '@/lib/validation';

export async function GET(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) {
            return jsonError(auth.error.message, auth.error.status);
        }
        const { user } = auth;
        const db = auth.db;

        const { id } = await params;
        const { data, error } = await db
            .from('community_comments')
            .select('id, user_id')
            .eq('id', id)
            .eq('is_deleted', false)
            .maybeSingle();

        if (error) {
            console.error('获取评论失败:', error);
            return jsonError('获取评论失败', 500);
        }
        if (!data) {
            return jsonError('评论不存在', 404);
        }

        const isAuthor = data.user_id === user.id;
        return jsonOk({
            viewer: {
                isAuthenticated: true,
                isAuthor,
            },
        });
    } catch (error) {
        console.error('获取评论失败:', error);
        return jsonError('获取评论失败', 500);
    }
}

export async function PUT(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) {
            return jsonError(auth.error.message, auth.error.status);
        }
        const { user } = auth;
        const db = auth.db;

        const { id } = await params;
        const body = await request.json();

        if (!hasNonEmptyStrings(body, ['content'])) {
            return jsonError('内容不能为空', 400);
        }

        const updateResult = await withRetry(async () => {
            const response = await db
                .from('community_comments')
                .update({
                    content: body.content,
                    updated_at: new Date().toISOString(),
                })
                .eq('id', id)
                .eq('user_id', user.id)
                .eq('is_deleted', false)
                .select()
                .maybeSingle();
            if (response.error) {
                throw response.error;
            }
            return response;
        });

        if (updateResult.error) {
            console.error('更新评论失败:', updateResult.error);
            return jsonError('更新评论失败', 500);
        }

        const data = updateResult.data as Record<string, unknown> | null;
        if (!data) {
            return jsonError('无权限编辑此评论', 403);
        }
        const safeComment = { ...(data || {}) } as Record<string, unknown>;
        delete (safeComment as { user_id?: unknown }).user_id;
        return jsonOk(safeComment);
    } catch (error) {
        console.error('更新评论失败:', error);
        return jsonError('更新评论失败', 500);
    }
}

export async function DELETE(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) {
            return jsonError(auth.error.message, auth.error.status);
        }
        const { user } = auth;
        const db = auth.db;

        const { id } = await params;

        const deleteResult = await withRetry(async () => {
            const response = await db
                .from('community_comments')
                .update({ is_deleted: true, updated_at: new Date().toISOString() })
                .eq('id', id)
                .eq('user_id', user.id)
                .eq('is_deleted', false)
                .select('id')
                .maybeSingle();
            if (response.error) {
                throw response.error;
            }
            return response;
        });

        if (deleteResult.error) {
            console.error('删除评论失败:', deleteResult.error);
            return jsonError('删除评论失败', 500);
        }

        if (!deleteResult.data) {
            return jsonError('无权限删除此评论', 403);
        }

        return jsonOk({ success: true });
    } catch (error) {
        console.error('删除评论失败:', error);
        return jsonError('删除评论失败', 500);
    }
}
