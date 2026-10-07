import sqlite3

def criar_conexao():
    conexao = sqlite3.connect("banco.db")
    conexao.row_factory = sqlite3.Row
    
    return conexao
    conexao.execute("PRAGMA foreign_keys = ON")

def criar_banco_consultas():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas(
            id_consulta INTEGER PRIMARY KEY AUTOINCREMENT,
            conteudo TEXT NOT NULL,
            id_redacao_fk INTEGER NOT NULL
            
            
            FOREIGN KEY (id_redacao_fk)
            REFERENCES redacoes(id_redacao)
        )               
    """)

def listar_consultas():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_consulta, id_redacao_fk, conteudo
        FROM consultas
    """)

    consultas = cursor.fetchall()
    conexao.close()
    
    return [dict(consulta)for consulta in consultas]

def adicionar_consulta(id_consulta,id_redacao_fk,conteudo):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO turmas (id_consulta,id_redacao_fk,conteudo)
        VALUES (?,?,?)
    """, (id_consulta,id_redacao_fk,conteudo))
    
    conexao.commit()
    conexao.close()
    
    return id_consulta

def buscar_consulta_por_id(id_consulta):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM consultas
        WHERE id_consulta = ?
    """, (id_consulta,))

    consulta = cursor.fetchone()
    conexao.close()

    return dict(consulta) if consulta else None

    
