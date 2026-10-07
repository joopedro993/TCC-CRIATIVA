import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def criar_conexao():
    conexao = sqlite3.connect("banco.db")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao
    

def criar_banco_turma():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas(
        id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_professor_fk INTEGER NOT NULL,
        
        
        FOREIGN KEY (id_professor_fk)
        REFERENCES professores(id_professor)
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

def adicionar_turma(nome, id_professor):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO turmas (nome, id_professor_fk)
        VALUES (?,?)
    """, (nome,id_professor))
    
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

def listar_turmas_por_professor(id_professor):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_turma,nome
        FROM turmas
        WHERE id_professor_fk = ?
    """, (id_professor,))

    turmas = cursor.fetchall()

    conexao.close()

    return [dict(turma) for turma in turmas]