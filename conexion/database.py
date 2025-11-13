import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from dotenv import load_dotenv, find_dotenv, dotenv_values

# Singleton globals
_client = None
_db = None


def criar_conexao():
    """
    Cria e testa a conexão com o banco MongoDB usando a URI definida no arquivo .env.
    Retorna uma tupla (client, db) se bem-sucedido, ou (None, None) em caso de erro.
    Também inicializa os singletons _client e _db globais.
    """
    global _client, _db
    
    # Localizar o arquivo .env do projeto
    env_path = find_dotenv() or os.path.join(os.path.dirname(__file__), '..', '.env')
    
    # Usar dotenv_values para ler explicitamente o arquivo
    env_vars = dotenv_values(env_path)
    
    # Carregar também via load_dotenv (compatibilidade)
    load_dotenv(dotenv_path=env_path)
    
    # Preferir valor do arquivo .env
    mongodb_uri = env_vars.get("MONGODB_URI") or env_vars.get("MONGO_URI") or os.getenv("MONGODB_URI")
    db_name = env_vars.get("DB_NAME") or os.getenv("DB_NAME", "aluguel_db")
    
    if not mongodb_uri:
        print("❌ Erro: Variável de ambiente MONGODB_URI não encontrada.", file=sys.stderr)
        return None, None

    try:
        _client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        _client.admin.command('ping')  # testa a conexão
        _db = _client[db_name]
        
        # Log seguro: mostrar host sem expor credenciais
        try:
            host = mongodb_uri.split('@', 1)[1].split('/', 1)[0]
            print(f"✅ Conexão estabelecida com sucesso! (host: {host}, db: {db_name})")
        except Exception:
            print(f"✅ Conexão estabelecida com sucesso! (db: {db_name})")
        
        return _client, _db
        
    except (ConnectionFailure, ConfigurationError) as err:
        print(f"❌ Erro ao conectar ao MongoDB: {err}", file=sys.stderr)
        _client = None
        _db = None
        return None, None
    except Exception as err:
        print(f"❌ Erro inesperado [criar_conexao]: {err}", file=sys.stderr)
        _client = None
        _db = None
        return None, None


def get_db():
    """Retorna a instância global do Database (ou None se não estiver inicializado)."""
    return _db


def get_client():
    """Retorna o MongoClient global (ou None se não estiver inicializado)."""
    return _client


def close_client():
    """Fecha o cliente MongoDB global caso exista."""
    global _client, _db
    if _client:
        try:
            _client.close()
        except Exception:
            pass
    _client = None
    _db = None