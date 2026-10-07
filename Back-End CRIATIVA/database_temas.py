import sqlite3

def criar_conexao():
    conexao = sqlite3.connect("banco_temas.db")
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    
    return conexao
    

def criar_banco_consultas():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temas(
            id_tema INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            textos_motivadores TEXT NOT NULL
        )               
    """)
    
def listar_tema():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_tema,titulo,textos_motivadores
        FROM turmas
    """)

    temas = cursor.fetchall()
    conexao.close()
    
    return [dict(tema)for tema in temas]

def adicionar_tema(titulo, textos_motivadores):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO temas (titulo,textos_motivadores)
        VALUES (?,?)
    """, (titulo,textos_motivadores))
    
    conexao.commit()
    conexao.close()
    
    return titulo

def atualizar_tema(id_tema,titulo,textos_motivadore):
    conexao = criar_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("""
        UPDATE temas
        SET titulo = ?, textos_motivadores = ?
        WHERE id_tema = ?
    """,(id_tema,titulo,textos_motivadore))

    conexao.commit()
    linhas_afetadas = cursor.rowcount
    conexao.close()

    return linhas_afetadas

def deletar_tema(id_tema):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM temas
        WHERE id_tema = ?
    """, (id_tema,))

    conexao.commit()
    linhas_afetadas = cursor.rowcount
    conexao.close()

    return linhas_afetadas

def buscar_tema_por_id(id_tema):
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT *
        FROM temas
        WHERE id_tema = ?

    """, (id_tema,))

    tema = cursor.fetchone()
    conexao.close()
    return dict(tema) if tema else None