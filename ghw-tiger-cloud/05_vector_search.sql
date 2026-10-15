-- ==============================================================================
-- Challenge 11: Implement AI-Powered Vector Search with pgvector
-- Native PostgreSQL Vector Storage & HNSW Similarity Search in Tiger Cloud
-- ==============================================================================

-- 1. Ensure pgvector extension is loaded
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create Knowledge Base table storing semantic vector embeddings
CREATE TABLE IF NOT EXISTS rag_knowledge_base (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    title VARCHAR(128) NOT NULL,
    category VARCHAR(32) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(384) NOT NULL
);

-- 3. Create HNSW (Hierarchical Navigable Small World) index for sub-millisecond approximate nearest neighbor search
CREATE INDEX IF NOT EXISTS idx_rag_hnsw_cosine 
ON rag_knowledge_base USING hnsw (embedding vector_cosine_ops);

-- 4. Create hybrid metadata B-tree index
CREATE INDEX IF NOT EXISTS idx_rag_category_created 
ON rag_knowledge_base (category, created_at DESC);

-- 5. Verification
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'rag_knowledge_base' AND column_name = 'embedding';
