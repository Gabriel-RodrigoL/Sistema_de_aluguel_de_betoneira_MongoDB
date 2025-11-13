import sys
import os

# --- INÍCIO DO CÓDIGO PARA EXECUÇÃO DIRETA ---
# Este bloco de código permite que o programa seja executado diretamente
# sem a necessidade de usar o comando `python -m`.
try:
    # Obtém o diretório do ficheiro 'main.py'
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    # Adiciona a pasta pai (que contém a pasta 'trabalho_BD') ao caminho do Python
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    # Importa os módulos necessários usando caminhos absolutos
    from utils.menu import menu
    from conexion import database
except ImportError as e:
    print("\nERRO DE IMPORTAÇÃO: Não foi possível encontrar os módulos do projeto.")
    print(f"Detalhe: {e}")
    print("Certifique-se de que está a executar o 'main.py' de dentro da pasta 'trabalho_BD'.")
    sys.exit(1) # Encerra o programa se a importação falhar
# --- FIM DO CÓDIGO PARA EXECUÇÃO DIRETA ---

def main():
    """Função principal que inicia a aplicação."""
    print("A tentar conectar à base de dados...")
    client, db = database.criar_conexao()
    if db is not None:
        print("Conexão bem-sucedida. A iniciar aplicação...")
        try:
            menu()
        finally:
            if client:
                client.close()
    else:
        print("\nERRO CRÍTICO: Não foi possível conectar à base de dados.")
        print("Verifique as suas credenciais no ficheiro .env e a sua ligação à Internet.")

if __name__ == "__main__":
    main()
