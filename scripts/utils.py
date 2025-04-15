import os
from dotenv import load_dotenv
import tiktoken
import google.generativeai as genai

load_dotenv()

# Configuração do Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text):
    try:
        # Usando o modelo correto do Gemini para embeddings
        result = genai.embed_content(
            model="models/embedding-001",  # <- Correção aqui
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"❌ Erro na API do Gemini: {str(e)}")
        return None

def chunk_text(text, max_tokens=500):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for token in tokens:
        current_chunk.append(token)
        current_length += 1
        
        if current_length >= max_tokens:
            chunks.append(encoding.decode(current_chunk))
            current_chunk = []
            current_length = 0
    
    if current_chunk:
        chunks.append(encoding.decode(current_chunk))
    
    return chunks
