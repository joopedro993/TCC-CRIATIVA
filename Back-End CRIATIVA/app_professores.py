from flask import Flask, jsonify, request
from flask_cors import CORS
from database_professores import *
import os
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

serializador = URLSafeTimedSerializer(os.environ.get("SECRET_KEY", "criativa-dev123"))

app = Flask(__name__)

CORS(app)

criar_banco_professores()


@app.route("/professores", methods=["GET"])
def buscar_professor():

    lista_professores = listar_professores()

    return jsonify(lista_professores)


@app.route("/professores", methods=["POST"])
def cadastrar_professor():

    dados = request.get_json()

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        return jsonify({
            "erro": "Nome, email e senha são obrigatórios"
        }), 400

    id_professor = adicionar_professor(
        nome,
        email,
        senha
    )

    return jsonify({
        "mensagem": f"O professor {id_professor} foi adicionado"
    }), 201


@app.route("/professores/<int:id_professor>", methods=["PUT"])
def atualizar_professor(id_professor):

    dados = request.get_json()

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        return jsonify({
            "erro": "Nome, email e senha são obrigatórios"
        }), 400

    resultado = editar_professor(
        id_professor,
        nome,
        email,
        senha
    )

    if resultado == 0:
        return jsonify({
            "erro": "Professor não encontrado"
        }), 404

    return jsonify({
        "mensagem": "Professor editado com sucesso"
    }), 200


@app.route("/professores/<int:id_professor>", methods=["DELETE"])
def deletar_professor(id_professor):

    resultado = excluir_professor(id_professor)

    if resultado == 0:
        return jsonify({
            "erro": "Professor não encontrado"
        }), 404

    return jsonify({
        "mensagem": "Professor excluído com sucesso"
    }), 200

@app.route("/professores/login", methods=["POST"])
def login():
    dados = request.get_json()

    print("DADOS RECEBIDOS:", dados)

    email = dados.get("emailLancar")
    senha = dados.get("senhaLancar")

    print("EMAIL:", email)
    print("SENHA RECEBIDA:", senha)

    if not email or not senha:
        return jsonify({
            "erro": "Email e senha são obrigatórios"
        }), 400

    professor = verificar_login(email, senha)

    print("RESULTADO DO LOGIN:", professor)

    if professor is None:
        return jsonify({
            "erro": "Email ou senha incorretos"
        }), 401
        
    token = serializador.dumps(
        {"id":professor["id_professor"],
         "tipo":"professor"}
        )
    serializador.loads(token, max_age=3600)

    return jsonify({
        "mensagem": "Login realizado com sucesso",
        "professor": professor,
        "token":token
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)