import sqlite3

def criar_conexao():
    conexao = sqlite3.connect("banco.db")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")    
    
    return conexao
    

def criar_banco_correcoes():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS correcoes(
            id_correcao INTEGER PRIMARY KEY AUTOINCREMENT,
            conteudo TEXT NOT NULL,
            competencia_1 INTEGER,
            competencia_2 INTEGER,
            competencia_3 INTEGER,
            competencia_4 INTEGER,
            competencia_5 INTEGER,
            nota_total INTEGER,
            comentario TEXT NOT NULL,
            data_correcao DATE NOT NULL,
            id_redacao_fk INTEGER NOT NULL,
            id_professor_fk INTEGER NOT NULL,
            
            FOREIGN KEY (id_redacao_fk)
            REFERENCES redacoes(id_redacao),

            FOREIGN KEY(id_professor_fk)
            REFERENCES professores(id_professor)
        )               
    """)
    
def listar_correcao():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_correcao, id_redacao_fk, id_professor_fk, competencia_1, competencia_2, competencia_3, competencia_4, competencia_5, nota_total, comentario, data_correcao
        FROM correcoes
    """)

    correcoes = cursor.fetchall()
    conexao.close()
    
    return [dict(correcao)for correcao in correcoes]

def adicionar_correcao(id_correcao,id_redacao_fk,id_professor_fk,competencia_1,competencia_2,competencia_3,competencia_4,competencia_5,nota_total,comentario,data_correcao):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO correcoes (id_redacao_fk, id_professor_fk, competencia_1, competencia_2, competencia_3, competencia_4, competencia_5, nota_total, comentario, data_correcao)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (id_redacao_fk,id_professor_fk,competencia_1,competencia_2, competencia_3, competencia_4, competencia_5, nota_total, comentario, data_correcao))
    
    conexao.commit()
    conexao.close()
    
    return id_correcao

def buscar_correcao_por_id(id_correcao):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM correcoes
        WHERE id_correcao = ?
    """, (id_correcao,))

    correcao = cursor.fetchone()
    conexao.close()

    return dict(correcao) if correcao else None

def atualizar_correcao(id_correcao,id_professor_fk, competencia_1, competencia_2, competencia_3, competencia_4, competencia_5, nota_total, comentario, data_correcao):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE correcoes
        SET id_professor_fk = ?, competencia_1 = ?, competencia_2 = ?, competencia_3 = ?, competencia_4 = ?, competencia_5 = ?, nota_total = ?, comentario = ?, data_correcao = ?
        WHERE id_correcao = ?
    """,(id_professor_fk, competencia_1, competencia_2, competencia_3, competencia_4, competencia_5, nota_total, comentario, data_correcao,id_correcao))

    conexao.commit()
    linhas_afetadas = cursor.rowcount
    conexao.close()

    return linhas_afetadas