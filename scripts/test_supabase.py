import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as variáveis de ambiente
load_dotenv()

# Obtém as credenciais do Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

def test_supabase_connection():
    try:
        # Cria o cliente Supabase
        supabase: Client = create_client(url, key)
        
        # Tenta fazer uma consulta simples
        response = supabase.table('_tables').select("*").limit(1).execute()
        
        print("✅ Conexão com o Supabase estabelecida com sucesso!")
        print(f"URL: {url}")
        print(f"Status da resposta: {response.status_code}")
        
    except Exception as e:
        print("❌ Erro ao conectar com o Supabase:")
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    test_supabase_connection() 