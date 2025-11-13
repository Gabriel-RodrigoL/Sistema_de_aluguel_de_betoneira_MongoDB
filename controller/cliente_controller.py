from conexion import database
import sys
from bson.objectid import ObjectId


def cadastrar_cliente(nome, telefone, cpf):
    db = database.get_db()
    if db is None:
        return "Erro: Não foi possível conectar ao banco de dados."

    try:
        col = db.clientes
        # Verifica unicidade de cpf e telefone
        if col.find_one({"cpf": cpf}):
            return "Erro: O CPF informado já está registado."
        if col.find_one({"telefone": telefone}):
            return "Erro: O telefone informado já está registado."

        doc = {"nome": nome, "telefone": telefone, "cpf": cpf}
        res = col.insert_one(doc)
        return f"Cliente registado com sucesso! id: {str(res.inserted_id)}"
    except Exception as e:
        print(f"Erro inesperado [cadastrar_cliente]: {e}", file=sys.stderr)
        return "Erro ao registar cliente."


def atualizar_cliente(id_cliente, novo_nome, novo_telefone):
    db = database.get_db()
    if db is None:
        return "Erro: Não foi possível conectar ao banco de dados."

    update = {}
    if novo_nome:
        update["nome"] = novo_nome
    if novo_telefone:
        update["telefone"] = novo_telefone

    if not update:
        return "Nenhuma informação fornecida para atualização."

    try:
        col = db.clientes
        # Se novo_telefone for fornecido, verificar duplicidade
        if novo_telefone and col.find_one({"telefone": novo_telefone, "_id": {"$ne": ObjectId(id_cliente)}}):
            return "Erro: O novo telefone informado já pertence a outro cliente."

        res = col.update_one({"_id": ObjectId(id_cliente)}, {"$set": update})
        if res.matched_count == 0:
            return "Erro: Cliente não encontrado (ID inválido)."
        return "Cliente atualizado com sucesso!"
    except Exception as e:
        print(f"Erro inesperado [atualizar_cliente]: {e}", file=sys.stderr)
        return "Erro ao atualizar cliente."


def deletar_cliente(id_cliente):
    db = database.get_db()
    if db is None:
        return "Erro: Não foi possível conectar ao banco de dados."

    try:
        col = db.clientes
        c = col.find_one({"_id": ObjectId(id_cliente)})
        if not c:
            return "Erro: Cliente não encontrado."

        # Verificar histórico de alugueis
        alug_col = db.alugueis
        if alug_col.find_one({"id_cliente": id_cliente}):
            return "Erro: Não é possível apagar um cliente que possui um histórico de alugueres."

        res = col.delete_one({"_id": ObjectId(id_cliente)})
        if res.deleted_count == 0:
            return "Erro ao apagar cliente."
        return "Cliente apagado com sucesso!"
    except Exception as e:
        print(f"Erro inesperado [deletar_cliente]: {e}", file=sys.stderr)
        return "Erro ao apagar cliente."

