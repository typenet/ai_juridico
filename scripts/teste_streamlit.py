import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define o modelo
model = genai.GenerativeModel("models/gemini-1.5-pro")  # ou outro da sua lista

st.title("🧠 Teste de Prompts com Gemini")
st.markdown("Use este app para testar respostas do modelo Gemini com diferentes estilos de prompts.")

# Entrada do texto base
texto_base = st.text_area("Texto base para o modelo interpretar", "O contrato estipula que o cliente tem 7 dias para desistência.")

# Tipo de prompt
tipo_prompt = st.selectbox(
    "Selecione o estilo de resposta desejado:",
    ["Resumo jurídico", "Resumo simples", "Explicação jurídica", "Tópicos resumidos", "Reescrever em linguagem simples"]
)

# Geração de prompt
def montar_prompt(texto, tipo):
    if tipo == "Resumo jurídico":
        return f"Resuma formalmente o seguinte conteúdo jurídico com linguagem técnica clara:\n\n{texto}"
    elif tipo == "Resumo simples":
        return f"Faça um resumo claro e simples do seguinte texto:\n\n{texto}"
    elif tipo == "Explicação jurídica":
        return f"Explique o significado jurídico do seguinte trecho:\n\n{texto}"
    elif tipo == "Tópicos resumidos":
        return f"Liste em tópicos os principais pontos do seguinte texto jurídico:\n\n{texto}"
    elif tipo == "Reescrever em linguagem simples":
        return f"Reescreva o seguinte texto jurídico em uma linguagem acessível para leigos:\n\n{texto}"
    else:
        return texto

# Botão de execução
if st.button("Gerar resposta"):
    with st.spinner("Consultando o modelo Gemini..."):
        try:
            prompt = montar_prompt(texto_base, tipo_prompt)
            response = model.generate_content(prompt)
            st.success("✅ Resposta gerada com sucesso:")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"❌ Erro ao gerar conteúdo: {e}")
