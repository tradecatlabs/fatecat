DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes
        WHERE indexname = 'knowledge_entries_vector_idx'
    ) THEN
        RAISE NOTICE 'Creating vector index...';
    END IF;
END $$;

CREATE INDEX CONCURRENTLY IF NOT EXISTS knowledge_entries_vector_idx
    ON public.knowledge_entries
    USING ivfflat (content_vector vector_cosine_ops)
    WITH (lists = 100);
