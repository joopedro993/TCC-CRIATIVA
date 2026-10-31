# Importa a biblioteca sqlite3 para trabalhar com o banco de dados SQLite
import sqlite3

# Importa funções para gerar e verificar hashes de senhas
from werkzeug.security import generate_password_hash, check_password_hash


# Cria e configura uma conexão com o banco de dados
def criar_conexao():
    # Conecta ao banco de dados banco.db
    conexao = sqlite3.connect("banco.db")

    # Permite acessar os dados das consultas pelo nome das colunas
    conexao.row_factory = sqlite3.Row

    # Ativa a verificação das chaves estrangeiras no SQLite
    conexao.execute("PRAGMA foreign_keys = ON")

    # Retorna a conexão criada
    return conexao
    

# Cria a tabela de alunos caso ela ainda não exista
def criar_banco_alunos():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Cria a tabela alunos com suas colunas e restrições
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
        id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        id_turma_fk INTEGER NOT NULL,
        
        
        FOREIGN KEY (id_turma_fk)
        REFERENCES turmas(id_turma)
        )
    """)

    # Salva as alterações no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()


# Lista todos os alunos cadastrados no banco de dados
def listar_aluno():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona o ID, o nome, o email e o ID da turma de cada aluno
    # A senha não é incluída nessa consulta
    cursor.execute("""
        SELECT id_aluno, nome, email, id_turma_fk
        FROM alunos
    """)

    # Recupera todos os registros encontrados
    alunos = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Converte cada registro em um dicionário e retorna a lista de alunos
    return [dict(aluno) for aluno in alunos]


# Adiciona um novo aluno ao banco de dados
def adicionar_aluno(nome,email,senha,id_turma_fk):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Gera um hash da senha para não armazená-la em texto puro
    senha_hash = generate_password_hash(senha)

    # Insere os dados do aluno na tabela
    cursor.execute("""
        INSERT INTO alunos (nome,email,senha,id_turma_fk)
        VALUES (?,?,?,?)
    """, (nome,email,senha_hash,id_turma_fk))

    # Salva o cadastro no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna o nome do aluno cadastrado
    return nome


# Exclui um aluno pelo seu ID
def deletar_aluno(id_aluno):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Exclui o aluno cujo ID corresponde ao informado
    cursor.execute("""
        DELETE FROM alunos
        WHERE id_aluno = ?
    """, (id_aluno,))

    # Salva as alterações no banco de dados
    conexao.commit()

    # Recupera a quantidade de linhas afetadas pelo comando
    linhas_afetadas = cursor.rowcount

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a quantidade de registros excluídos
    return linhas_afetadas


# Atualiza os dados de um aluno pelo seu ID
def atualizar_aluno(id_aluno,nome,email,senha):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Gera um novo hash para a senha informada
    senha_hash = generate_password_hash(senha)

    # Atualiza o nome, o email e a senha do aluno correspondente ao ID
    cursor.execute("""
        UPDATE alunos
        SET nome = ?, email = ?, senha = ?, id_turma_fk = ?
        WHERE id_aluno = ?
    """,(nome,email,senha_hash,id_aluno))

    # Salva as alterações no banco de dados
    conexao.commit()

    # Recupera a quantidade de linhas afetadas pela atualização
    linhas_afetadas = cursor.rowcount

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a quantidade de registros atualizados
    return linhas_afetadas


# Verifica se o email e a senha informados são válidos
def verificar_login_aluno(email,senha):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Busca o aluno que possui o email informado
    cursor.execute("""
        SELECT id_aluno, nome, email, senha
        FROM alunos
        WHERE email = ?
    """, (email,))

    # Recupera o primeiro registro encontrado
    aluno = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Se nenhum aluno for encontrado, retorna None
    if aluno is None:
        return None

    # Compara a senha informada com o hash armazenado
    # Se a senha estiver incorreta, retorna None
    if not check_password_hash(aluno["senha"],senha):
        return None

    # Se o login for válido, retorna os dados do aluno
    # A senha não é incluída no retorno
    return {
        "id_aluno": aluno["id_aluno"],
        "nome": aluno["nome"],
        "email": aluno["email"]
    }


# Busca os dados de um aluno pelo seu ID
def buscar_aluno_por_id(id_aluno):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona todas as colunas do aluno correspondente ao ID
    cursor.execute("""
        SELECT id_aluno, nome, email, id_turma_fk
        FROM alunos
        WHERE id_aluno = ?

    """, (id_aluno,))

    # Recupera o registro encontrado
    aluno = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Se o aluno existir, converte os dados em dicionário
    # Caso contrário, retorna None
    return dict(aluno) if aluno else None


# Lista todos os alunos que pertencem a uma determinada turma
def listar_alunos_por_turma(id_turma):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Busca o ID, o nome e o email dos alunos da turma informada
    cursor.execute("""
        SELECT id_aluno,nome, email 
        FROM alunos
        WHERE id_turma_fk = ?
    """, (id_turma,))

    # Recupera todos os alunos encontrados na turma
    alunos = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Converte os registros em dicionários e retorna a lista
    return [dict(aluno) for aluno in alunos]
