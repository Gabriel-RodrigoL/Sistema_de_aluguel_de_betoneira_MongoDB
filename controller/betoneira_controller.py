from conexion import database
import sys
from bson.objectid import ObjectId


def cadastrar_betoneira(modelo, valor):
    db = database.get_db()
    if db is None:
        return "Erro: Não foi possível conectar ao banco de dados."

    try:
        col = db.betoneiras
        doc = {"modelo": modelo, "valor": float(valor), "status": "disponivel"}
        res = col.insert_one(doc)
        return f"Betoneira registada com sucesso! id: {str(res.inserted_id)}"
    except Exception as e:
        print(f"Erro inesperado [cadastrar_betoneira]: {e}", file=sys.stderr)
        return "Erro ao registar betoneira."


def atualizar_dados_betoneira(id_betoneira, novo_modelo, novo_valor):
    db = database.get_db()
    if db is None:
        return "Erro: Não foi possível conectar ao banco de dados."

    update = {}
    if novo_modelo:
        update["modelo"] = novo_modelo
    if novo_valor is not None:
        try:
            update["valor"] = float(novo_valor)
        except Exception:
            return "Erro: valor inválido."

    if not update:
        return "Nenhuma informação fornecida para atualização."

    try:
        col = db.betoneiras
        res = col.update_one({"_id": ObjectId(id_betoneira)}, {"$set": update})
        if res.matched_count == 0:
            return "Erro: Betoneira não encontrada (ID inválido)."
        return "Dados da betoneira atualizados com sucesso!"
    except Exception as e:
        print(f"Erro inesperado [atualizar_dados_betoneira]: {e}", file=sys.stderr)
        return "Erro ao atualizar dados da betoneira."


def atualizar_status_manutencao(id_betoneira, novo_status):
    db = database.get_db()
    if db is None:
        return "Erro: Não foi possível conectar ao banco de dados."

    if novo_status == 'alugada':
        return "Erro: O status 'alugada' é definido automaticamente ao registrar um aluguel."

    status_permitidos = ['disponivel', 'manutencao']
    if novo_status not in status_permitidos:
        return f"Erro: Status '{novo_status}' não é válido para operação manual."

    try:
        col = db.betoneiras
        b = col.find_one({"_id": ObjectId(id_betoneira)})
        if not b:
            return "Erro: Betoneira não encontrada."
        if b.get("status") == 'alugada':
            return "Erro: Não é possível alterar o status de uma betoneira que está alugada."

        res = col.update_one({"_id": ObjectId(id_betoneira)}, {"$set": {"status": novo_status}})
        if res.matched_count == 0:
            return "Erro: Betoneira não encontrada (ID inválido)."
        return "Status da betoneira atualizado com sucesso!"
    except Exception as e:
        print(f"Erro inesperado [atualizar_status_manutencao]: {e}", file=sys.stderr)
        return "Erro ao atualizar status."


def deletar_betoneira(id_betoneira):
    db = database.get_db()
    if db is None:
        return "Erro: Não foi possível conectar ao banco de dados."

    try:
        col = db.betoneiras
        b = col.find_one({"_id": ObjectId(id_betoneira)})
        if not b:
            return "Erro: Betoneira não encontrada."
        if b.get("status") == 'alugada':
            return "Erro: Não é possível apagar uma betoneira que está atualmente alugada."

        # Verificar histórico de alugueis
        alug_col = db.alugueis
        if alug_col.find_one({"id_betoneira": id_betoneira}):
            return "Erro: Não é possível apagar a betoneira, pois ela possui um histórico de alugueres."

        res = col.delete_one({"_id": ObjectId(id_betoneira)})
        if res.deleted_count == 0:
            return "Erro ao apagar betoneira."
        return "Betoneira apagada com sucesso!"
    except Exception as e:
        print(f"Erro inesperado [deletar_betoneira]: {e}", file=sys.stderr)
        return "Erro ao apagar betoneira."
