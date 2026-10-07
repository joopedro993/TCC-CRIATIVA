import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def criar_conexao():
    conexao = sqlite3.connect("banco.db")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao
    

def criar_banco_alunos():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
        id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        id_turma_fk INTEGER NOT NULL,
        
        
        FOREIGN KEY (id_turma_fk)
        REFERENCES alunos(id_turma)
        )
    """)

    conexao.commit()
    conexao.close()

def listar_aluno():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_aluno, nome, email
        FROM alunos
    """)

    alunos = cursor.fetchall()
    conexao.close()

    return [dict(aluno) for aluno in alunos]

def adicionar_aluno(nome,email,senha):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    senha_hash = generate_password_hash(senha)

    cursor.execute("""
        INSERT INTO alunos (nome,email,senha)
        VALUES (?,?,?)
    """, (nome,email,senha_hash))

    conexao.commit()
    conexao.close()

    return nome

def deletar_aluno(id_aluno):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM alunos
        WHERE id_aluno = ?
    """, (id_aluno,))

    conexao.commit()
    linhas_afetadas = cursor.rowcount
    conexao.close()

    return linhas_afetadas

def atualizar_aluno(id_aluno,nome,email,senha):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    senha_hash = generate_password_hash(senha)

    cursor.execute("""
        UPDATE alunos
        SET nome = ?, email = ?, senha = ?
        WHERE id_aluno = ?
    """,(nome,email,senha_hash,id_aluno))

    conexao.commit()
    linhas_afetadas = cursor.rowcount
    conexao.close()

    return linhas_afetadas

def verificar_login(email,senha):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_aluno, nome, email, senha
        FROM alunos
        WHERE email = ?
    """, (email,))

    aluno = cursor.fetchone()
    conexao.close()

    if aluno is None:
        return None
    if not check_password_hash(aluno["senha"],senha):
        return None
    return {
        "id_aluno": aluno["id_aluno"],
        "nome": aluno["nome"],
        "email": aluno["email"]
    }

def buscar_aluno_por_id(id_aluno):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM alunos
        WHERE id_aluno = ?

    """, (id_aluno,))

    aluno = cursor.fetchone()
    conexao.close()
    return dict(aluno) if aluno else None