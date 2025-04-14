-- Criar extensão para vetores se ainda não existir
create extension if not exists vector;

-- Criar tabela document_chunks
create table if not exists document_chunks (
    id uuid primary key,
    cpf text,
    processo text,
    data text,
    tipo text,
    titulo text,
    chunk_index integer,
    text text,
    embedding vector(1536),
    source text
);

-- Criar índice para busca por similaridade
create index on document_chunks 
using ivfflat (embedding vector_cosine_ops)
with (lists = 100); 