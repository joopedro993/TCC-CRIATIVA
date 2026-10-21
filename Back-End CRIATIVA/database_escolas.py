# Importa a biblioteca sqlite3 para trabalhar com o banco de dados
import sqlite3


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
    

# Cria a tabela escolas caso ela ainda não exista
def criar_banco_escolas():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()
    
    # Cria a tabela escolas com as colunas de ID e nome
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS escolas (
                       id_escola INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT
                   )
                   """)
    
# Lista todas as escolas cadastradas no banco de dados
def listar_escolas():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()
    
    # Seleciona o ID e o nome de todas as escolas
    cursor.execute("""
        SELECT id_escola, nome
        FROM escolas
    """)
    
    # Recupera todas as escolas encontradas
    escolas = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()
    
    # Converte os registros em dicionários e retorna a lista
    return [dict(escola) for escola in escolas]
    

# Adiciona uma nova escola ao banco de dados
def adicionar_escola(nome):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()
    
    # Insere o nome da escola na tabela escolas
    cursor.execute("""
        INSERT INTO escolas (nome)
        VALUES (?)                   
    """, (nome,))

    # Salva a nova escola no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()
    
    # Retorna o nome da escola adicionada
    return nome


# Exclui uma escola pelo seu ID
def excluir_escolas(id_escola):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Exclui a escola que possui o ID informado
    cursor.execute("""
        DELETE FROM escolas
        WHERE id_escola = ?
    """, (id_escola,))

    # Salva a exclusão no banco de dados
    conexao.commit()

    # Recupera a quantidade de registros afetados pela exclusão
    linhas_afetadas = cursor.rowcount

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a quantidade de registros excluídos
    return linhas_afetadas

    
    
    