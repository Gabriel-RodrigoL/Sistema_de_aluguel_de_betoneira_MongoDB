from conexion import database
import sys
from bson.objectid import ObjectId


def registrar_aluguel(id_cliente, id_betoneira, data_inicio, data_prevista_termino):
    db = database.get_db()
    if db is None:
        return "Erro: Não foi possível conectar ao banco de dados."

    try:
        bet_col = db.betoneiras
        alug_col = db.alugueis

        b = bet_col.find_one({"_id": ObjectId(id_betoneira)})
        if not b:
            return "Erro: Betoneira não encontrada."
        if b.get("status") != 'disponivel':
            return f"Erro: A betoneira não está disponível (status: {b.get('status')})."

        data_inicio_str = str(data_inicio) if not isinstance(data_inicio, str) else data_inicio
        data_prevista_termino_str = str(data_prevista_termino) if not isinstance(data_prevista_termino, str) else data_prevista_termino

        doc = {
            "id_cliente": id_cliente,
            "id_betoneira": id_betoneira,
            "data_inicio": data_inicio_str,
            "data_prevista_termino": data_prevista_termino_str,
            "status": "ativo"
        }
        res = alug_col.insert_one(doc)

        bet_col.update_one({"_id": ObjectId(id_betoneira)}, {"$set": {"status": "alugada"}})

        return f"Aluguel registado com sucesso! id: {str(res.inserted_id)}"
    except Exception as e:
        print(f"Erro inesperado [registrar_aluguel]: {e}", file=sys.stderr)
        return "Erro ao registar aluguel."


def finalizar_aluguel(id_aluguel, data_termino_real):
    db = database.get_db()
    if db is None:
        return "Erro: Não foi possível conectar ao banco de dados."

    try:
        alug_col = db.alugueis
        bet_col = db.betoneiras

        alug = alug_col.find_one({"_id": ObjectId(id_aluguel)})
        if not alug or alug.get("status") != 'ativo':
            return f"Erro: Aluguel com ID {id_aluguel} não encontrado ou já finalizado."

        data_termino_real_str = str(data_termino_real) if not isinstance(data_termino_real, str) else data_termino_real

        alug_col.update_one({"_id": ObjectId(id_aluguel)}, {"$set": {"data_termino_real": data_termino_real_str, "status": "finalizado"}})

        id_betoneira = alug.get("id_betoneira")
        bet_col.update_one({"_id": ObjectId(id_betoneira)}, {"$set": {"status": "disponivel"}})

        return f"Aluguel {id_aluguel} finalizado. Betoneira {id_betoneira} libertada."
    except Exception as e:
        print(f"Erro inesperado [finalizar_aluguel]: {e}", file=sys.stderr)
        return "Erro ao finalizar aluguel."
