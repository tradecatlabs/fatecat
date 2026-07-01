import 'server-only';

import type { SupabaseClient } from '@supabase/supabase-js';

async function getFeatureFlag(key: string): Promise<boolean> {
    const val = process.env[key];
    if (!val) return false;
    return val === 'true' || val === '1';
}

export async function createVectorIndexIfNeeded(
    supabase: SupabaseClient
): Promise<{ success: boolean; error?: string }> {
    const { data: indexExists } = await supabase.rpc('check_vector_index_exists');
    if (indexExists) return { success: true };

    const vectorEnabled = await getFeatureFlag('VECTOR_SEARCH_ENABLED');
    if (!vectorEnabled) {
        return { success: false, error: 'Vector search not enabled' };
    }

    try {
        await triggerVectorIndexJob();
        return { success: true };
    } catch (error) {
        return { success: false, error: String(error) };
    }
}

async function triggerVectorIndexJob(): Promise<void> {
    const supabaseUrl = process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL;
    const anonKey = process.env.SUPABASE_ANON_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    const internalSecret = process.env.INTERNAL_API_SECRET;

    if (!supabaseUrl || !anonKey || !internalSecret) {
        throw new Error('Missing Supabase configuration (SUPABASE_URL, SUPABASE_ANON_KEY and INTERNAL_API_SECRET required)');
    }

    const response = await fetch(`${supabaseUrl}/functions/v1/create-vector-index`, {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${anonKey}`,
            apikey: anonKey,
            'x-internal-api-secret': internalSecret,
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) {
        throw new Error('Vector index job failed');
    }
}

export async function triggerVectorIndexCreation(dimension?: number): Promise<{
    success: boolean;
    results?: Array<{ dimension: number; status: string }>;
    error?: string;
}> {
    const supabaseUrl = process.env.SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL;
    const anonKey = process.env.SUPABASE_ANON_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    const internalSecret = process.env.INTERNAL_API_SECRET;

    if (!supabaseUrl || !anonKey || !internalSecret) {
        throw new Error('Missing Supabase configuration (SUPABASE_URL, SUPABASE_ANON_KEY and INTERNAL_API_SECRET required)');
    }

    const response = await fetch(`${supabaseUrl}/functions/v1/create-vector-index`, {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${anonKey}`,
            apikey: anonKey,
            'x-internal-api-secret': internalSecret,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ dimension })
    });

    if (!response.ok) {
        const error = await response.text();
        return { success: false, error };
    }

    return await response.json();
}
