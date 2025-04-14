import os
from dotenv import load_dotenv
from supabase import create_client
import requests

load_dotenv()

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def create_table():
    try:
        # Configurar headers para a API
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }
        
        # SQL para criar a tabela
        sql = """
        create table if not exists document_chunks (
            id uuid primary key,
            cpf text,
            processo text,
            data text,
            tipo text,
            titulo text,
            chunk_index integer,
            text text,
            embedding vector(1536),
            source text
        );
        """
        
        # Fazer requisição para a API REST do Supabase
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
            headers=headers,
            json={"sql": sql}
        )
        
        if response.status_code == 200:
            print("✅ Tabela criada com sucesso!")
        else:
            print(f"❌ Erro ao criar tabela: {response.text}")
        
    except Exception as e:
        print(f"❌ Erro ao criar tabela: {str(e)}")

if __name__ == "__main__":
    create_table() 