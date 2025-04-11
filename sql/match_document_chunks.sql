-- SQL Function for Supabase
CREATE FUNCTION match_document_chunks(query_embedding vector, match_count int)
RETURNS TABLE (
  id uuid,
  cpf text,
  processo text,
  text text,
  similarity float
)
LANGUAGE sql STABLE AS $$
  SELECT id, cpf, processo, text, 1 - (embedding <=> query_embedding) AS similarity
  FROM document_chunks
  ORDER BY embedding <=> query_embedding
  LIMIT match_count;
$$;
