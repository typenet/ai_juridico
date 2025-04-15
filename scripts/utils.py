# utils.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/embedding-001")

# Configuração da API Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Cria o modelo de embedding
embedding_model = genai.EmbeddingModel(model_name=EMBEDDING_MODEL)

def get_embedding(text):
    try:
        response = embedding_model.embed_content(
            content=text,
            task_type="retrieval_document"
        )
        return response['embedding']
    except Exception as e:
        print(f"❌ Erro ao gerar embedding: {e}")
        return None

def chunk_text(text, max_tokens=500):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def generate_summary_from_chunks(chunks_with_content):
    combined_text = "\n".join([item['chunk_content'] for item in chunks_with_content])
    model = genai.GenerativeModel("gemini-pro")

    try:
        prompt = f"Resuma o seguinte conteúdo jurídico de forma clara e objetiva:\n\n{combined_text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Erro ao gerar resumo: {e}")
        return "Erro ao gerar resumo."