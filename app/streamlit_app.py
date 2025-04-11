import streamlit as st
from utils import retrieve_chunks_by_identifier, generate_summary_from_chunks

st.set_page_config(page_title="RAG Jurídico", layout="wide")
st.title("Resumo de Documentos Jurídicos com IA")

identifier = st.text_input("Informe o número do processo ou CPF do cliente")

if identifier:
    st.info("Buscando documentos relacionados...")
    chunks = retrieve_chunks_by_identifier(identifier)
    if chunks:
        st.success(f"{len(chunks)} trechos encontrados. Gerando resumo...")
        resumo = generate_summary_from_chunks(chunks)
        st.subheader("Resumo do Documento")
        st.write(resumo)
    else:
        st.warning("Nenhum trecho encontrado para este identificador.")
