import os
import uuid
import pdfplumber
import datetime
import requests
from utils import get_embedding, chunk_text

# Definindo os caminhos
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "pdfs")
LOG_FOLDER = os.path.join(BASE_DIR, "logs")

# Criando as pastas se não existirem
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def setup_logs():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    processed_log = os.path.join(LOG_FOLDER, f"processed_{timestamp}.log")
    error_log = os.path.join(LOG_FOLDER, f"errors_{timestamp}.log")
    return processed_log, error_log

def log_processed(file_path, log_file):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - Processado: {file_path}\n")

def log_error(file_path, error_msg, log_file):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - Erro: {file_path} - {error_msg}\n")

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

def process_with_docling(pdf_path, processed_log, error_log):
    text = extract_text_from_pdf(pdf_path, error_log)
    if text:
        log_processed(pdf_path, processed_log)
    return {
        "id": str(uuid.uuid4()),
        "text": text,
        "metadata": {},
        "tokens": [],
        "entities": [],
        "relations": []
    }

def save_to_supabase(data):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    # Garantindo que todos os campos necessários estejam presentes
    required_fields = {
        "id": data.get("id", str(uuid.uuid4())),
        "cpf": data.get("cpf", ""),
        "processo": data.get("processo", ""),
        "data": data.get("data", ""),
        "tipo": data.get("tipo", ""),
        "titulo": data.get("titulo", ""),
        "chunk_index": data.get("chunk_index", 0),
        "text": data.get("text", ""),
        "embedding": data.get("embedding", []),
        "source": data.get("source", "")
    }
    
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/document_chunks",
            headers=headers,
            json=required_fields
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar no Supabase: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Detalhes do erro: {e.response.text}")
        return False

def process_json(doc_json, source):
    metadata = doc_json.get("metadata", {})
    text = doc_json.get("text", "")
    cpf = metadata.get("cpf", "")
    processo = metadata.get("processo", "")
    data = metadata.get("data", "")
    tipo = metadata.get("tipo", "")
    titulo = metadata.get("titulo", os.path.basename(source))

    chunks = chunk_text(text, max_tokens=500)

    for i, chunk in enumerate(chunks):
        emb = get_embedding(chunk)
        if emb is None:
            continue
            
        data_row = {
            "id": str(uuid.uuid4()),
            "cpf": cpf,
            "processo": processo,
            "data": data,
            "tipo": tipo,
            "titulo": titulo,
            "chunk_index": i,
            "text": chunk,
            "embedding": emb,
            "source": source
        }
        save_to_supabase(data_row)

def process_folder(folder_path):
    processed_log, error_log = setup_logs()
    print(f"\n📝 Logs iniciados em:")
    print(f"✅ Processados: {processed_log}")
    print(f"❌ Erros: {error_log}\n")
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(folder_path, filename)
            print(f"Convertendo: {filename}")
            doc_json = process_with_docling(filepath, processed_log, error_log)
            process_json(doc_json, filepath)

if __name__ == "__main__":
    process_folder(PDF_FOLDER)
