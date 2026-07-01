/**
 * 单个帖子 API 路由
 * GET: 获取帖子详情
 * PUT: 更新帖子
 * DELETE: 删除帖子（软删除）
 */

import { NextRequest } from 'next/server';
import { CommunityComment, normalizePostInput } from '@/lib/community';
import { asCommunityLookupClient, loadCommunityAuthorProfileMap, toPublicPost, type CommunityPostRow } from '@/lib/community-server';
import { getAuthContext, jsonError, jsonOk, requireUserContext, getSystemAdminClient } from '@/lib/api-utils';
import { withRetry } from '@/lib/retry';

type CommunityCommentRow = Omit<CommunityComment, 'author_name' | 'author_avatar_url' | 'replies'> & {
    user_id: string;
    replies?: CommunityCommentRow[];
};

export async function GET(
    _request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const auth = await getAuthContext(_request);
        if (auth.authError) {
            return jsonError(auth.authError.message, auth.authError.status);
        }
        const { user } = auth;
        const db = auth.db;
        const { id } = await params;

        // 获取帖子
        const { data: post, error: postError } = await db
            .from('community_posts')
            .select('*')
            .eq('id', id)
            .eq('is_deleted', false)
            .single();

        if (postError) {
            if (postError.code === 'PGRST116') {
                return jsonError('帖子不存在', 404);
            }
            console.error('获取帖子失败:', postError);
            return jsonError('获取帖子失败', 500);
        }

        // 使用 Service Role Client 增加浏览量（绕过 RLS）
        const serviceClient = getSystemAdminClient();
        await withRetry(async () => {
            const { error } = await serviceClient
                .rpc('increment_community_post_view_count', { post_id: id });
            if (error) {
                throw error;
            }
        });

        // 获取评论 - 使用 serviceClient 和重试逻辑
        const commentsResult = await withRetry(async () => {
            const response = await serviceClient
                .from('community_comments')
                .select('*')
                .eq('post_id', id)
                .eq('is_deleted', false)
                .order('created_at', { ascending: true });
            if (response.error) {
                throw response.error;
            }
            return response;
        });
        const commentsData = commentsResult.data;
        const commentsError = commentsResult.error;

        if (commentsError) {
            console.error('获取评论失败:', commentsError);
        }

        const authorMap = await loadCommunityAuthorProfileMap(asCommunityLookupClient(serviceClient), [
            post.user_id,
            ...((commentsData || []).map((comment: CommunityCommentRow) => comment.user_id)),
        ]);

        type CommentWithReplies = CommunityCommentRow & { replies: CommentWithReplies[] };
        const comments: CommentWithReplies[] = (commentsData || []).map((comment: CommunityCommentRow) => ({
            ...comment,
            replies: [],
        }));

        const commentMap = new Map<string, CommentWithReplies>();
        const rootComments: CommentWithReplies[] = [];

        comments.forEach(comment => {
            commentMap.set(comment.id, comment);
        });

        comments.forEach(comment => {
            if (comment.parent_id) {
                const parent = commentMap.get(comment.parent_id);
                if (parent) {
                    parent.replies.push(comment);
                }
            } else {
                rootComments.push(comment);
            }
        });

        // 获取当前用户信息（需要在处理评论前获取）
        const currentUserId = user?.id;
        const isPostAuthor = currentUserId ? post.user_id === currentUserId : false;
        const viewer = {
            isAuthenticated: !!currentUserId,
            isAuthor: isPostAuthor,
        };
        const commentIds = comments.map((comment) => comment.id);
        const viewerVotes = {
            post: null as 'up' | 'down' | null,
            comments: {} as Record<string, 'up' | 'down'>,
        };

        if (currentUserId) {
            const voteTargetIds = [post.id, ...commentIds];
            if (voteTargetIds.length > 0) {
                const voteResult = await withRetry(async () => {
                    const response = await serviceClient
                        .from('community_votes')
                        .select('target_type, target_id, vote_type')
                        .eq('user_id', currentUserId)
                        .in('target_id', voteTargetIds);
                    if (response.error) {
                        throw response.error;
                    }
                    return response;
                });

                if (voteResult.error) {
                    console.error('获取帖子投票状态失败:', voteResult.error);
                } else {
                    for (const row of voteResult.data || []) {
                        if (row.target_type === 'post' && row.target_id === post.id) {
                            viewerVotes.post = row.vote_type as 'up' | 'down';
                            continue;
                        }
                        if (row.target_type === 'comment' && typeof row.target_id === 'string') {
                            viewerVotes.comments[row.target_id] = row.vote_type as 'up' | 'down';
                        }
                    }
                }
            }
        }

        // 为评论添加 author/isAuthor 标记，然后移除 user_id
        type SafeComment = Omit<CommentWithReplies, 'user_id' | 'replies'> & {
            author_name: string;
            author_avatar_url: string | null;
            isAuthor: boolean;
            isPostAuthor: boolean;
            replies: SafeComment[];
        };
        function processComment(comment: CommentWithReplies): SafeComment {
            const isCommentAuthor = currentUserId ? comment.user_id === currentUserId : false;
            const isPostAuthor = comment.user_id === post.user_id;
            const { replies, ...safeComment } = comment;
            delete (safeComment as { user_id?: unknown }).user_id;
            const authorProfile = authorMap.get(comment.user_id) || { name: '命理爱好者', avatarUrl: null };
            return {
                ...safeComment,
                author_name: authorProfile.name,
                author_avatar_url: authorProfile.avatarUrl,
                isAuthor: isCommentAuthor,
                isPostAuthor,
                replies: (replies || []).map(processComment),
            };
        }

        const safePost = toPublicPost(
            post as CommunityPostRow,
            authorMap.get(post.user_id) || { name: '命理爱好者', avatarUrl: null },
        );
        const safeComments = rootComments.map(c => processComment(c));

        return jsonOk({
            post: safePost,
            comments: safeComments,
            viewer,
            viewerVotes,
        });
    } catch (error) {
        console.error('获取帖子失败:', error);
        return jsonError('获取帖子失败', 500);
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
        let body: unknown;
        try {
            body = await request.json();
        } catch {
            return jsonError('请求体不是合法 JSON', 400);
        }

        const normalized = normalizePostInput(body, 'update');
        if ('error' in normalized) {
            return jsonError(normalized.error, 400);
        }

        // 只允许用户更新特定字段，防止权限提升
        const updateData: Record<string, unknown> = {
            ...normalized.data,
            updated_at: new Date().toISOString(),
        };

        const { data, error } = await db
            .from('community_posts')
            .update(updateData)
            .eq('id', id)
            .eq('user_id', user.id)
            .select()
            .single();

        if (error) {
            console.error('更新帖子失败:', error);
            return jsonError('更新帖子失败', 500);
        }

        const authorMap = await loadCommunityAuthorProfileMap(asCommunityLookupClient(db), [user.id]);
        return jsonOk(
            toPublicPost(data as CommunityPostRow, authorMap.get(user.id) || { name: '命理爱好者', avatarUrl: null }),
        );
    } catch (error) {
        console.error('更新帖子失败:', error);
        return jsonError('更新帖子失败', 500);
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

        const { error } = await db
            .from('community_posts')
            .update({ is_deleted: true, updated_at: new Date().toISOString() })
            .eq('id', id)
            .eq('user_id', user.id);

        if (error) {
            console.error('删除帖子失败:', error);
            return jsonError('删除帖子失败', 500);
        }

        return jsonOk({ success: true });
    } catch (error) {
        console.error('删除帖子失败:', error);
        return jsonError('删除帖子失败', 500);
    }
}
