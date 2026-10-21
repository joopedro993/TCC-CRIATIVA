# Importa a biblioteca sqlite3 para trabalhar com o banco de dados
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
    

# Cria a tabela turmas caso ela ainda não exista
def criar_banco_turma():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Cria a tabela turmas com as colunas de ID, nome
    # e a chave estrangeira que relaciona a turma ao professor
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas(
        id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_professor_fk INTEGER NOT NULL,
        
        
        FOREIGN KEY (id_professor_fk)
        REFERENCES professores(id_professor)
        )
    """)

    # Salva as alterações no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()


# Lista todas as turmas cadastradas no banco de dados
def listar_turma():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona o ID da turma, o ID do professor responsável e o nome
    cursor.execute("""
        SELECT id_turma,id_professor_fk,nome
        FROM turmas
    """)

    # Recupera todas as turmas encontradas
    turmas = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()
    
    # Converte os registros em dicionários e retorna a lista
    return [dict(turma)for turma in turmas]


# Adiciona uma nova turma ao banco de dados
def adicionar_turma(nome, id_professor):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Insere o nome da turma e o ID do professor responsável
    cursor.execute("""
        INSERT INTO turmas (nome, id_professor_fk)
        VALUES (?,?)
    """, (nome,id_professor))
    
    # Salva a nova turma no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()
    
    # Retorna o nome da turma adicionada
    return nome


# Busca uma turma pelo seu ID
def buscar_turma_por_id(id_turma):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona todos os dados da turma correspondente ao ID informado
    cursor.execute("""
        SELECT * FROM turmas
        WHERE id_turma = ?
    """, (id_turma,))

    # Recupera a turma encontrada
    turma = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a turma como dicionário se ela existir
    # Caso contrário, retorna None
    return dict(turma) if turma else None


# Lista as turmas vinculadas a um determinado professor
def listar_turmas_por_professor(id_professor):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona o ID e o nome das turmas
    # que pertencem ao professor informado
    cursor.execute("""
        SELECT id_turma,nome
        FROM turmas
        WHERE id_professor_fk = ?
    """, (id_professor,))

    # Recupera todas as turmas encontradas
    turmas = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Converte os registros em dicionários e retorna a lista
    return [dict(turma) for turma in turmas]
