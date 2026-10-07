import sqlite3

def criar_conexao():
    conexao = sqlite3.connect("banco_redacao.db")
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_banco_redacao():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS redacoes(
            id_redacao INTEGER PRIMARY KEY AUTOINCREMENT,
            tema TEXT NOT NULL,
            texto TEXT NOT NULL,
            nota REAL,
            feedback TEXT,
            id_aluno INTEGER NOT NULL,
            id_aluno_fk INTEGER NOT NULL FOREIGN KEY
            REFERENCES alunos,
            id_atividade_fk INTEGER NOT NULL FOREIGN KEY
            REFERENCES atividades
            )

    """)

    conexao.commit()
    conexao.close()



def adicionar_redacao(tema,texto,id_aluno):
    conexao = criar_conexao()
    cursor = conexao.cursor()


    cursor.execute("""
        INSERT INTO redacoes
        (tema, texto, id_aluno)
        VALUES(?,?,?)


    """, (tema,texto,id_aluno))


    conexao.commit()
    conexao.close()


def listar_redacoes():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM redacoes

    """)

    redacoes = cursor.fetchall()

    conexao.close()

    return [dict(redacao) for redacao in redacoes]


def buscar_redacao_por_id(id_redacao):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM redacoes
        WHERE id_redacao = ?

    """, (id_redacao,))

    redacao = cursor.fetchone()

    conexao.close()

    return dict(redacao) if redacao else None

def atualizar_redacao(id_redacao,nota,feedback):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE redacoes
        SET nota = ?, feedback = ?
        WHERE id_redacao = ?


    """, (nota,feedback,id_redacao))


    conexao.commit()
    conexao.close()


def excluir_redacao(id_redacao):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM redacoes
        WHERE id_redacao = ?
    """, (id_redacao,))

    conexao.commit()
    conexao.close()