import sqlite3

def criar_conexao():
    conexao = sqlite3.connect("banco_alunos.db")
    conexao.row_factory = sqlite3.Row

    return conexao

def criar_banco_atividade():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
        id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        tema TEXT NOT NULL,
        descricao TEXT NOT NULL,
        data_disponibilizacao DATE NOT NULL,
        prazo INTEGER NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()
    
def listar_atividade():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT id_atividade, titulo, tema, descricao, data_disponibilizacao, prazo
        FROM atividades               
    """)
    
    atividades = cursor.fetchall()
    conexao.close()
    
    return [dict(atividade)for atividade in atividades]

def adicionar_atividade(titulo,tema,descricao,data_disponibilizacao,prazo):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("""
        INSERT INTO atividades (titulo,tema,descricao,data_disponibilizacao,prazo)
        VALUES (?,?,?,?,?)    
    """, (titulo,tema,descricao,data_disponibilizacao,prazo))
    
    conexao.commit()
    conexao.close()
    
    return titulo