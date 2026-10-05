from flask import Flask, jsonify, request
from flask_cors import CORS
from database_escolas import *

app = Flask(__name__)

CORS(app)

criar_banco_escolas()

@app.route("/escolas", methods=["GET"])
def buscar_escola():
    lista_escolas = listar_escolas()

    return jsonify(lista_escolas)

@app.route("/escolas", methods=["POST"])
def cadastrar_escola():
    dados = request.get_json()
    nome = dados.get("nome")

    if not nome:
        return jsonify({
            "erro": "Nome, email e senha são obrigatórios"
        }), 400

    id_escola = adicionar_escola(
        nome
    )

    return jsonify({
        "mensagem": f"A escola {id_escola} foi adicionada"
    }), 201

@app.route("/escolas/<int:id_escola>", methods=["DELETE"])
def deletar_escola(id_escola):
    resultado = excluir_escolas(id_escola)

    if resultado == 0:
        return jsonify({
            "erro": "escola não encontrada"
        }), 404
    
    return jsonify({
        "mensagem": "escola excluída com sucesso."
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5003)
