from flask import Flask, request, jsonify
from flask_cors import CORS
from database_turma import *

app = Flask(__name__)

CORS(app)

criar_banco_turma()

@app.route("/turmas", methods=["GET"])
def buscar_turma():
    lista_turma = listar_turma()

    return jsonify(lista_turma)

@app.route("/turmas", methods=["POST"])
def cadastrar_turma():
    dados = request.get_json()
    nome = dados.get("nome")

    if not nome:
        return jsonify({
            "erro": "O nome da turma é obrigatório"
        }), 400
    
    adicionar_turma(nome)

    return jsonify({
        "mensagem": "Turma cadastrada com sucesso."
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5004)
