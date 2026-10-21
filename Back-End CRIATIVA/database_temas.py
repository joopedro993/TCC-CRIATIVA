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
    

# Cria a tabela temas caso ela ainda não exista
def criar_banco_temas():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()
    
    # Cria a tabela temas com as colunas de ID,
    # título e textos motivadores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temas(
            id_tema INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            textos_motivadores TEXT NOT NULL
        )               
    """)
    

# Lista todos os temas cadastrados no banco de dados
def listar_tema():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona o ID, o título e os textos motivadores dos temas
    cursor.execute("""
        SELECT id_tema,titulo,textos_motivadores
        FROM temas
    """)

    # Recupera todos os temas encontrados
    temas = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()
    
    # Converte os registros em dicionários e retorna a lista
    return [dict(tema)for tema in temas]


# Adiciona um novo tema ao banco de dados
def adicionar_tema(titulo, textos_motivadores):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Insere o título e os textos motivadores na tabela temas
    cursor.execute("""
        INSERT INTO temas (titulo,textos_motivadores)
        VALUES (?,?)
    """, (titulo,textos_motivadores))
    
    # Salva o novo tema no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()
    
    # Retorna o título do tema adicionado
    return titulo


# Atualiza o título e os textos motivadores de um tema
def atualizar_tema(id_tema,titulo,textos_motivadore):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()
    
    # Atualiza o título e os textos motivadores
    # do tema correspondente ao ID informado
    cursor.execute("""
        UPDATE temas
        SET titulo = ?, textos_motivadores = ?
        WHERE id_tema = ?
    """,(id_tema,titulo,textos_motivadore))

    # Salva as alterações no banco de dados
    conexao.commit()

    # Recupera a quantidade de registros afetados pela atualização
    linhas_afetadas = cursor.rowcount

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a quantidade de registros atualizados
    return linhas_afetadas


# Exclui um tema pelo seu ID
def deletar_tema(id_tema):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Exclui o tema que possui o ID informado
    cursor.execute("""
        DELETE FROM temas
        WHERE id_tema = ?
    """, (id_tema,))

    # Salva a exclusão no banco de dados
    conexao.commit()

    # Recupera a quantidade de registros afetados pela exclusão
    linhas_afetadas = cursor.rowcount

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a quantidade de registros excluídos
    return linhas_afetadas


# Busca um tema pelo seu ID
def buscar_tema_por_id(id_tema):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona todos os dados do tema correspondente ao ID informado
    cursor.execute("""
        SELECT *
        FROM temas
        WHERE id_tema = ?

    """, (id_tema,))

    # Recupera o tema encontrado
    tema = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna o tema como dicionário se ele existir
    # Caso contrário, retorna None
    return dict(tema) if tema else None
