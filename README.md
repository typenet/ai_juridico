# RAG Jurídico com Supabase, Docling e Streamlit

Este projeto é um agente de IA que analisa documentos jurídicos (PDFs), extrai informações com Docling, envia embeddings para o Supabase e permite buscas e resumos via interface Streamlit, utilizando uma LLM (como GPT-4 ou DeepSeek).

---

## Funcionalidades

- Leitura de PDFs jurídicos de uma pasta.
- Extração de dados com Docling e conversão para JSON.
- Indexação de trechos no Supabase com embeddings.
- Busca por CPF ou número de processo.
- Resumo automático dos documentos com LLM.
- Interface interativa com Streamlit.

---

## Como usar localmente

### 1. Clone o projeto
```bash
git clone https://github.com/typenet/ai_juridico.git
cd rag_juridico
```

### 2. Crie o ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate   # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o `.env`
Crie um arquivo `.env` com as chaves abaixo:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-supabase
OPENAI_API_KEY=sua-chave-openai-ou-deepseek
EMBEDDING_MODEL=text-embedding-ada-002
```

### 5. Prepare os dados
Coloque seus PDFs na pasta `pdfs/` e execute:

```bash
python scripts/process_chunks.py
```

### 6. Rode a interface
```bash
streamlit run app/streamlit_app.py
```

---

## Deploy no Streamlit Cloud

1. Faça o push do projeto para o GitHub.
2. Acesse: https://streamlit.io/cloud
3. Clique em “Deploy an app”.
4. Configure:
   - Main file: `app/streamlit_app.py`
   - Adicione as variáveis do `.env` em **Secrets**.
5. Clique em Deploy.

---

## Deploy em servidor próprio

```bash
# Clone e entre no projeto
git clone https://github.com/seu-usuario/rag_juridico.git
cd rag_juridico

# Ative o ambiente e instale dependências
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Exporte variáveis de ambiente
export $(cat .env | xargs)

# Rode o app
streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

---

## Licença

Este projeto é livre para uso e modificação conforme sua necessidade.
