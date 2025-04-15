import google.generativeai as genai
import numpy as np
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da chave da API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Função para obter o embedding de um texto
def get_embedding(text: str):
    try:
        # Usando a função adequada para gerar embeddings
        response = genai.embed(text=text)  # Alterando para a função correta de embeddings
        embedding = response['embedding']  # Assumindo que o retorno tem a chave 'embedding'
        return embedding
    except Exception as e:
        print(f"❌ Erro ao gerar embedding: {e}")
        return None

# Função para dividir o texto em chunks com base no número máximo de tokens
def chunk_text(text: str, max_tokens: int):
    """Divide o texto em chunks menores para se ajustar ao limite de tokens"""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk + [word])) > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Função para gerar resumo a partir de chunks
def generate_summary_from_chunks(chunks):
    """
    Gera um resumo a partir de uma lista de chunks.
    Utiliza a API Gemini para gerar o resumo.
    """
    try:
        full_text = " ".join([chunk['chunk_content'] for chunk in chunks])
        response = genai.generate_text(  # Mudança para usar a função correta para geração de texto
            model="models/gemini-1.5-flash-latest",
            prompt=full_text,
            temperature=0.7,
            max_output_tokens=300  # Ajuste de acordo com a necessidade
        )
        return response['text']
    except Exception as e:
        print(f"❌ Erro ao gerar resumo: {e}")
        return "Erro ao gerar resumo."
