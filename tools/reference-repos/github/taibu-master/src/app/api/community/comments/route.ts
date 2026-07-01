/**
 * 评论 API 路由
 * POST: 创建评论
 */

import { NextRequest } from 'next/server';
import { asCommunityLookupClient, loadSingleCommunityAuthorProfile } from '@/lib/community-server';
import { jsonError, jsonOk, requireUserContext } from '@/lib/api-utils';
import { withRetry } from '@/lib/retry';
import { hasNonEmptyStrings } from '@/lib/validation';

type CommunityCommentRow = {
    id: string;
    post_id: string;
    user_id: string;
    parent_id: string | null;
    content: string;
    upvote_count: number;
    downvote_count: number;
    is_deleted: boolean;
    created_at: string;
    updated_at: string;
};

export async function POST(request: NextRequest) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) {
            return jsonError(auth.error.message, auth.error.status);
        }
        const { user } = auth;
        const db = auth.db;

        const body = await request.json();

        if (!hasNonEmptyStrings(body, ['post_id', 'content'])) {
            return jsonError('帖子ID和内容不能为空', 400);
        }

        const authorProfile = await loadSingleCommunityAuthorProfile(asCommunityLookupClient(db), user.id);

        // 创建评论
        const commentResult = await withRetry(async () => {
            const response = await db
                .from('community_comments')
                .insert({
                    post_id: body.post_id,
                    user_id: user.id,
                    parent_id: body.parent_id || null,
                    content: body.content,
                })
                .select()
                .single();
            if (response.error) {
                throw response.error;
            }
            return response;
        });

        if (commentResult.error) {
            console.error('创建评论失败:', commentResult.error);
            return jsonError('创建评论失败', 500);
        }

        const data = commentResult.data as CommunityCommentRow | null;
        if (!data) {
            return jsonError('创建评论失败', 500);
        }

        return jsonOk({
            id: data.id,
            post_id: data.post_id,
            parent_id: data.parent_id,
            content: data.content,
            upvote_count: data.upvote_count,
            downvote_count: data.downvote_count,
            is_deleted: data.is_deleted,
            created_at: data.created_at,
            updated_at: data.updated_at,
            author_name: authorProfile.name,
            author_avatar_url: authorProfile.avatarUrl,
        });
    } catch (error) {
        console.error('创建评论失败:', error);
        return jsonError('创建评论失败', 500);
    }
}
