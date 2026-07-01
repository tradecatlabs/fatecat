/**
 * 社区帖子列表 API 路由
 * GET: 获取帖子列表
 * POST: 创建新帖子
 */

import { NextRequest } from 'next/server';
import { PostCategory, PostFilters, normalizePostInput } from '@/lib/community';
import { asCommunityLookupClient, loadCommunityAuthorProfileMap, loadSingleCommunityAuthorProfile, toPublicPost, type CommunityPostRow } from '@/lib/community-server';
import { jsonError, jsonOk, requireUserContext, getSystemAdminClient } from '@/lib/api-utils';
import { withRetry } from '@/lib/retry';
import { parsePagination } from '@/lib/pagination';
import { quotePostgrestString } from '@/lib/utils/postgrest';

export async function GET(request: NextRequest) {
    try {
        const { searchParams } = new URL(request.url);

        const { from, to } = parsePagination(searchParams, { defaultPageSize: 20 });
        const category = searchParams.get('category') as PostCategory | null;
        const search = searchParams.get('search');
        const sortBy = searchParams.get('sortBy') as PostFilters['sortBy'] || 'latest';

        // 使用 serviceClient 和重试逻辑
        const serviceClient = getSystemAdminClient();

        const result = await withRetry(async () => {
            let query = serviceClient
                .from('community_posts')
                .select('*', { count: 'exact' })
                .eq('is_deleted', false);

            // 应用筛选条件
            if (category) {
                query = query.eq('category', category);
            }
            if (search) {
                const pattern = quotePostgrestString(`%${search}%`);
                query = query.or(`title.ilike.${pattern},content.ilike.${pattern}`);
            }

            // 排序
            if (sortBy === 'latest') {
                query = query.order('is_pinned', { ascending: false }).order('created_at', { ascending: false });
            } else if (sortBy === 'popular') {
                query = query.order('is_pinned', { ascending: false }).order('upvote_count', { ascending: false });
            } else if (sortBy === 'hot') {
                query = query.order('is_pinned', { ascending: false }).order('comment_count', { ascending: false });
            }

            // 分页
            query = query.range(from, to);

            const response = await query;
            if (response.error) {
                throw response.error;
            }
            return response;
        });

        if (result.error) {
            console.error('获取帖子失败:', result.error);
            return jsonError('获取帖子失败', 500);
        }

        const authorMap = await loadCommunityAuthorProfileMap(
            asCommunityLookupClient(serviceClient),
            (result.data || []).map((post: CommunityPostRow) => post.user_id),
        );
        const safePosts = (result.data || []).map((post: CommunityPostRow) =>
            toPublicPost(post, authorMap.get(post.user_id) || { name: '命理爱好者', avatarUrl: null }),
        );

        return jsonOk({
            posts: safePosts,
            total: result.count || 0,
        });
    } catch (error) {
        console.error('获取帖子失败:', error);
        return jsonError('获取帖子失败', 500);
    }
}

export async function POST(request: NextRequest) {
    try {
        const auth = await requireUserContext(request);
        if ('error' in auth) {
            return jsonError(auth.error.message, auth.error.status);
        }
        const { user } = auth;
        const db = auth.db;

        let body: unknown;
        try {
            body = await request.json();
        } catch {
            return jsonError('请求体不是合法 JSON', 400);
        }

        const normalized = normalizePostInput(body, 'create');
        if ('error' in normalized) {
            return jsonError(normalized.error, 400);
        }

        const authorProfile = await loadSingleCommunityAuthorProfile(asCommunityLookupClient(db), user.id);

        // 创建帖子
        const { data: post, error: postError } = await db
            .from('community_posts')
            .insert({
                user_id: user.id,
                ...normalized.data,
            })
            .select()
            .single();

        if (postError) {
            console.error('创建帖子失败:', postError);
            return jsonError('创建帖子失败', 500);
        }

        return jsonOk(toPublicPost(post as CommunityPostRow, authorProfile));
    } catch (error) {
        console.error('创建帖子失败:', error);
        return jsonError('创建帖子失败', 500);
    }
}
