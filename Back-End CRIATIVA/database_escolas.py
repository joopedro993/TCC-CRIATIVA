import sqlite3

def criar_conexao():
    conexao = sqlite3.connect("banco_escolas.db")
    conexao.row_factory = sqlite3.Row
    
    return conexao
    conexao.execute("PRAGMA foreign_keys = ON")

def criar_banco_escolas():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS escolas (
                       id_escola INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT
                   )
                   """)
    
def listar_escolas():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT id_escola, nome
        FROM escolas
    """)
    
    escolas = cursor.fetchall()
    conexao.close()
    
    return [dict(escola) for escola in escolas]
    
def adicionar_escola(nome):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("""
        INSERT INTO escolas (nome)
        VALUES (?)                   
    """, (nome,))
    conexao.commit()
    conexao.close()
    
    return nome

def excluir_escolas(id_escola):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM escolas
        WHERE id_escola = ?
    """, (id_escola,))

    conexao.commit()

    linhas_afetadas = cursor.rowcount

    conexao.close()

    return linhas_afetadas
    
    
    
    
    