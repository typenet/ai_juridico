import os
import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL")

print("🔍 Testando conexão com a API do Deepseek...")

headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}

# Texto de exemplo para testar
payload = {
    "input": "Este é um texto de exemplo para gerar embeddings.",
    "model": "text-embedding-ada-002"
}

try:
    print("📤 Enviando requisição...")
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    print("✅ Conexão bem-sucedida!")
    print("🔢 Primeiros valores do embedding:", data["data"][0]["embedding"][:5])
except requests.exceptions.RequestException as e:
    print(f"❌ Erro na conexão: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print("Status code:", e.response.status_code)
        print("Resposta:", e.response.text)
