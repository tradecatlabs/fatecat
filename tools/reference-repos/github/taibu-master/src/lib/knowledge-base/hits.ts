import 'server-only';

import type { SupabaseClient } from '@supabase/supabase-js';
import { searchKnowledge } from '@/lib/knowledge-base/search';
import { stripMentionTokens } from '@/lib/mentions';
import type { KnowledgeHit, RankedResult, SearchCandidate } from '@/lib/knowledge-base/types';
import type { MembershipType } from '@/lib/user/membership';

export interface BuildKnowledgeHitsOptions {
    query: string;
    userId: string;
    membershipType: MembershipType;
    accessToken: string | null;
    promptKbIds: string[];
    supabase: SupabaseClient;
}

/**
 * Shared knowledge base search and hit builder.
 *
 * Replaces duplicate implementations in:
 * - src/lib/server/chat/prompt-context.ts
 * - src/lib/chat/preview-context.ts
 */
export async function buildKnowledgeHits({
    query,
    userId,
    membershipType,
    accessToken,
    promptKbIds,
    supabase,
}: BuildKnowledgeHitsOptions): Promise<KnowledgeHit[]> {
    if (membershipType === 'free') return [];

    const cleanedQuery = stripMentionTokens(query);
    if (!cleanedQuery || promptKbIds.length === 0) return [];

    const results = await searchKnowledge(cleanedQuery, {
        limit: 12,
        topK: 5,
        accessToken: accessToken || undefined,
        userId,
        kbIds: promptKbIds,
        membershipType,
    });

    const candidates = results as Array<SearchCandidate | RankedResult>;
    const kbIds = Array.from(
        new Set(candidates.map((result) => result.kbId).filter(Boolean))
    ) as string[];

    if (kbIds.length === 0) return [];

    const { data: kbRows } = await supabase
        .from('knowledge_bases')
        .select('id, name, weight')
        .eq('user_id', userId)
        .in('id', kbIds);

    const kbMap = new Map<string, { name: string; weight: string }>();
    for (const kb of kbRows || []) {
        if (typeof kb.id === 'string' && typeof kb.name === 'string') {
            kbMap.set(kb.id, {
                name: kb.name,
                weight: typeof kb.weight === 'string' ? kb.weight : 'normal',
            });
        }
    }

    return candidates.slice(0, 8).map((result): KnowledgeHit => ({
        kbId: result.kbId,
        kbName: kbMap.get(result.kbId)?.name || '知识库',
        content: result.content,
        score: result.score || 0,
    }));
}
