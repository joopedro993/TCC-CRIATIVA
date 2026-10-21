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
    

# Cria a tabela consultas caso ela ainda não exista
def criar_banco_consultas():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()
    
    # Cria a tabela consultas com suas colunas e chave estrangeira
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas(
            id_consulta INTEGER PRIMARY KEY AUTOINCREMENT,
            conteudo TEXT NOT NULL,
            id_redacao_fk INTEGER NOT NULL,
            
            
            FOREIGN KEY (id_redacao_fk)
            REFERENCES redacoes(id_redacao)
        )               
    """)
    
    # Salva as alterações no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()


# Lista todas as consultas cadastradas no banco de dados
def listar_consultas():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona o ID da consulta, o ID da redação relacionada e o conteúdo
    cursor.execute("""
        SELECT id_consulta, id_redacao_fk, conteudo
        FROM consultas
    """)

    # Recupera todas as consultas encontradas
    consultas = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()
    
    # Converte os registros em dicionários e retorna a lista
    return [dict(consulta)for consulta in consultas]


# Adiciona uma nova consulta ao banco de dados
def adicionar_consulta(id_consulta,id_redacao_fk,conteudo):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Insere os dados informados na tabela indicada pelo comando SQL
    cursor.execute("""
        INSERT INTO turmas (id_consulta,id_redacao_fk,conteudo)
        VALUES (?,?,?)
    """, (id_consulta,id_redacao_fk,conteudo))
    
    # Salva as alterações no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()
    
    # Retorna o ID da consulta informado
    return id_consulta


# Busca uma consulta pelo seu ID
def buscar_consulta_por_id(id_consulta):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona todos os dados da consulta que possui o ID informado
    cursor.execute("""
        SELECT * FROM consultas
        WHERE id_consulta = ?
    """, (id_consulta,))

    # Recupera o primeiro registro encontrado
    consulta = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a consulta como dicionário se ela existir
    # Caso contrário, retorna None
    return dict(consulta) if consulta else None

    
