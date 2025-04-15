import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar Gemini com API Key
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY"),
    transport="rest"
)

# Usar um modelo disponível (sugestão: gemini-1.5-pro-latest)
modelo_escolhido = "models/gemini-1.5-pro-latest"

# Testar geração de conteúdo
try:
    model = genai.GenerativeModel(modelo_escolhido)
    prompt = "Resuma: O contrato estipula que o cliente tem 7 dias para desistência."
    response = model.generate_content(prompt)
    print("\n✅ Resumo gerado:\n")
    print(response.text)
except Exception as e:
    print(f"\n❌ Erro ao gerar conteúdo: {str(e)}")
