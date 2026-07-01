import type { MembershipType } from '@/lib/user/membership';

export type KnowledgeBaseWeight = 'low' | 'normal' | 'high';

export interface KnowledgeBase {
    id: string;
    user_id: string;
    name: string;
    description: string | null;
    weight: KnowledgeBaseWeight;
    created_at: string;
    updated_at: string;
}

export interface KnowledgeBaseInput {
    name: string;
    description?: string | null;
    weight?: KnowledgeBaseWeight;
}

export type SearchConfig = 'simple' | 'english';

export type SearchMethod = 'fts' | 'trigram' | 'vector';

export interface SearchCandidate {
    id: string;
    kbId: string;
    content: string;
    metadata: Record<string, unknown>;
    score: number;
    method: SearchMethod;
}

export interface RankedResult extends SearchCandidate {
    rank: number;
}

export interface SearchOptions {
    kbIds?: string[];
    limit?: number;
    topK?: number;
    useVector?: boolean;
    accessToken?: string;
    userId?: string;
    membershipType?: MembershipType;
    searchConfig?: Partial<{
        ftsConfig: SearchConfig;
        enableTrigram: boolean;
        trigramThreshold: number;
    }>;
}

export interface SearchResult {
    results: RankedResult[] | SearchCandidate[];
}

export interface KnowledgeHit {
    kbId: string;
    kbName: string;
    content: string;
    score: number;
}

export interface IngestResult {
    entriesCreated: number;
    chunks: number;
}
