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

    

# Cria a tabela redacoes caso ela ainda não exista
def criar_banco_redacao():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Cria a tabela redacoes com suas colunas e chaves estrangeiras
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS redacoes(
            id_redacao INTEGER PRIMARY KEY AUTOINCREMENT,
            tema TEXT NOT NULL,
            texto TEXT NOT NULL,
            data_envio TEXT NOT NULL,
            id_atividade_fk INTEGER NOT NULL,
            id_aluno_fk INTEGER NOT NULL,

            -- Impede que o mesmo aluno envie mais de uma redação para a mesma atividade
            UNIQUE(id_aluno_fk, id_atividade_fk),
            
            
            FOREIGN KEY(id_aluno_fk)
            REFERENCES alunos(id_aluno),
            FOREIGN KEY (id_atividade_fk)
            REFERENCES atividades(id_atividade)
            )

    """)

    # Salva as alterações no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()



# Adiciona uma nova redação ao banco de dados
def adicionar_redacao(tema,texto,id_aluno_fk,id_atividade_fk, dt_envio):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()


    # Insere o tema, o texto, o ID do aluno,
    # o ID da atividade e a data de envio da redação
    cursor.execute("""
        INSERT INTO redacoes
        (tema, texto, id_aluno_fk,id_atividade_fk, data_envio)
        VALUES(?,?,?,?,?)


    """, (tema,texto,id_aluno_fk,id_atividade_fk, dt_envio))


    # Salva a redação no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()
    return True # Retorna True indicando que deu tudo certo

except sqlite3.IntegrityError:
        # Se cair aqui, significa que a restrição UNIQUE foi violada
        # (ou seja, o aluno já enviou uma redação para essa atividade)
        if 'conexao' in locals() and conexao:
            conexao.close()
            
        return False  # Retorna False indicando que já existe um envio


# Lista todas as redações cadastradas no banco de dados
def listar_redacoes():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona todos os dados das redações cadastradas
    cursor.execute("""
        SELECT *
        FROM redacoes

    """)

    # Recupera todas as redações encontradas
    redacoes = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Converte os registros em dicionários e retorna a lista
    return [dict(redacao) for redacao in redacoes]


# Busca uma redação pelo seu ID
def buscar_redacao_por_id(id_redacao):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona a redação que possui o ID informado
    cursor.execute("""
        SELECT *
        FROM redacoes
        WHERE id_redacao = ?

    """, (id_redacao,))

    # Recupera a redação encontrada
    redacao = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a redação como dicionário se ela existir
    # Caso contrário, retorna None
    return dict(redacao) if redacao else None

# Exclui uma redação pelo seu ID
def excluir_redacao(id_redacao):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Exclui a redação que possui o ID informado
    cursor.execute("""
        DELETE FROM redacoes
        WHERE id_redacao = ?
    """, (id_redacao,))

    # Salva a exclusão no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()

def corrigir_datas_antigas():
    conexao = criar_conexao()
    cursor = conexao.cursor()
    
    # Atualiza todos os registos onde data_envio é "Não Consta"
    cursor.execute("""
        UPDATE redacoes 
        SET data_envio = '2026-01-01' 
        WHERE data_envio = 'Não Consta'
    """)
    
    conexao.commit()
    print(f"Registos atualizados com sucesso: {cursor.rowcount}")
    conexao.close()
