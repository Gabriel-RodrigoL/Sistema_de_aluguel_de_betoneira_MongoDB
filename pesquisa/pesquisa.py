import pandas as pd
from conexion import database
import sys
import warnings


def listar_todos_clientes():

    conn = None
    try:
        conn = database.criar_conexao()
        if not conn:
            print("\n>> Erro de conexão.")
            return

        sql = "SELECT id, nome, telefone, cpf FROM clientes ORDER BY nome"
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql(sql, conn)

        if df.empty:
            print("\n>> Nenhum cliente registado.")
        else:
            print("\n--- Lista de Clientes ---")
            print(df.to_string(index=False))

    except Exception as e:
        print(f"\n>> Erro inesperado ao listar clientes: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

def listar_todas_betoneiras():

    conn = None
    try:
        conn = database.criar_conexao()
        if not conn:
            print("\n>> Erro de conexão.")
            return
            
        sql = "SELECT id, modelo, valor, status FROM betoneiras ORDER BY id"

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql(sql, conn)

        if df.empty:
            print("\n>> Nenhuma betoneira registada.")
        else:
            print("\n--- Lista de Betoneiras ---")
            df['valor'] = df['valor'].map('R${:,.2f}'.format)
            print(df.to_string(index=False))

    except Exception as e:
        print(f"\n>> Erro inesperado ao listar betoneiras: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

def listar_betoneiras_disponiveis():

    conn = None
    try:
        conn = database.criar_conexao()
        if not conn:
            print("\n>> Erro de conexão.")
            return

        sql = "SELECT id, modelo, valor FROM betoneiras WHERE status = 'disponivel' ORDER BY id"
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql(sql, conn)

        if df.empty:
            print("\n>> Nenhuma betoneira disponível no momento.")
        else:
            print("\n--- Betoneiras Disponíveis ---")
            df['valor'] = df['valor'].map('R${:,.2f}'.format)
            print(df.to_string(index=False))

    except Exception as e:
        print(f"\n>> Erro inesperado ao gerar relatório: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

def listar_alugueis_ativos():

    conn = None
    try:
        conn = database.criar_conexao()
        if not conn:
            print("\n>> Erro de conexão.")
            return

        sql = """
            SELECT
                a.id AS id_aluguel,
                c.nome AS cliente,
                b.modelo AS betoneira,
                a.data_inicio,
                a.data_prevista_termino
            FROM alugueis a
            JOIN clientes c ON a.id_cliente = c.id
            JOIN betoneiras b ON a.id_betoneira = b.id
            WHERE a.status = 'ativo'
            ORDER BY a.data_prevista_termino ASC
        """
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql(sql, conn)
        
        if df.empty:
            print("\n>> Nenhum aluguel ativo no momento.")
        else:
            print("\n--- Aluguéis Ativos ---")
            print(df.to_string(index=False))

    except Exception as e:
        print(f"\n>> Erro inesperado ao gerar relatório: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

def historico_alugueis():

    conn = None
    try:
        conn = database.criar_conexao()
        if not conn:
            print("\n>> Erro de conexão.")
            return

        sql = """
            SELECT
                a.id AS id_aluguel,
                c.nome AS cliente,
                b.modelo AS betoneira,
                a.data_inicio,
                a.data_termino_real,
                a.status
            FROM alugueis a
            JOIN clientes c ON a.id_cliente = c.id
            JOIN betoneiras b ON a.id_betoneira = b.id
            ORDER BY a.data_inicio DESC
        """

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            df = pd.read_sql(sql, conn)

        if df.empty:
            print("\n>> Nenhum histórico de aluguel encontrado.")
        else:
            print("\n--- Histórico de Aluguéis ---")
            print(df.to_string(index=False))

    except Exception as e:
        print(f"\n>> Erro inesperado ao consultar histórico: {e}", file=sys.stderr)
    finally:
        if conn:
            conn.close()

