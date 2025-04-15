# streamlit_app.py
import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from utils import get_embedding, generate_summary_from_chunks  # Importe as funções necessárias

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def retrieve_text_by_ids(ids):
    """Recupera o conteúdo dos chunks da tabela document_chunks pelos seus IDs."""
    try:
        response = supabase.table("document_chunks").select("id, chunk_content").in_("id", ids).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as e:
        st.error(f"Erro ao buscar conteúdo dos chunks: {e}")
        return []

st.title("Seu Aplicativo de Resumo Jurídico")

identifier = st.text_input("Digite um identificador para buscar documentos:")
top_k = st.slider("Número de documentos relevantes para buscar:", min_value=1, max_value=5, value=3)

if st.button("Buscar e Gerar Resumo"):
    if identifier:
        query_embedding = get_embedding(identifier)
        if query_embedding is not None:
            response = supabase.rpc("match_document_chunks", {
                "query_embedding": query_embedding,
                "match_count": top_k
            }).execute()

            if response.data:
                relevant_ids = [item['id'] for item in response.data]
                relevant_chunks_with_content = retrieve_text_by_ids(relevant_ids)

                if relevant_chunks_with_content:
                    resumo = generate_summary_from_chunks(relevant_chunks_with_content)
                    st.subheader("Resumo:")
                    st.write(resumo)
                else:
                    st.warning("Não foram encontrados chunks com conteúdo para gerar o resumo.")
            else:
                st.warning("Não foram encontrados documentos relevantes.")
        else:
            st.error("Erro ao gerar embedding para o identificador.")
    else:
        st.warning("Por favor, digite um identificador.")