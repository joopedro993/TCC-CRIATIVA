from flask import Flask,request,jsonify
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from database_alunos import *
from database_professores import *
from database_escolas import *
from database_turma import *
from database_redacao import *
import os

serializador = URLSafeTimedSerializer(os.environ.get("SECRET_KEY", "criativa-dev123"))

app = Flask(__name__)

CORS(app)

def criar_bancos():
    criar_banco_alunos()
    criar_banco_professores()
    criar_banco_escolas()
    criar_banco_turma()
    criar_banco_redacao()

criar_bancos()

#===============================PROFESSORES====================================================================

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

@app.route("/professores/<int:id_professor>", methods=["GET"])
def obter_professor(id_professor):
    professor = buscar_professor(id_professor)

    if professor is None:
        return jsonify({
            "erro":"Professor não encontrado"
        }),404

    return jsonify(professor), 200

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

#===============================ALUNOS====================================================================

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

@app.route("/alunos/<int:id_aluno>", methods=["GET"])
def obter_aluno(id_aluno):
    aluno = buscar_aluno_por_id(id_aluno)

    if aluno is None:
        return jsonify({
            "erro": "Aluno não encontrado"
        }), 404

    return jsonify(aluno), 200

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

#===============================ESCOLAS====================================================================

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

#===============================TURMA====================================================================

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

@app.route("/turmas/<int:id_turma>", methods=["GET"])
def obter_turma(id_turma):
    turma = buscar_turma_por_id(id_turma)
    
    if turma is None:
        return jsonify({"erro":"Turma não encontrada"}), 404

    return jsonify(turma), 200

#===============================REDAÇÕES====================================================================

@app.route("/redacoes", methods=["GET"])
def buscar_redacoes():
    return jsonify(listar_redacoes())

@app.route("/redacoes", methods=["POST"])
def cadastrar_redacao():
    dados = request.get_json()

    tema = dados.get("tema")
    texto = dados.get("texto")
    id_aluno = dados.get("id_aluno")

    if not tema or not texto or not id_aluno:
        return jsonify({
            "erro":"tema, texto e id_aluno são obrigatorios"
        }), 400

    adicionar_redacao(tema,texto,id_aluno)

    return jsonify({
        "mensagem":"Redação cadastrada com sucesso"
    }),201



@app.route("/redacoes/<int_redacao>",methods=["GET"])
def obter_redacao(id_redacao):
    redacao = buscar_redacao_por_id(id_redacao)

    if not redacao:
        return jsonify({
            "erro":"Redação não encontrada"
        }), 404

    return jsonify(redacao)

@app.route("/redacoes/<int:id_redacao>", methods=["PUT"])
def editar_redacao(id_redacao):
    dados = request.get_json()

    nota = dados.get("nota")
    feedback = dados.get("feedback")

    atualizar_redacao(id_redacao, nota, feedback)

    return jsonify({
        "mensagem": "Redação atualizada com sucesso"
    })

@app.route("/redacoes/<int:id_redacao>", methods=["DELETE"])
def deletar_redacao(id_redacao):
    excluir_redacao(id_redacao)

    return jsonify({
        "mensagem": "Redação removida com sucesso"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5010)
