import os
import uuid
from docling import load
from utils import get_embedding, supabase, chunk_text

PDF_FOLDER = "./pdfs"

def process_with_docling(pdf_path):
    doc = load(pdf_path)
    return doc.to_dict()

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
        supabase.table("document_chunks").upsert(data_row).execute()

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(folder_path, filename)
            print(f"Convertendo: {filename}")
            doc_json = process_with_docling(filepath)
            process_json(doc_json, filepath)

if __name__ == "__main__":
    process_folder(PDF_FOLDER)
