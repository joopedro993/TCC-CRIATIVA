# Importa as ferramentas do Flask para criar a API,
# receber requisições e retornar respostas em JSON
from flask import Flask, request, jsonify

# Importa o CORS para permitir requisições de outras origens
from flask_cors import CORS

# Importa ferramentas para criar e verificar tokens assinados
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

# Importa as funções relacionadas ao banco de dados dos alunos
from database_alunos import *

# Importa as funções relacionadas ao banco de dados dos professores
from database_professores import *

# Importa as funções relacionadas ao banco de dados das escolas
from database_escolas import *

# Importa as funções relacionadas ao banco de dados das turmas
from database_turma import *

# Importa as funções relacionadas ao banco de dados das redações
from database_redacao import *

# Importa as funções relacionadas ao banco de dados das atividades
from database_atividades import *

# Importa as funções relacionadas ao banco de dados dos temas
from database_temas import *

# Importa as funções relacionadas ao banco de dados das correções
from database_correcao import *

# Importa as funções relacionadas ao banco de dados das consultas
from database_consultas import *

# Importa a biblioteca os para acessar variáveis de ambiente
import os

# Importa a biblioteca json para trabalhar com dados no formato JSON
import json


# Cria um serializador para gerar e verificar tokens assinados
# Utiliza a chave secreta definida nas variáveis de ambiente
# Caso ela não exista, utiliza o valor padrão informado
serializador = URLSafeTimedSerializer(os.environ.get("SECRET_KEY", "criativa-dev123"))

# Cria a aplicação Flask
app = Flask(__name__)

# Habilita o CORS na aplicação para permitir requisições de outras origens
CORS(app)


# Cria as tabelas utilizadas pelo sistema
def criar_bancos():
    # Cria a tabela de alunos
    criar_banco_alunos()

    # Cria a tabela de professores
    criar_banco_professores()

    # Cria a tabela de escolas
    criar_banco_escolas()

    # Cria a tabela de turmas
    criar_banco_turma()

    # Cria a tabela de redações
    criar_banco_redacao()

    # Cria a tabela de correções
    criar_banco_correcoes()

    # Cria a tabela de temas
    criar_banco_temas()

    # Cria a tabela de consultas
    criar_banco_consultas()

    # Cria a tabela de atividades
    criar_banco_atividade()


# Executa a função para criar as tabelas ao iniciar a aplicação
criar_bancos()


# ===============================PROFESSORES====================================================================


# Define a rota para listar todos os professores
# O método GET é utilizado para consultar dados
@app.route("/professores", methods=["GET"])
def buscar_professor():

    # Recupera a lista de professores cadastrados
    lista_professores = listar_professores()

    # Retorna a lista de professores no formato JSON
    return jsonify(lista_professores)


# Define a rota para cadastrar um professor
# O método POST é utilizado para enviar novos dados
@app.route("/professores", methods=["POST"])
def cadastrar_professor():

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Obtém o nome informado
    nome = dados.get("nome")

    # Obtém o email informado
    email = dados.get("email")

    # Obtém a senha informada
    senha = dados.get("senha")

    # Obtém o identificador da escola
    escola = dados.get("escola")

    # Verifica se os campos obrigatórios foram preenchidos
    if not nome or not email or not senha or not escola:
        # Retorna uma mensagem de erro com o status HTTP 400
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    # Cadastra o professor no banco de dados
    id_professor = adicionar_professor(nome, email, senha, escola)

    # Retorna uma mensagem de sucesso com o status HTTP 201
    return jsonify({"mensagem": f"O professor {id_professor} foi adicionado"}), 201


# Define a rota para atualizar um professor pelo ID
# O método PUT é utilizado para atualizar dados existentes
@app.route("/professores/<int:id_professor>", methods=["PUT"])
def atualizar_professor(id_professor):

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Obtém o novo nome do professor
    nome = dados.get("nome")

    # Obtém o novo email do professor
    email = dados.get("email")

    # Obtém a nova senha do professor
    senha = dados.get("senha")

    # Obtém o identificador da escola
    escola = dados.get("id_escola_fk")

    # Verifica se os campos obrigatórios foram preenchidos
    if not nome or not email or not senha or not escola:
        # Retorna um erro caso algum campo esteja vazio
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    # Atualiza os dados do professor no banco de dados
    resultado = editar_professor(id_professor, nome, email, senha, escola)

    # Verifica se nenhum registro foi atualizado
    if resultado == 0:
        # Retorna o status HTTP 404 se o professor não for encontrado
        return jsonify({"erro": "Professor não encontrado"}), 404

    # Retorna uma mensagem de sucesso com o status HTTP 200
    return jsonify({"mensagem": "Professor editado com sucesso"}), 200


# Define a rota para excluir um professor pelo ID
# O método DELETE é utilizado para remover dados
@app.route("/professores/<int:id_professor>", methods=["DELETE"])
def deletar_professor(id_professor):

    # Exclui o professor do banco de dados
    resultado = excluir_professor(id_professor)

    # Verifica se nenhum registro foi excluído
    if resultado == 0:
        # Retorna um erro caso o professor não exista
        return jsonify({"erro": "Professor não encontrado"}), 404

    # Retorna uma mensagem de sucesso
    return jsonify({"mensagem": "Professor excluído com sucesso"}), 200


# Define a rota para consultar um professor específico pelo ID
@app.route("/professores/<int:id_professor>", methods=["GET"])
def obter_professor(id_professor):

    # Busca o professor pelo identificador informado
    professor = buscar_professor_por_id(id_professor)

    # Verifica se o professor não foi encontrado
    if professor is None:
        # Retorna o status HTTP 404
        return jsonify({"erro": "Professor não encontrado"}), 404

    # Retorna os dados do professor no formato JSON
    return jsonify(professor), 200


# Define a rota para listar os professores de uma escola específica
@app.route("/professores/escola/<int:id_escola>", methods=["GET"])
def buscar_professores_por_escola(id_escola):

    # Busca os professores vinculados à escola informada
    professores = listar_professores_por_escola(id_escola)

    # Retorna a lista de professores no formato JSON
    return jsonify(professores)


# Define a rota para realizar o login de professores
# O método POST recebe as credenciais de acesso
@app.route("/professores/login", methods=["POST"])
def login_professores():

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Exibe os dados recebidos no terminal para depuração
    print("DADOS RECEBIDOS:", dados)

    # Obtém o email informado e remove espaços nas extremidades,
    # convertendo as letras para minúsculas
    email = dados.get("emailLancar").strip().lower()

    # Obtém a senha informada
    senha = dados.get("senhaLancar")

    # Exibe o email no terminal para depuração
    print("EMAIL:", email)

    # Exibe a senha recebida no terminal para depuração
    print("SENHA RECEBIDA:", senha)

    # Verifica se o email ou a senha estão vazios
    if not email or not senha:
        # Retorna um erro com o status HTTP 400
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    # Verifica se as credenciais do professor são válidas
    professor = verificar_login_professores(email, senha)

    # Exibe o resultado da verificação no terminal
    print("RESULTADO DO LOGIN:", professor)

    # Verifica se o login falhou
    if professor is None:
        # Retorna o status HTTP 401 para credenciais inválidas
        return jsonify({"erro": "Email ou senha incorretos"}), 401

    # Cria um token contendo o ID do professor e seu tipo de usuário
    token = serializador.dumps({"id": professor["id_professor"], "tipo": "professor"})

    # Verifica a validade e o prazo máximo do token
    # O limite informado é de 3600 segundos, equivalente a uma hora
    serializador.loads(token, max_age=3600)

    # Retorna a mensagem de sucesso, os dados do professor e o token
    return (
        jsonify(
            {
                "mensagem": "Login realizado com sucesso",
                "professor": professor,
                "token": token,
            }
        ),
        200,
    )


# ===============================ALUNOS====================================================================


# Define a rota para listar todos os alunos
@app.route("/alunos", methods=["GET"])
def buscar_aluno():

    # Recupera a lista de alunos cadastrados
    lista_alunos = listar_aluno()

    # Retorna a lista de alunos no formato JSON
    return jsonify(lista_alunos)


# Define a rota para listar os alunos de uma turma específica
@app.route("/alunos/turmas/<int:id_turma>", methods=["GET"])
def buscar_aluno_por_turma(id_turma):

    # Busca os alunos vinculados à turma informada
    alunos = listar_alunos_por_turma(id_turma)

    # Retorna a lista de alunos no formato JSON
    return jsonify(alunos)


# Define a rota para cadastrar um novo aluno
@app.route("/alunos", methods=["POST"])
def cadastrar_aluno():

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Obtém o nome do aluno
    nome = dados.get("nome")

    # Obtém o email do aluno
    email = dados.get("email")

    # Obtém a senha do aluno
    senha = dados.get("senha")

    # Obtém o identificador da turma
    turma = dados.get("turma")

    # Verifica se os campos obrigatórios foram preenchidos
    if not nome or not email or not senha or not turma:
        # Retorna uma mensagem de erro com o status HTTP 400
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    # Cadastra o aluno no banco de dados
    id_aluno = adicionar_aluno(nome, email, senha, turma)

    # Retorna uma mensagem de sucesso com o status HTTP 201
    return jsonify({"mensagem": f"O aluno {id_aluno} foi adicionado"}), 201


# Define a rota para excluir um aluno pelo ID
@app.route("/alunos/<int:id_aluno>", methods=["DELETE"])
def excluir_aluno(id_aluno):

    # Exclui o aluno do banco de dados
    resultado = deletar_aluno(id_aluno)

    # Verifica se nenhum registro foi excluído
    if resultado == 0:
        # Retorna um erro caso o aluno não exista
        return jsonify({"erro": "aluno não encontrado"}), 404

    # Retorna uma mensagem confirmando a exclusão
    return jsonify({"mensagem": "aluno excluído com sucesso."}), 200


# Define a rota para atualizar os dados de um aluno
@app.route("/alunos/<int:id_aluno>", methods=["PUT"])
def editar_aluno(id_aluno):

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Obtém o novo nome do aluno
    nome = dados.get("nome")

    # Obtém o novo email do aluno
    email = dados.get("email")

    # Obtém a nova senha do aluno
    senha = dados.get("senha")

    # Obtém o identificador da turma
    turma = dados.get("turma")

    # Verifica se os campos obrigatórios foram preenchidos
    if not nome or not email or not senha or not turma:
        # Retorna um erro caso algum campo esteja vazio
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    # Atualiza os dados do aluno no banco de dados
    resultado = atualizar_aluno(id_aluno, nome, email, senha, turma)

    # Verifica se nenhum registro foi atualizado
    if resultado == 0:
        # Retorna um erro caso o aluno não exista
        return jsonify({"erro": "aluno não encontrado."}), 404

    # Retorna uma mensagem de sucesso
    return jsonify({"mensagem": "aluno editado com sucesso."}), 200


# Define a rota para consultar um aluno específico pelo ID
@app.route("/alunos/<int:id_aluno>", methods=["GET"])
def obter_aluno(id_aluno):

    # Busca o aluno pelo identificador informado
    aluno = buscar_aluno_por_id(id_aluno)

    # Verifica se o aluno não foi encontrado
    if aluno is None:
        # Retorna o status HTTP 404
        return jsonify({"erro": "Aluno não encontrado"}), 404

    # Retorna os dados do aluno no formato JSON
    return jsonify(aluno), 200


# Define a rota para realizar o login de alunos
@app.route("/alunos/login", methods=["POST"])
def login_alunos():

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Exibe os dados recebidos no terminal para depuração
    print("DADOS RECEBIDOS:", dados)

    # Obtém o email informado
    email = dados.get("emailLancar")

    # Obtém a senha informada
    senha = dados.get("senhaLancar")

    # Exibe o email no terminal para depuração
    print("EMAIL:", email)

    # Exibe a senha recebida no terminal para depuração
    print("SENHA RECEBIDA:", senha)

    # Verifica se o email ou a senha estão vazios
    if not email or not senha:
        # Retorna um erro com o status HTTP 400
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    # Verifica se as credenciais do aluno são válidas
    aluno = verificar_login_aluno(email, senha)

    # Exibe o resultado da verificação no terminal
    print("RESULTADO DO LOGIN:", aluno)

    # Verifica se o login falhou
    if aluno is None:
        # Retorna o status HTTP 401 para credenciais inválidas
        return jsonify({"erro": "Email ou senha incorretos"}), 401

    # Cria um token contendo o ID do aluno e seu tipo de usuário
    token = serializador.dumps({"id": aluno["id_aluno"], "tipo": "aluno"})

    # Verifica a validade e o prazo máximo do token
    # O limite informado é de 3600 segundos, equivalente a uma hora
    serializador.loads(token, max_age=3600)

    # Retorna a mensagem de sucesso, os dados do aluno e o token
    return (
        jsonify(
            {"mensagem": "Login realizado com sucesso", "aluno": aluno, "token": token}
        ),
        200,
    )


# ===============================ESCOLAS====================================================================


# Define a rota para listar todas as escolas
@app.route("/escolas", methods=["GET"])
def buscar_escola():

    # Recupera a lista de escolas cadastradas
    lista_escolas = listar_escolas()

    # Retorna a lista de escolas no formato JSON
    return jsonify(lista_escolas)


# Define a rota para cadastrar uma escola
@app.route("/escolas", methods=["POST"])
def cadastrar_escola():

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Obtém o nome da escola
    nome = dados.get("nome")

    # Verifica se o nome foi informado
    if not nome:
        # Retorna uma mensagem de erro com o status HTTP 400
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    # Cadastra a escola no banco de dados
    id_escola = adicionar_escola(nome)

    # Retorna uma mensagem de sucesso com o status HTTP 201
    return jsonify({"mensagem": f"A escola {id_escola} foi adicionada"}), 201


# Define a rota para excluir uma escola pelo ID
@app.route("/escolas/<int:id_escola>", methods=["DELETE"])
def deletar_escola(id_escola):

    # Exclui a escola do banco de dados
    resultado = excluir_escolas(id_escola)

    # Verifica se nenhuma escola foi excluída
    if resultado == 0:
        # Retorna um erro caso a escola não exista
        return jsonify({"erro": "escola não encontrada"}), 404

    # Retorna uma mensagem confirmando a exclusão
    return jsonify({"mensagem": "escola excluída com sucesso."}), 200


# ===============================TURMA====================================================================


# Define a rota para listar todas as turmas
@app.route("/turmas", methods=["GET"])
def buscar_turma():

    # Recupera a lista de turmas cadastradas
    lista_turma = listar_turma()

    # Retorna a lista de turmas no formato JSON
    return jsonify(lista_turma)


# Define a rota para cadastrar uma turma
@app.route("/turmas", methods=["POST"])
def cadastrar_turma():

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Obtém o nome da turma
    nome = dados.get("nome")

    # Obtém o identificador do professor responsável
    id_professor = dados.get("professor")

    # Verifica se o nome e o professor foram informados
    if not nome or not id_professor:
        # Retorna uma mensagem de erro com o status HTTP 400
        return jsonify({"erro": "O nome da turma é obrigatório"}), 400

    # Cadastra a turma no banco de dados
    adicionar_turma(nome, id_professor)

    # Retorna uma mensagem confirmando o cadastro
    return jsonify({"mensagem": "Turma cadastrada com sucesso."}), 200


# Define a rota para consultar uma turma específica pelo ID
@app.route("/turmas/<int:id_turma>", methods=["GET"])
def obter_turma(id_turma):

    # Busca a turma pelo identificador informado
    turma = buscar_turma_por_id(id_turma)

    # Verifica se a turma não foi encontrada
    if turma is None:
        # Retorna o status HTTP 404
        return jsonify({"erro": "Turma não encontrada"}), 404

    # Retorna os dados da turma no formato JSON
    return jsonify(turma), 200


# Define a rota para listar as turmas de um professor
@app.route("/turmas/professores/<int:id_professor>", methods=["GET"])
def buscar_turmas_por_professor(id_professor):

    # Busca as turmas vinculadas ao professor informado
    turmas = listar_turmas_por_professor(id_professor)

    # Retorna a lista de turmas no formato JSON
    return jsonify(turmas)


# ===============================REDAÇÕES====================================================================


# Define a rota para listar todas as redações
@app.route("/redacoes", methods=["GET"])
def buscar_redacoes():

    # Recupera e retorna a lista de redações
    return jsonify(listar_redacoes())


# Define a rota para cadastrar uma nova redação
@app.route("/redacoes", methods=["POST"])
def cadastrar_redacao():

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Obtém o tema da redação
    tema = dados.get("tema")

    # Obtém o texto escrito pelo aluno
    texto = dados.get("texto")

    # Obtém o identificador do aluno
    id_aluno = dados.get("id_aluno")

    # Obtém o identificador da atividade relacionada
    id_atividade = dados.get("id_atividade")

    # Obtém a data de envio da redação
    data_envio = dados.get("data_envio")

    # Verifica se os campos obrigatórios foram preenchidos
    if not tema or not texto or not id_aluno or not id_atividade:
        # Retorna um erro com o status HTTP 400
        return jsonify({"erro": "tema, texto e id_aluno são obrigatorios"}), 400

    # Salva a redação no banco de dados
    adicionar_redacao(tema, texto, id_aluno, id_atividade, data_envio)

    # Retorna uma mensagem de sucesso com o status HTTP 201
    return jsonify({"mensagem": "Redação cadastrada com sucesso"}), 201


# Define a rota para consultar uma redação pelo ID
@app.route("/redacoes/<int:id_redacao>", methods=["GET"])
def obter_redacao(id_redacao):

    # Busca a redação pelo identificador informado
    redacao = buscar_redacao_por_id(id_redacao)

    # Verifica se a redação não foi encontrada
    if not redacao:
        # Retorna o status HTTP 404
        return jsonify({"erro": "Redação não encontrada"}), 404

    # Retorna os dados da redação no formato JSON
    return jsonify(redacao)


# Define a rota para atualizar uma redação pelo ID
@app.route("/redacoes/<int:id_redacao>", methods=["PUT"])
def editar_redacao(id_redacao):

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Obtém a nota da redação
    nota = dados.get("nota")

    # Obtém o feedback da correção
    feedback = dados.get("feedback")

    # Atualiza a nota e o feedback da redação
    atualizar_redacao(id_redacao, nota, feedback)

    # Retorna uma mensagem confirmando a atualização
    return jsonify({"mensagem": "Redação atualizada com sucesso"})


# Define a rota para excluir uma redação pelo ID
@app.route("/redacoes/<int:id_redacao>", methods=["DELETE"])
def deletar_redacao(id_redacao):

    # Exclui a redação do banco de dados
    excluir_redacao(id_redacao)

    # Retorna uma mensagem confirmando a remoção
    return jsonify({"mensagem": "Redação removida com sucesso"})


# ===============================ATIVIDADES====================================================================


# Define a rota para listar todas as atividades
@app.route("/atividades", methods=["GET"])
def buscar_atividades():

    # Recupera e retorna a lista de atividades
    return jsonify(listar_atividades())


# Define a rota para cadastrar uma atividade
@app.route("/atividades", methods=["POST"])
def cadastrar_atividade():

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Obtém o título da atividade
    titulo = dados.get("titulo")

    # Obtém o tema da atividade
    tema = dados.get("tema")

    # Obtém a descrição da atividade
    descricao = dados.get("descricao")

    # Obtém a data de disponibilização da atividade
    data_disponibilizacao = dados.get("data_disponibilizacao")

    # Obtém o prazo para realizar a atividade
    prazo = dados.get("prazo")

    # Obtém o identificador da turma relacionada
    id_turma = dados.get("id_turma")

    # Obtém o identificador do tema relacionado
    id_tema = dados.get("id_tema")

    # Verifica se todos os campos indicados foram preenchidos
    if not all([titulo, tema, descricao, data_disponibilizacao, prazo, id_turma]):
        # Retorna um erro caso algum campo esteja vazio
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    # Cadastra a atividade com seus dados e identificadores relacionados
    adicionar_atividade(titulo, tema, descricao, data_disponibilizacao, prazo, id_tema, id_turma)

    # Retorna uma mensagem de sucesso com o status HTTP 201
    return jsonify({"mensagem": "Atividade cadastrada com sucesso"}), 201


# Define a rota para consultar uma atividade pelo ID
@app.route("/atividades/<int:id_atividade>", methods=["GET"])
def obter_atividade(id_atividade):

    # Busca a atividade pelo identificador informado
    atividade = buscar_atividade_por_id(id_atividade)

    # Verifica se a atividade não foi encontrada
    if not atividade:
        # Retorna o status HTTP 404
        return jsonify({"erro": "Atividade não encontrada"}), 404

    # Retorna os dados da atividade no formato JSON
    return jsonify(atividade)


# Define a rota para atualizar uma atividade pelo ID
@app.route("/atividades/<int:id_atividade>", methods=["PUT"])
def editar_atividade(id_atividade):

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Atualiza os dados da atividade com os valores recebidos
    atualizar_atividade(
        id_atividade,
        dados.get("titulo"),
        dados.get("tema"),
        dados.get("descricao"),
        dados.get("data_disponibilizacao"),
        dados.get("prazo"),
    )

    # Retorna uma mensagem confirmando a atualização
    return jsonify({"mensagem": "Atividade atualizada com sucesso"})


# Define a rota para excluir uma atividade pelo ID
@app.route("/atividades/<int:id_atividade>", methods=["DELETE"])
def deletar_atividade(id_atividade):

    # Exclui a atividade do banco de dados
    excluir_atividade(id_atividade)

    # Retorna uma mensagem confirmando a remoção
    return jsonify({"mensagem": "Atividade removida com sucesso"})


# Define a rota para listar as atividades de uma turma específica
@app.route("/atividades/turma/<int:id_turma>", methods=["GET"])
def buscar_atividades_por_turma(id_turma):

    # Busca as atividades vinculadas à turma informada
    atividades = listar_atividades_por_turma(id_turma)

    # Retorna a lista de atividades no formato JSON
    return jsonify(atividades)


# =======================================CORREÇÃO=======================================================

# Define a rota para listar todas as correções
@app.route("/correcao", methods=["GET"])
def buscar_correcao():

    # Recupera a lista de correções cadastradas
    lista_correcao = listar_correcao()

    # Retorna a lista de correções no formato JSON
    return jsonify(lista_correcao)


# Define a rota para consultar uma correção pelo ID
@app.route("/correcao/<int:id_correcao>", methods=["GET"])
def obter_correcao(id_correcao):

    # Busca a correção pelo identificador informado
    correcao = buscar_correcao_por_id(id_correcao)

    # Verifica se a correção não foi encontrada
    if not correcao:
        # Retorna o status HTTP 404
        return jsonify({"erro": "Correção não encontrada!"}), 404

    # Retorna os dados da correção no formato JSON
    return jsonify(correcao)


# Define a rota para cadastrar uma correção
@app.route("/correcao", methods=["POST"])
def cadastrar_correcao():

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Obtém o ID da correção
    id_correcao = dados.get("id_correcao")

    # Obtém o ID da redação que será corrigida
    id_redacao_fk = dados.get("id_redacao")

    # Obtém o ID do professor responsável pela correção
    id_professor_fk = dados.get("id_professor")

    # Obtém as notas das cinco competências
    competencia_1 = dados.get("competencia_1")
    competencia_2 = dados.get("competencia_2")
    competencia_3 = dados.get("competencia_3")
    competencia_4 = dados.get("competencia_4")
    competencia_5 = dados.get("competencia_5")
    
    # Obtém o comentário da correção
    comentario = dados.get("comentario")

    # Obtém a data em que a correção foi realizada
    data_correcao = dados.get("data_correcao")

    # Verifica se todos os campos indicados foram preenchidos
    if not all(
        [
            id_correcao,
            id_redacao_fk,
            id_professor_fk,
            competencia_1,
            competencia_2,
            competencia_3,
            competencia_4,
            competencia_5,
            comentario,
            data_correcao,
        ]
    ):
        # Retorna um erro caso algum campo esteja vazio
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    # Calcula a nota total somando as cinco competências
    nota_total = (
            competencia_1 + competencia_2 + competencia_3 + competencia_4 + competencia_5
        )
    
    # Salva a correção no banco de dados
    adicionar_correcao(
        id_correcao,
        id_redacao_fk,
        id_professor_fk,
        competencia_1,
        competencia_2,
        competencia_3,
        competencia_4,
        competencia_5,
        nota_total,
        comentario,
        data_correcao,
    )

    # Retorna uma mensagem de sucesso com o status HTTP 201
    return jsonify({"mensagem": "Correção cadastrada com sucesso"}), 201


# O bloco abaixo contém uma rota de edição de correção
# que está desativada porque foi colocada dentro de aspas triplas
"""@app.route("/correcao/<int:id_correcao>", methods=["PUT"])
def editar_correcao(id_correcao):
    dados = request.get_json()

    id_redacao_fk = dados("id_redacao")
    id_professor_fk = dados("id_professor")
    competencia_1 = dados("competencia_1")
    competencia_2 = dados("competencia_2")
    competencia_3 = dados("competencia_3")
    competencia_4 = dados("competencia_4")
    competencia_5 = dados("competencia_5")
    nota_total = (
        competencia_1 + competencia_2 + competencia_3 + competencia_4 + competencia_5
    )
    comentario = dados("comentario")
    data_correcao = dados("data_correcao")

    atualizar_correcao(
        id_correcao,
        id_redacao_fk,
        id_professor_fk,
        competencia_1,
        competencia_2,
        competencia_3,
        competencia_4,
        competencia_5,
        nota_total,
        comentario,
        data_correcao,
    )

    return jsonify({"mensagem": "Correção atualizada com sucesso"}), 200"""


# =========================================TEMA============================================================

# Define a rota para listar todos os temas
@app.route("/temas", methods=["GET"])
def buscar_tema():

    # Recupera a lista de temas cadastrados
    lista_temas = listar_tema()

    # Retorna a lista de temas no formato JSON
    return jsonify(lista_temas)


# Define a rota para consultar um tema pelo ID
@app.route("/temas/<int:id>", methods=["GET"])
def obter_tema(id):

    # Busca o tema pelo identificador informado
    tema = buscar_tema_por_id(id)

    # Verifica se o tema não foi encontrado
    if not tema:
        # Retorna uma mensagem de erro com o status HTTP 404
        return jsonify({"erro": "Correção não encontrada!"}), 404

    # Retorna os dados do tema no formato JSON
    return jsonify(tema)


# Define a rota para cadastrar um novo tema
@app.route("/temas", methods=["POST"])
def cadastrar_tema():

    # Recupera os dados enviados na requisição
    dados = request.get_json()

    # Obtém o título do tema
    titulo = dados["titulo"]

    # Converte os textos motivadores para uma string JSON
    # O parâmetro ensure_ascii=False mantém os caracteres especiais
    textos_motivadores = json.dumps(dados["textos_motivadores"], ensure_ascii=False)

    # Verifica se o título e os textos motivadores foram preenchidos
    if not all([titulo, textos_motivadores]):

        # Retorna um erro caso algum campo esteja vazio
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    # Cadastra o tema no banco de dados
    adicionar_tema(titulo, textos_motivadores)

    # Retorna uma mensagem de sucesso com o status HTTP 201
    return jsonify({"mensagem": "Tema cadastrado com sucesso"}), 201


# Verifica se este arquivo está sendo executado diretamente
if __name__ == "__main__":

    # Inicia o servidor Flask na porta 5010
    # O modo debug permite visualizar erros durante o desenvolvimento
    app.run(debug=True, port=5010)
