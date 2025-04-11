import requests
import numpy as np
from supabase import create_client, Client
import tiktoken
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "deepseek-embedding")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_embedding(text):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "input": text,
        "model": EMBEDDING_MODEL
    }
    
    response = requests.post(
        "https://api.deepseek.com/v1/embeddings",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        return response.json()['data'][0]['embedding']
    else:
        raise Exception(f"Erro ao obter embedding: {response.text}")

def chunk_text(text, max_tokens=500):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    chunks = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [enc.decode(chunk) for chunk in chunks]

def retrieve_chunks_by_identifier(identifier, top_k=5):
    query_embedding = get_embedding(identifier)
    response = supabase.rpc("match_document_chunks", {
        "query_embedding": query_embedding,
        "match_count": top_k
    }).execute()
    return response.data

def generate_summary_from_chunks(chunks):
    texto = "\n\n".join(chunk["text"] for chunk in chunks)
    prompt = f"Faça um resumo detalhado e claro do seguinte conteúdo jurídico:\n{texto}"
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Erro ao gerar resumo: {response.text}")
