from flask import Flask, jsonify, request
from flask_cors import CORS
from database_alunos import *

app = Flask(__name__)

CORS(app)

criar_banco_alunos()

@app.route("/alunos", methods=["GET"])
def buscar_aluno():
    lista_alunos = listar_aluno()

    return jsonify(lista_alunos)

@app.route("/alunos", methods=["POST"])
def cadastrar_aluno():
    dados = request.get_json()
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        return jsonify({
            "erro": "Nome, email e senha são obrigatórios"
        }), 400

    id_aluno = adicionar_aluno(
        nome,
        email,
        senha
    )

    return jsonify({
        "mensagem": f"O aluno {id_aluno} foi adicionado"
    }), 201

@app.route("/alunos/<int:id_aluno>", methods=["DELETE"])
def excluir_aluno(id_aluno):
    resultado = deletar_aluno(id_aluno)

    if resultado == 0:
        return jsonify({
            "erro": "aluno não encontrado"
        }), 404
    
    return jsonify({
        "mensagem": "aluno excluído com sucesso."
    }), 200

@app.route("/alunos/<int:id_aluno>", methods=["PUT"])
def editar_aluno(id_aluno):
    dados = request.get_json()

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        return jsonify({
            "erro": "Nome, email e senha são obrigatórios"
        }), 400
    
    resultado = atualizar_aluno(id_aluno,nome,email,senha)

    if resultado == 0:
        return jsonify({
            "erro": "aluno não encontrado."
        }), 404
    
    return jsonify({
        "mensagem": "aluno editado com sucesso."
    }), 200

@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    print("DADOS RECEBIDOS:", dados)

    email = dados.get("email")
    senha = dados.get("senha")

    print("EMAIL:", email)
    print("SENHA RECEBIDA:", senha)

    if not email or not senha:
        return jsonify({
            "erro": "Email e senha são obrigatórios"
        }), 400

    aluno = verificar_login(email, senha)

    print("RESULTADO DO LOGIN:", aluno)

    if aluno is None:
        return jsonify({
            "erro": "Email ou senha incorretos"
        }), 401

    return jsonify({
        "mensagem": "Login realizado com sucesso",
        "aluno": aluno
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
