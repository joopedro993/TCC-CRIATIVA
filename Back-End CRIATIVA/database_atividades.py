import sqlite3

def criar_conexao():
    conexao = sqlite3.connect("banco.db")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON") 
    
    return conexao
    

def criar_banco_atividade():
    conexao = criar_conexao()
    cursor = conexao.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atividades(
            id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            tema TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data_disponibilizacao TEXT NOT NULL,
            prazo TEXT NOT NULL,
            id_tema_fk INTEGER NOT NULL,
            id_turma_fk INTEGER NOT NULL,
            
            
            FOREIGN KEY (id_tema_fk)
            REFERENCES temas(id_tema),

            FOREIGN KEY (id_turma_fk)
            REFERENCES turmas(id_turma)
        )
    """)

    conexao.commit()
    conexao.close()



def adicionar_atividade(titulo,tema,descricao,data_disponibilizacao,prazo,id_turma,id_tema_fk,id_turma_fk):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO atividades
        (titulo, tema, descricao, data_disponibilizacao, prazo, id_turma,id_tema_fk,id_turma_fk)
        VALUES (?, ?, ?, ?, ?, ?,?,?)
    """, (titulo,tema,descricao,data_disponibilizacao,prazo,id_turma,id_tema_fk,id_turma_fk))

    conexao.commit()
    conexao.close()



def listar_atividades():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM atividades
    """)

    atividades = cursor.fetchall()

    conexao.close()

    return [dict(atividade) for atividade in atividades]


def buscar_atividade_por_id(id_atividade):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM atividades
        WHERE id_atividade = ?
    """, (id_atividade,))

    atividade = cursor.fetchone()

    conexao.close()

    return dict(atividade) if atividade else None





def atualizar_atividade(
    id_atividade,
    titulo,
    tema,
    descricao,
    data_disponibilizacao,
    prazo
):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE atividades
        SET titulo = ?,
            tema = ?,
            descricao = ?,
            data_disponibilizacao = ?,
            prazo = ?
        WHERE id_atividade = ?
    """, (
        titulo,
        tema,
        descricao,
        data_disponibilizacao,
        prazo,
        id_atividade
    ))

    conexao.commit()
    conexao.close()




def excluir_atividade(id_atividade):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM atividades
        WHERE id_atividade = ?
    """, (id_atividade,))

    conexao.commit()
    conexao.close()