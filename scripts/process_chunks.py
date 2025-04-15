import os
import uuid
import pdfplumber
import datetime
import requests
from dotenv import load_dotenv
from utils import get_embedding, chunk_text  # Certifique-se que este arquivo existe e está correto

# Definindo os caminhos
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "pdfs")
LOG_FOLDER = os.path.join(BASE_DIR, "logs")

# Criando as pastas se não existirem
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# Carrega variáveis de ambiente
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def setup_logs():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    processed_log = os.path.join(LOG_FOLDER, f"processed_{timestamp}_embeddings.log")
    error_log = os.path.join(LOG_FOLDER, f"errors_{timestamp}_embeddings.log")
    return processed_log, error_log

def log_processed(file_path, log_file):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - Embedding Processado: {file_path}\n")

def log_error(file_path, error_msg, log_file):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - Erro (Embedding): {file_path} - {error_msg}\n")

def is_valid_pdf(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            return header == b'%PDF'
    except:
        return False

def extract_text_from_pdf(file_path, error_log):
    if not is_valid_pdf(file_path):
        error_msg = "Arquivo inválido ou não é um PDF"
        log_error(file_path, error_msg, error_log)
        print(f"⚠️ {error_msg}: {os.path.basename(file_path)}")
        return ""

    try:
        all_text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text.append(text)
        return "\n".join(all_text)
    except Exception as e:
        error_msg = str(e)
        log_error(file_path, error_msg, error_log)
        print(f"❌ Erro ao processar PDF {os.path.basename(file_path)}: {error_msg}")
        return ""

def process_pdf_for_embeddings(pdf_path, processed_log, error_log):
    text = extract_text_from_pdf(pdf_path, error_log)
    if text:
        log_processed(pdf_path, processed_log)
        return {"text": text, "source": pdf_path}
    return None

def save_embedding_to_supabase(embedding_data, table_name="document_chunks"):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/{table_name}",
            headers=headers,
            json=embedding_data
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar embedding no Supabase: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Detalhes do erro: {e.response.text}")
        return False

def process_pdf_and_save_embeddings(pdf_data):
    if pdf_data and pdf_data["text"]:
        source = pdf_data["source"]
        chunks = chunk_text(pdf_data["text"], max_tokens=500)

        for i, chunk in enumerate(chunks):
            emb = get_embedding(chunk)
            if emb is None:
                print(f"⚠️ Falha ao gerar embedding para chunk {i} de {os.path.basename(source)}")
                continue

            embedding_data = {
                "id": str(uuid.uuid4()),
                "embedding": emb,
                "chunk_content": chunk  # Adicionando a coluna chunk_content
            }
            if save_embedding_to_supabase(embedding_data):
                print(f"✅ Embedding e conteúdo para chunk {i} de {os.path.basename(source)} salvo.")
            else:
                print(f"❌ Falha ao salvar embedding e conteúdo para chunk {i} de {os.path.basename(source)}.")

def process_folder_for_embeddings(folder_path):
    processed_log, error_log = setup_logs()
    print(f"\n📝 Logs de embeddings iniciados em:")
    print(f"✅ Processados: {processed_log}")
    print(f"❌ Erros: {error_log}\n")

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(folder_path, filename)
            print(f"Processando para embeddings: {filename}")
            pdf_data = process_pdf_for_embeddings(filepath, processed_log, error_log)
            if pdf_data:
                process_pdf_and_save_embeddings(pdf_data)

if __name__ == "__main__":
    process_folder_for_embeddings(PDF_FOLDER)
    print("\n✅ Processamento de embeddings e conteúdo concluído.")