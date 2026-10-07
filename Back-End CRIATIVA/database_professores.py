import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def criar_conexao():
    conexao = sqlite3.connect("banco.db")
    conexao.row_factory = sqlite3.Row

    return conexao
    conexao.execute("PRAGMA foreign_keys = ON")


def criar_banco_professores():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            id_escola_fk INTEGER NOT NULL
            
            
            FOREIGN KEY(id_escola_fk)
            REFERENCES escolas(id_escola)
        )
    """)

    conexao.commit()
    conexao.close()


def adicionar_professor(nome, email, senha):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    senha_hash = generate_password_hash(senha)

    cursor.execute("""
        INSERT INTO professores (nome, email, senha)
        VALUES (?, ?, ?)
    """, (nome, email, senha_hash))

    conexao.commit()

    conexao.close()

    return nome


def listar_professores():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_professor, nome, email
        FROM professores
    """)

    professores = cursor.fetchall()

    conexao.close()

    return [dict(professor) for professor in professores]


def editar_professor(id_professor, nome, email, senha):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    senha_hash = generate_password_hash(senha)

    cursor.execute("""
        UPDATE professores
        SET nome = ?, email = ?, senha = ?
        WHERE id_professor = ?
    """, (nome, email, senha_hash, id_professor))

    conexao.commit()

    linhas_afetadas = cursor.rowcount

    conexao.close()

    return linhas_afetadas


def excluir_professor(id_professor):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM professores
        WHERE id_professor = ?
    """, (id_professor,))

    conexao.commit()

    linhas_afetadas = cursor.rowcount

    conexao.close()

    return linhas_afetadas

def verificar_login(email, senha):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_professor, nome, email, senha
        FROM professores
        WHERE email = ?
    """, (email,))

    professor = cursor.fetchone()

    conexao.close()

    if professor is None:
        return None

    if not check_password_hash(professor["senha"], senha):
        return None

    return {
        "id_professor": professor["id_professor"],
        "nome": professor["nome"],
        "email": professor["email"]
    }

def buscar_professor_por_id(id_professor):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM professores
        WHERE id_professor = ?
    """, (id_professor,))

    professor = cursor.fetchone()
    conexao.close()
    return dict(professor) if professor else None