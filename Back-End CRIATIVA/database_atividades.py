# Importa a biblioteca sqlite3 para trabalhar com o banco de dados
import sqlite3


# Cria e configura uma conexão com o banco de dados
def criar_conexao():
    # Conecta ao banco de dados banco.db
    conexao = sqlite3.connect("banco.db")

    # Permite acessar os valores das colunas pelo nome
    conexao.row_factory = sqlite3.Row

    # Ativa a verificação das chaves estrangeiras
    conexao.execute("PRAGMA foreign_keys = ON") 
    
    # Retorna a conexão criada
    return conexao
    

# Cria a tabela de atividades caso ela ainda não exista
def criar_banco_atividade():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Cria a tabela atividades com suas colunas e chaves estrangeiras
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

    # Salva as alterações no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()



# Adiciona uma nova atividade ao banco de dados
def adicionar_atividade(titulo,tema,descricao,data_disponibilizacao,prazo,id_tema_fk,id_turma_fk):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Insere os dados da atividade na tabela atividades
    cursor.execute("""
        INSERT INTO atividades
        (titulo, tema, descricao, data_disponibilizacao, prazo,id_tema_fk,id_turma_fk)
        VALUES (?, ?, ?, ?, ?,?,?)
    """, (titulo,tema,descricao,data_disponibilizacao,prazo,id_tema_fk,id_turma_fk))

    # Salva a atividade no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()



# Lista todas as atividades cadastradas
def listar_atividades():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona todos os registros da tabela atividades
    cursor.execute("""
        SELECT *
        FROM atividades
    """)

    # Recupera todas as atividades encontradas
    atividades = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Converte os registros em dicionários e retorna a lista
    return [dict(atividade) for atividade in atividades]


# Busca uma atividade pelo seu ID
def buscar_atividade_por_id(id_atividade):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona a atividade que possui o ID informado
    cursor.execute("""
        SELECT *
        FROM atividades
        WHERE id_atividade = ?
    """, (id_atividade,))

    # Recupera a atividade encontrada
    atividade = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a atividade como dicionário se ela existir
    # Caso contrário, retorna None
    return dict(atividade) if atividade else None





# Atualiza os dados de uma atividade pelo seu ID
def atualizar_atividade(
    id_atividade,
    titulo,
    tema,
    descricao,
    data_disponibilizacao,
    prazo
):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Atualiza o título, o tema, a descrição,
    # a data de disponibilização e o prazo da atividade
    # correspondente ao ID informado
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

    # Salva as alterações no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()




# Exclui uma atividade pelo seu ID
def excluir_atividade(id_atividade):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Exclui a atividade que possui o ID informado
    cursor.execute("""
        DELETE FROM atividades
        WHERE id_atividade = ?
    """, (id_atividade,))

    # Salva a exclusão no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()
    

# Lista as atividades pertencentes a uma determinada turma
def listar_atividades_por_turma(id_turma):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()
    
    # Seleciona o ID, o título, o tema,
    # a data de disponibilização e o prazo das atividades
    # que pertencem à turma informada
    cursor.execute("""
                   SELECT id_atividade, titulo, tema, data_disponibilizacao, prazo,descricao
                   FROM atividades
                   WHERE id_turma_fk = ?""",
                   (id_turma,))
    
    # Recupera todas as atividades encontradas para a turma
    atividades = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()
    
    # Converte os registros em dicionários e retorna a lista
    return [dict (atividade) for atividade in atividades]
