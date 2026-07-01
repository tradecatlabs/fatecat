import postgres from 'https://deno.land/x/postgresjs@v3.4.5/mod.js';

const VECTOR_DIMENSIONS = [1536, 1024, 768] as const;

interface CreateIndexRequest {
    dimension?: number;
}

Deno.serve(async (req: Request) => {
    const internalHeader = req.headers.get('x-internal-api-secret');
    const internalSecret = Deno.env.get('INTERNAL_API_SECRET');

    if (!internalSecret) {
        return new Response(JSON.stringify({ error: 'Server misconfigured' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    if (internalHeader !== internalSecret) {
        return new Response(JSON.stringify({ error: 'Unauthorized' }), {
            status: 401,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    let requestedDimension: number | undefined;
    try {
        if (req.method === 'POST') {
            const body = await req.json() as CreateIndexRequest;
            requestedDimension = body.dimension;
        }
    } catch {
        requestedDimension = undefined;
    }

    if (requestedDimension !== undefined) {
        if (!Number.isInteger(requestedDimension) || requestedDimension <= 0) {
            return new Response(JSON.stringify({
                error: 'Invalid dimension: must be a positive integer'
            }), {
                status: 400,
                headers: { 'Content-Type': 'application/json' }
            });
        }

        if (!VECTOR_DIMENSIONS.includes(requestedDimension as typeof VECTOR_DIMENSIONS[number])) {
            return new Response(JSON.stringify({
                error: `Invalid dimension: must be one of ${VECTOR_DIMENSIONS.join(', ')}`,
                allowedDimensions: VECTOR_DIMENSIONS
            }), {
                status: 400,
                headers: { 'Content-Type': 'application/json' }
            });
        }
    }

    const databaseUrl = Deno.env.get('SUPABASE_DB_URL');
    if (!databaseUrl) {
        return new Response(JSON.stringify({ error: 'Database URL not configured' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    const sql = postgres(databaseUrl, {
        max: 1,
        idle_timeout: 20,
        connect_timeout: 30
    });

    try {
        const results: Array<{ dimension: number; status: string; error?: string }> = [];
        const dimensionsToProcess = requestedDimension ? [requestedDimension] : VECTOR_DIMENSIONS;

        for (const dim of dimensionsToProcess) {
            const indexName = `knowledge_entries_vector_${dim}_idx`;

            if (!/^[a-zA-Z0-9_]+$/.test(indexName)) {
                results.push({ dimension: dim, status: 'failed', error: 'Invalid index name pattern' });
                continue;
            }

            try {
                const [existing] = await sql`
                    SELECT 1 FROM pg_indexes
                    WHERE schemaname = 'public'
                      AND indexname = ${indexName}
                `;

                if (existing) {
                    results.push({ dimension: dim, status: 'already_exists' });
                    continue;
                }

                const [hasData] = await sql`
                    SELECT EXISTS (
                        SELECT 1 FROM public.knowledge_entries
                        WHERE (metadata->>'embedding_dim')::int = ${dim}
                          AND content_vector IS NOT NULL
                        LIMIT 1
                    ) as has_data
                `;

                if (!hasData?.has_data) {
                    results.push({ dimension: dim, status: 'skipped_no_data' });
                    continue;
                }

                await sql.unsafe(`
                    CREATE INDEX CONCURRENTLY IF NOT EXISTS ${indexName}
                    ON public.knowledge_entries
                    USING ivfflat ((content_vector::vector(${dim})) vector_cosine_ops)
                    WITH (lists = 100)
                    WHERE (metadata->>'embedding_dim')::int = ${dim}
                `);

                results.push({ dimension: dim, status: 'created' });
            } catch (error) {
                results.push({
                    dimension: dim,
                    status: 'failed',
                    error: error instanceof Error ? error.message : String(error)
                });
            }
        }

        return new Response(JSON.stringify({
            success: true,
            results,
            timestamp: new Date().toISOString()
        }), {
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (error) {
        return new Response(JSON.stringify({
            success: false,
            error: error instanceof Error ? error.message : String(error)
        }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    } finally {
        await sql.end();
    }
});
