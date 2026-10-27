# Importa a biblioteca sqlite3 para trabalhar com o banco de dados
import sqlite3


# Cria e configura uma conexão com o banco de dados
def criar_conexao():
    # Conecta ao banco de dados banco.db
    conexao = sqlite3.connect("banco.db")

    # Permite acessar os dados das consultas pelo nome das colunas
    conexao.row_factory = sqlite3.Row

    # Ativa a verificação das chaves estrangeiras no SQLite
    conexao.execute("PRAGMA foreign_keys = ON")    
    
    # Retorna a conexão criada
    return conexao
    

# Cria a tabela correcoes caso ela ainda não exista
def criar_banco_correcoes():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()
    
    # Cria a tabela correcoes com as notas, os comentários,
    # a data da correção e as referências à redação e ao professor
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS correcoes(
            id_correcao INTEGER PRIMARY KEY AUTOINCREMENT,
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
    conexao.commit()
    conexao.close()
    
    # Define as colunas da tabela e suas chaves estrangeiras


# Lista todas as correções cadastradas no banco de dados
def listar_correcao():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona os dados das correções, incluindo as notas
    # das cinco competências, a nota total e o comentário
    cursor.execute("""
        SELECT id_correcao, id_redacao_fk, id_professor_fk, competencia_1, competencia_2, competencia_3, competencia_4, competencia_5, nota_total, comentario, data_correcao
        FROM correcoes
    """)

    # Recupera todas as correções encontradas
    correcoes = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()
    
    # Converte os registros em dicionários e retorna a lista
    return [dict(correcao)for correcao in correcoes]


# Adiciona uma nova correção ao banco de dados
def adicionar_correcao(id_correcao,id_redacao_fk,id_professor_fk,competencia_1,competencia_2,competencia_3,competencia_4,competencia_5,nota_total,comentario,data_correcao):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Insere os dados da correção na tabela correcoes
    # São armazenadas as notas, o comentário, a data,
    # o ID da redação e o ID do professor responsável
    cursor.execute("""
        INSERT INTO correcoes (id_redacao_fk, id_professor_fk, competencia_1, competencia_2, competencia_3, competencia_4, competencia_5, nota_total, comentario, data_correcao)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (id_redacao_fk,id_professor_fk,competencia_1,competencia_2, competencia_3, competencia_4, competencia_5, nota_total, comentario, data_correcao))
    
    # Salva a nova correção no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()
    
    # Retorna o ID da correção informado
    return id_correcao


# Busca uma correção pelo seu ID
def buscar_correcao_por_id(id_correcao):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona todos os dados da correção que possui o ID informado
    cursor.execute("""
        SELECT * FROM correcoes
        WHERE id_correcao = ?
    """, (id_correcao,))

    # Recupera a correção encontrada
    correcao = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a correção como dicionário se ela existir
    # Caso contrário, retorna None
    return dict(correcao) if correcao else None


# Atualiza as informações de uma correção existente
def atualizar_correcao(id_correcao,id_professor_fk, competencia_1, competencia_2, competencia_3, competencia_4, competencia_5, nota_total, comentario, data_correcao):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Atualiza o professor responsável, as notas das competências,
    # a nota total, o comentário e a data da correção
    # da correção correspondente ao ID informado
    cursor.execute("""
        UPDATE correcoes
        SET id_professor_fk = ?, competencia_1 = ?, competencia_2 = ?, competencia_3 = ?, competencia_4 = ?, competencia_5 = ?, nota_total = ?, comentario = ?, data_correcao = ?
        WHERE id_correcao = ?
    """,(id_professor_fk, competencia_1, competencia_2, competencia_3, competencia_4, competencia_5, nota_total, comentario, data_correcao,id_correcao))

    # Salva as alterações no banco de dados
    conexao.commit()

    # Recupera a quantidade de linhas afetadas pela atualização
    linhas_afetadas = cursor.rowcount

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a quantidade de registros atualizados
    return linhas_afetadas
