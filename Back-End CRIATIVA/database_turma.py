import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def criar_conexao():
    conexao = sqlite3.connect("banco_turma.db")
    conexao.row_factory = sqlite3.Row

    return conexao

def criar_banco_turma():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas(
        id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_professor_fk INTEGER NOT NULL FOREIGN KEY
        REFERENCES professores
        )
    """)

    conexao.commit()
    conexao.close()

def listar_turma():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_turma,id_professor_fk,nome
        FROM turmas
    """)

    turmas = cursor.fetchall()
    conexao.close()
    
    return [dict(turma)for turma in turmas]

def adicionar_turma(nome):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO turmas (nome)
        VALUES (?)
    """, (nome,))
    
    conexao.commit()
    conexao.close()
    
    return nome

def buscar_turma_por_id(id_turma):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM turmas
        WHERE id_turma = ?
    """, (id_turma,))

    turma = cursor.fetchone()
    conexao.close()

    return dict(turma) if turma else None